-- 创建测试数据库（如果不存在）
CREATE DATABASE IF NOT EXISTS test;
USE test;

-- 删除旧表（避免冲突）
DROP TABLE IF EXISTS users;

-- 创建 users 表
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(50) NOT NULL
);

-- 插入测试数据
INSERT INTO users (username, password) VALUES
('admin', 'admin123'),
('user1', 'pass1'),
('user2', 'pass2'),
('test', 'testpass');