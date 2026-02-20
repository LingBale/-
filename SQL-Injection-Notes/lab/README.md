# SQL 注入测试环境搭建指南

## 环境要求
- Web 服务器（Apache / Nginx） + PHP（5.6+，开启 PDO 扩展）
- MySQL / MariaDB
- Python 3.6+（用于运行爆破脚本）

## 文件说明
- `SQL-Injection.php`：存在 SQL 注入漏洞的测试页面
- `init.sql`：数据库初始化脚本

## 搭建步骤
1. 将 `SQL-Injection.php` 放到 Web 服务器的根目录（如 `htdocs` 或 `www`）。
2. 在 MySQL 中执行 `init.sql` 创建数据库和表：
   - 可以使用 Navicat、phpMyAdmin 或命令行：`mysql -u root -p < init.sql`
   - 默认数据库密码为 `root`（如不一致请修改 `SQL-Injection.php` 中的 `$pass` 变量）。
3. 确保 Web 服务器已启动，访问 `http://localhost/SQL-Injection.php?id=1` 应看到 `User: admin - admin123`。
4. 访问 `http://localhost/SQL-Injection.php?id=1'` 应看到 SQL 报错，说明注入点存在。

## 注意事项
⚠️ **此文件包含安全漏洞，仅限本地学习使用，严禁部署到公网！**
