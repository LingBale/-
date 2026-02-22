# XSS 学习笔记

本目录包含跨站脚本（XSS）的完整学习资料，包括 PDF 笔记、本地测试环境以及多种语言编写的脚本工具。

## 📂 目录结构

- `XSS-Notes.pdf`：XSS 详细笔记（50+ 页，涵盖基础概念、检测技巧、绕过手法、挖掘思路、自动化工具、防御机制及 2023-2026 前沿案例）
- `lab/`：本地测试环境文件（含多种 XSS 漏洞页面）
  - `index.php`：测试平台导航页
  - 多个 PHP 文件：反射型、存储型、DOM 型、JavaScript 上下文、属性注入、CSS 注入、JSONP 回调等漏洞场景
  - `advanced/`：高级场景文件夹
  - `comments.txt`：存储型 XSS 的数据文件（自动创建）
  - `README.md`：环境搭建详细说明
- `code/`：XSS 相关脚本集（Python、JavaScript、Ruby 等）
  - `esprima.py`：基于 AST 的 Payload 生成器
  - `Fuzzing.py`：XSS Payload 模糊测试字典生成器
  - `Jython.py`：Burp Suite 扩展示例（Jython 扫描器）
  - `Playwright.py`：使用 Playwright 的自动化 XSS 测试脚本（Python）
  - `puppeteer_xss.js`：使用 Puppeteer 的自动化 XSS 测试脚本（Node.js）
  - `xss_tampermonkey_helper.user.js`：Tampermonkey 用户脚本，辅助手工测试
  - `beef_xss_module.rb`：BeEF 自定义模块示例（Ruby）

## 🚀 快速开始

1. **搭建本地测试环境**：按照 `lab/README.md` 的步骤配置 Web 服务器并访问测试页面。
2. **运行自动化脚本**：进入 `code/` 目录，根据脚本说明安装依赖并执行（如 `python Playwright.py`）。
3. **深入学习笔记**：打开 `XSS-Notes.pdf`，结合测试环境动手实践，理解每个漏洞的原理与利用方式。

## 📌 注意事项

- 所有脚本示例均基于本地测试环境编写，若用于其他目标请修改 URL 及判断逻辑。
- 部分脚本（如 `Playwright.py`、`puppeteer_xss.js`）需要安装对应的浏览器驱动和依赖库，请参考脚本内注释。
- 测试环境中的 PHP 文件使用了部分 PHP 7+ 语法，若你的 PHP 版本较低（如 5.x），请将 `??` 运算符替换为 `isset` 的三元表达式（详见 `lab/README.md`）。
- 浏览器安全策略可能影响某些 XSS 的触发（如 DOM 型 XSS 需要对 `location.hash` 进行 `decodeURIComponent` 解码），测试时建议使用多种浏览器或调整安全设置。

## ⚖️ 法律声明

本仓库所有内容（包括笔记、代码、测试环境）**仅供学习和研究使用，严禁用于任何非法目的**。使用者需自行承担因使用不当导致的一切法律责任。请遵守《中华人民共和国网络安全法》及相关法律法规，合理合法地使用网络安全技术。
