<!DOCTYPE html>
<html>
<head>
    <title>反射型 XSS</title>
</head>
<body>
    <h1>反射型 XSS</h1>
    <form method="GET">
        <input type="text" name="input" placeholder="输入内容" value="<?php echo isset($_GET['input']) ? htmlspecialchars($_GET['input'], ENT_QUOTES) : ''; ?>">
        <button type="submit">提交</button>
    </form>
    <hr>
    <?php
    if (isset($_GET['input'])) {
        $input = $_GET['input']; // 漏洞点：直接输出
        // 输出在 HTML 标签内
        echo "<div>输出在 DIV 中：$input</div>";
        // 输出在 input 属性中（未转义）
        echo "<input value='$input' placeholder='属性注入'>";
        // 输出在 script 变量中
        echo "<script>var userInput = '$input'; console.log('Script context:', userInput);</script>";
        // 输出在注释中
        echo "<!-- 注释内容：$input -->";
    }
    ?>
    <p>尝试提交 <code>&lt;script&gt;alert(1)&lt;/script&gt;</code> 或 <code>" onmouseover="alert(1)</code></p >
</body>
</html>