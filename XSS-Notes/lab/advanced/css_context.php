<!DOCTYPE html>
<html>
<head>
    <title>CSS 上下文注入</title>
    <style>
        .user-bg {
            background: <?php echo $_GET['bg'] ?? 'white'; ?>;
        }
    </style>
</head>
<body>
    <h1>CSS 注入</h1>
    <div class="user-bg" style="height: 100px;">背景颜色可控</div>
    <p>尝试 Payload（仅 IE/旧版）：<code>red; background: url('javascript:alert(1)');</code> 或 <code>expression(alert(1))</code></p >
</body>
</html>