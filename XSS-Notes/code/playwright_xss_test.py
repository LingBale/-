"""
本代码对应PDF文件中的“XSS 自动化工具运用与开发：自定义脚本开发：JPython + Selenium/Puppeteer/Playwright构建动态扫描器”
本代码用于测试XSS漏洞，使用Playwright库进行自动化测试。
"""

from playwright.sync_api import sync_playwright
import time

def test_xss(url, param_name, payload):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # 可设 headless=True
        page = browser.new_page()
        
        # 监听 alert 事件
        page.on("dialog", lambda dialog: print(f"Alert triggered: {dialog.message}"))
        
        # 构造测试 URL
        test_url = url.replace("FUZZ", payload)  # 假设参数位置用 FUZZ 标记
        page.goto(test_url)
        time.sleep(2)  # 等待页面执行
        browser.close()