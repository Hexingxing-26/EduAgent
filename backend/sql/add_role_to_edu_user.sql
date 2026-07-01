-- 为现有 edu_user 表新增 role 字段
ALTER TABLE edu_user
ADD COLUMN `role` VARCHAR(20) NOT NULL DEFAULT 'student' COMMENT '用户角色：student学生 / teacher教师 / admin超级管理员';
