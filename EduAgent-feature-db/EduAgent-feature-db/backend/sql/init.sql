-- 用户表
CREATE TABLE edu_user (
  id INT PRIMARY KEY AUTO_INCREMENT,
  username VARCHAR(50) NOT NULL UNIQUE,
  password VARCHAR(100) NOT NULL,
  nickname VARCHAR(50),
  major VARCHAR(50),
  create_time DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 对话记录表
CREATE TABLE edu_chat (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    session_id VARCHAR(100),
    content TEXT,
    role VARCHAR(20),
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 学习画像表
CREATE TABLE edu_profile (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT UNIQUE,
    weak_points TEXT,
    learning_json TEXT,
    update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 资源存储表
CREATE TABLE edu_resource (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    resource_type VARCHAR(30),
    content TEXT,
    progress INT DEFAULT 0,
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP
);
