<!DOCTYPE html>
<html>
<head>
    <title>XSS 测试平台</title>
    <style>
        body { font-family: Arial; margin: 20px; }
        li { margin: 10px 0; }
    </style>
</head>
<body>
    <h1>XSS 漏洞实践指南</h1>
    <ul>
        <li><a href="reflective.php">反射型 XSS（多种上下文）</a ></li>
        <li><a href="stored.php">存储型 XSS（留言板）</a ></li>
        <li><a href="dom.php">DOM 型 XSS</a ></li>
        <li><a href="advanced/js_context.php">JavaScript 上下文注入</a ></li>
        <li><a href="advanced/attribute.php">HTML 属性注入</a ></li>
        <li><a href="advanced/css_context.php">CSS 上下文注入</a ></li>
        <li><a href="advanced/jsonp.php">JSONP 回调 XSS</a ></li>
    </ul>
    <p>在每个页面中尝试你的 Payload，观察浏览器行为。</p >
</body>
</html>