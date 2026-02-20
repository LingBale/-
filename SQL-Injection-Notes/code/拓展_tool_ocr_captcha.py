"""
验证码识别工具 - 使用 Tesseract OCR
需要安装 Tesseract 和 pytesseract
"""

import pytesseract
from PIL import Image
import requests
from io import BytesIO
import sys

def recognize_captcha_from_url(image_url):
    """从 URL 识别验证码"""
    try:
        response = requests.get(image_url, timeout=10)
        if response.status_code == 200:
            img = Image.open(BytesIO(response.content))
            # 转为灰度图，提高识别率
            img = img.convert('L')
            # 使用 Tesseract 识别，配置为单字符模式（可根据实际调整）
            text = pytesseract.image_to_string(img, config='--psm 8')
            return text.strip()
        else:
            print(f"[!] 无法下载图片: {image_url}")
            return None
    except Exception as e:
        print(f"[!] 识别失败: {e}")
        return None

def recognize_captcha_from_file(file_path):
    """从本地文件识别验证码"""
    try:
        img = Image.open(file_path)
        img = img.convert('L')
        text = pytesseract.image_to_string(img, config='--psm 8')
        return text.strip()
    except Exception as e:
        print(f"[!] 识别失败: {e}")
        return None

def main():
    print("=" * 50)
    print("验证码识别工具 (Tesseract OCR)")
    print("=" * 50)
    if len(sys.argv) < 2:
        print("用法:")
        print("  python 拓展_tool_ocr_captcha.py <图片URL或本地路径>")
        sys.exit(1)

    path = sys.argv[1]
    if path.startswith("http"):
        result = recognize_captcha_from_url(path)
    else:
        result = recognize_captcha_from_file(path)

    if result:
        print(f"[+] 识别结果: {result}")
    else:
        print("[-] 识别失败")

if __name__ == "__main__":
    main()