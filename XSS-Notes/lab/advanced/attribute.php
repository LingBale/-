<!DOCTYPE html>
<html>
<head>
    <title>HTML 属性注入</title>
</head>
<body>
    <h1>属性注入</h1>
    <?php
    $color = $_GET['color'] ?? 'black';
    ?>
    <div style="color: <?php echo $color; ?>">这是一段彩色文字（属性中）</div>
    <input type="text" value="<?php echo $color; ?>" placeholder="尝试闭合">
    <p>测试 Payload: <code>" onmouseover="alert(1)</code> 或 <code>red" style="background:url('javascript:alert(1)')</code></p >
</body>
</html>