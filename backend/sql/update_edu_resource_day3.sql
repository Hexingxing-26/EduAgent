ALTER TABLE edu_resource ADD COLUMN generate_progress TINYINT DEFAULT 0 COMMENT '生成进度0-100';
ALTER TABLE edu_resource ADD COLUMN task_id VARCHAR(100) COMMENT 'AI生成任务唯一标识';
