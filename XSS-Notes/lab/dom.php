<!DOCTYPE html>
<html>
<head>
    <title>DOM 型 XSS</title>
</head>
<body>
    <h1>DOM 型 XSS</h1>
    <p>当前 URL 片段 (hash) 将插入到页面中：</p >
    <div id="output"></div>
    <script>
        var rawHash = location.hash.slice(1);
        // 先解码百分号编码的字符串
        var hash = decodeURIComponent(rawHash);
        document.getElementById('output').innerHTML = hash; 
    </script>
    <p>尝试访问 <code>#&lt;img src=x onerror=alert(1)&gt;</code></p >
    <p>或者利用 <code>#&lt;svg onload=alert(1)&gt;</code></p >
</body>
</html>