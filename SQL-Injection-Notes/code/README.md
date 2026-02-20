# SQL 注入 Python 脚本集

本目录包含针对本地测试环境 `SQL-Injection.php` 编写的各类注入脚本，按功能分类。

## 📁 文件说明

### 基础脚本（可直接运行）
- `bool_dbname.py`：布尔盲注爆破数据库名
- `bool_tables.py`：布尔盲注爆破表名  
- `bool_columns.py`：布尔盲注爆破字段名
- `bool_users_passwords.py`：布尔盲注爆破用户名和密码
- `time_dbname.py`：时间盲注爆破数据库名
- `time_tables.py`：时间盲注爆破表名
- `time_columns.py`：时间盲注爆破字段名
- `time_users_passwords.py`：时间盲注爆破用户名和密码

✅ **运行条件**：
- 本地 Web 环境已启动（Apache + MySQL）
- `SQL-Injection.php` 可正常访问
- 数据库已用 `init.sql` 初始化
- 安装依赖：`pip install requests`

---

### 高级拓展脚本（需特定配置）

#### `拓展_bool_multithread_dbname.py`
多线程布尔盲注爆破数据库名，演示并发加速。

✅ **运行条件**：同基础脚本，无需额外配置。

---

#### `拓展_bool_resume_dbname.py`
布尔盲注带断点续传功能，中断后可继续爆破。

✅ **运行条件**：同基础脚本，无需额外配置。

---

#### `拓展_bool_proxy_dbname.py`
布尔盲注带代理轮换，用于绕过 IP 封锁。

⚠️ **重要**：
- 脚本中的代理列表是示例，**必须替换为真实可用代理**才能运行。
- 本地测试（`localhost`）**不需要代理**，建议直接使用基础脚本。
- 仅在真实外网目标且需要绕过 IP 封禁时使用此脚本。

---

#### `拓展_tool_ocr_captcha.py`
验证码识别工具，基于 Tesseract OCR。

⚠️ **需要安装额外依赖**：
1. 安装 Tesseract OCR 引擎：
   - Windows：下载 [UB-Mannheim 版本](https://github.com/UB-Mannheim/tesseract/wiki)
   - Linux：`sudo apt install tesseract-ocr`
   - macOS：`brew install tesseract`
2. 安装 Python 库：`pip install pytesseract pillow`
3. 如果 Tesseract 不在系统路径，需在代码中指定路径（见脚本注释）。

---

## 🔧 通用排错指南

1. **基础脚本无法运行**：
   - 检查 `TARGET_URL` 是否正确（默认 `http://localhost/SQL-Injection.php`）
   - 确认 Web 服务是否启动，数据库是否初始化
   - 尝试用浏览器访问 `http://localhost/SQL-Injection.php?id=1` 看是否返回数据

2. **高级脚本报错**：
   - 先确保基础脚本能正常运行
   - 按每个脚本的 ⚠️ 提示检查配置
   - 代理脚本需要真实代理；验证码脚本需要安装 Tesseract

3. **网络请求超时**：
   - 可适当调整脚本顶部的 `TIMEOUT` 和 `SLEEP_TIME` 参数

---

## 📌 注意事项

- 所有脚本均基于**本地测试环境**编写，判断条件为页面包含 `"User:"`（真）或 `"No user found."`（假）
- 如需用于其他目标，请修改 `TARGET_URL` 和判断逻辑
- 时间盲注脚本中 `SLEEP_TIME` 必须大于 `TIMEOUT`，否则无法检测延时
- 高级脚本供学习参考，实际使用时请根据环境调整
