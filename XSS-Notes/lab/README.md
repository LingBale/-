# XSS 本地测试环境搭建指南

本目录包含一个完整的 XSS 漏洞测试平台，涵盖反射型、存储型、DOM 型以及多种高级场景（JavaScript 上下文、属性注入、CSS 注入、JSONP 回调等）。

## 环境要求

- Web 服务器（Apache / Nginx）+ PHP（5.6 或 7+，推荐 7+）
- 文件系统可写（用于 `comments.txt` 存储评论）
- 浏览器（建议 Chrome、Firefox、Edge 等现代浏览器）

## 文件说明

| 文件名 | 作用 |
|-------|------|
| `index.php` | 测试平台导航页 |
| `reflective.php` | 反射型 XSS（HTML 元素、属性、JS 变量、注释等上下文） |
| `stored.php` | 存储型 XSS（基于文件存储的留言板） |
| `dom.php` | DOM 型 XSS（利用 `location.hash` 注入） |
| `advanced/js_context.php` | JavaScript 字符串上下文注入 |
| `advanced/attribute.php` | HTML 属性注入 |
| `advanced/css_context.php` | CSS 上下文注入（expression、javascript: 等） |
| `advanced/jsonp.php` | JSONP 回调型 XSS |
| `comments.txt` | 存储型留言文件（自动创建） |

## 搭建步骤

1. 将整个 `lab/` 目录（或所有文件）复制到 Web 服务器的根目录下（如 Apache 的 `htdocs` 或 `www` 文件夹），例如命名为 `xss-lab`。
2. 确保 PHP 环境正常运行，且 Web 服务器对当前目录有写入权限（以便 `comments.txt` 可被创建）。
3. 访问测试平台导航页：`http://localhost/xss-lab/index.php`
4. 点击链接进入各个漏洞页面，在输入框或 URL 中尝试 XSS Payload。

## 注意事项

⚠️ **此环境包含真实的安全漏洞，仅限本地学习使用，严禁部署到公网！**

- **PHP 版本兼容性**：部分文件（如 `attribute.php`、`css_context.php`、`jsonp.php`）使用了 PHP 7+ 的 `??` 运算符。若你的 PHP 版本低于 7，请将 `??` 替换为 `isset` 的三元表达式，例如：
  ```php
  // 原写法
  $color = $_GET['color'] ?? 'black';
  // 改为
  $color = isset($_GET['color']) ? $_GET['color'] : 'black';
