-- 备份配置表
CREATE TABLE backup_configs (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    type VARCHAR(20) NOT NULL,  -- system, database, files
    target_path TEXT NOT NULL,  -- 备份目标路径
    retention_count INTEGER NOT NULL DEFAULT 7,  -- 保留的备份数量
    schedule VARCHAR(50) NOT NULL,  -- cron表达式
    enabled BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 备份记录表
CREATE TABLE backup_records (
    id SERIAL PRIMARY KEY,
    config_id INTEGER REFERENCES backup_configs(id),
    file_path TEXT NOT NULL,      -- 备份文件路径
    file_size BIGINT NOT NULL,    -- 文件大小(字节)
    status VARCHAR(20) NOT NULL,  -- running, success, failed
    error_message TEXT,
    started_at TIMESTAMP NOT NULL,
    completed_at TIMESTAMP,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 插入默认配置
INSERT INTO backup_configs 
(name, type, target_path, retention_count, schedule)
VALUES
('system_backup', 'system', '/backups/system', 7, '0 0 * * 0'),
('database_backup', 'database', '/backups/database', 14, '0 0 * * *'),
('files_backup', 'files', '/backups/files', 7, '0 0 * * *'); 