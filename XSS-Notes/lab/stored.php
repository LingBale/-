<?php
$file = 'comments.txt';
// 写入评论
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['comment'])) {
    $comment = $_POST['comment'] . PHP_EOL;
    file_put_contents($file, $comment, FILE_APPEND | LOCK_EX);
    header('Location: stored.php');
    exit;
}
// 读取评论
$comments = file_exists($file) ? file($file) : [];
?>
<!DOCTYPE html>
<html>
<head>
    <title>存储型 XSS (留言板)</title>
</head>
<body>
    <h1>留言板</h1>
    <form method="POST">
        <textarea name="comment" rows="4" cols="50" placeholder="写下你的评论..."></textarea><br>
        <button type="submit">提交</button>
    </form>
    <hr>
    <h2>已有评论</h2>
    <?php foreach ($comments as $c): ?>
        <div><?php echo $c; // 漏洞点：直接输出 ?></div>
    <?php endforeach; ?>
    <p>尝试提交 <code>&lt;img src=x onerror=alert(1)&gt;</code>，刷新页面即可触发。</p >
</body>
</html>