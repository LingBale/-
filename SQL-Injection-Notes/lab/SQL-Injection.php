<?php
// 数据库配置（根据你的环境修改）
$host = 'localhost';
$dbname = 'test';
$user = 'root';      // 你的数据库用户名
$pass = '';

try {
    $pdo = new PDO("mysql:host=$host;dbname=$dbname;charset=utf8", $user, $pass);
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
} catch (PDOException $e) {
    die("数据库连接失败: " . $e->getMessage());
}

// 获取 id 参数（字符型注入点）
$id = isset($_GET['id']) ? $_GET['id'] : '';

// 直接拼接 SQL，存在漏洞
$sql = "SELECT * FROM users WHERE id = '$id'";

// 可选：调试时查看 SQL 语句（取消注释下一行即可显示）
// echo "<!-- SQL: $sql -->";

try {
    $stmt = $pdo->query($sql);
    $results = $stmt->fetchAll(PDO::FETCH_ASSOC);
    
    if (count($results) > 0) {
        foreach ($results as $row) {
            echo "User: " . htmlspecialchars($row['username']) . " - " . htmlspecialchars($row['password']) . "<br>";
        }
    } else {
        // 固定输出，便于布尔盲注判断
        echo "No user found.";
    }
} catch (PDOException $e) {
    // 报错信息直接输出，支持报错注入
    echo "SQL Error: " . $e->getMessage();
}
?>