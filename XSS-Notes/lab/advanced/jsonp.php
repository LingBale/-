<?php
// 模拟 JSONP 接口
$callback = $_GET['callback'] ?? 'callback';
$data = ['name' => 'XSS', 'message' => 'Hello'];
header('Content-Type: application/javascript');
echo $callback . '(' . json_encode($data) . ');';
?>