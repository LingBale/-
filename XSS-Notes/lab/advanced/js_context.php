<!DOCTYPE html>
<html>
<head>
    <title>JavaScript 上下文注入</title>
</head>
<body>
    <h1>JavaScript 上下文</h1>
    <p>输入将直接拼接到 JavaScript 字符串中：</p >
    <form method="GET">
        <input type="text" name="name" placeholder="输入名字">
        <button type="submit">提交</button>
    </form>
    <?php if (isset($_GET['name'])): ?>
        <script>
            var name = '<?php echo $_GET['name']; ?>'; // 漏洞点：未转义
            document.write('<p>Hello, ' + name + '!</p >');
        </script>
        <p>尝试闭合字符串：<code>'</code>, <code>\';alert(1)//</code> 或 <code>\'</code></p >
    <?php endif; ?>
</body>
</html>