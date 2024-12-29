-- 创建备份配置表
CREATE TABLE backup_configs (
    id VARCHAR(36) PRIMARY KEY,
    server_id VARCHAR(36) NOT NULL,
    name VARCHAR(100) NOT NULL,
    type VARCHAR(20) NOT NULL,  -- full/incremental
    schedule VARCHAR(100) NOT NULL,  -- cron表达式
    retention_days INTEGER NOT NULL,
    target_dir VARCHAR(255) NOT NULL,
    enabled BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    FOREIGN KEY (server_id) REFERENCES servers(id) ON DELETE CASCADE
);

-- 创建备份任务表
CREATE TABLE backup_jobs (
    id VARCHAR(36) PRIMARY KEY,
    config_id VARCHAR(36) NOT NULL,
    server_id VARCHAR(36) NOT NULL,
    type VARCHAR(20) NOT NULL,
    status VARCHAR(20) NOT NULL,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP,
    size BIGINT,
    file_path VARCHAR(255),
    error TEXT,
    created_at TIMESTAMP NOT NULL,
    FOREIGN KEY (config_id) REFERENCES backup_configs(id) ON DELETE CASCADE,
    FOREIGN KEY (server_id) REFERENCES servers(id) ON DELETE CASCADE
);

-- 创建索引
CREATE INDEX idx_backup_config_server ON backup_configs(server_id);
CREATE INDEX idx_backup_job_config ON backup_jobs(config_id);
CREATE INDEX idx_backup_job_server ON backup_jobs(server_id);
CREATE INDEX idx_backup_job_status ON backup_jobs(status);
CREATE INDEX idx_backup_job_start ON backup_jobs(start_time DESC); 