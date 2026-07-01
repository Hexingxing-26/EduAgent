-- 用户表
CREATE TABLE edu_user (
  id INT PRIMARY KEY AUTO_INCREMENT,
  username VARCHAR(50) NOT NULL UNIQUE,
  password VARCHAR(100) NOT NULL,
  nickname VARCHAR(50),
  major VARCHAR(50),
  role VARCHAR(20) NOT NULL DEFAULT 'student' COMMENT '用户角色：student学生 / teacher教师 / admin超级管理员',
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

-- 学生画像表（根据 student_data.json 格式）
CREATE TABLE students (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL COMMENT '姓名',
    age INT COMMENT '年龄',
    major VARCHAR(100) COMMENT '专业',
    course VARCHAR(100) COMMENT '课程',
    study_goal VARCHAR(255) COMMENT '学习目标',
    knowledge_level VARCHAR(50) COMMENT '知识基础',
    learning_preference VARCHAR(50) COMMENT '学习偏好',
    weak_knowledge VARCHAR(255) COMMENT '薄弱知识',
    study_time VARCHAR(50) COMMENT '学习时间',
    raw_json JSON COMMENT '原始 JSON 数据（可选）',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
)
ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 资源存储表
CREATE TABLE edu_resource (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    resource_type VARCHAR(30),
    content TEXT,
    progress INT DEFAULT 0,
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 学习记录表（根据 learning_records.json 格式）
CREATE TABLE learning_records (
    id VARCHAR(64) PRIMARY KEY COMMENT '记录 id，如 RU0001_000',
    user_id VARCHAR(50) COMMENT '用户 id，如 U0001',
    course VARCHAR(200) COMMENT '课程',
    chapter VARCHAR(200) COMMENT '章节',
    score INT COMMENT '得分',
    correct_rate DECIMAL(5,4) COMMENT '正确率（0-1）',
    problems_done INT COMMENT '完成题目数',
    duration_minutes INT COMMENT '持续分钟数',
    study_date DATE COMMENT '学习日期',
    time_slot VARCHAR(20) COMMENT '时间段，如 10:00-12:00',
    raw_json JSON COMMENT '原始 JSON 数据（可选）',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
)
ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
