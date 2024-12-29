-- 存储策略表
CREATE TABLE storage_policies (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    data_type VARCHAR(20) NOT NULL,  -- metrics, logs, alerts, backups
    retention_days INTEGER NOT NULL,  -- 数据保留天数
    compression_enabled BOOLEAN NOT NULL DEFAULT false,
    compression_after_days INTEGER,   -- 多少天后压缩
    backup_enabled BOOLEAN NOT NULL DEFAULT false,
    backup_schedule VARCHAR(50),      -- cron表达式
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 存储策略执行历史
CREATE TABLE storage_policy_executions (
    id SERIAL PRIMARY KEY,
    policy_id INTEGER REFERENCES storage_policies(id),
    action_type VARCHAR(20) NOT NULL,  -- cleanup, compress, backup
    status VARCHAR(20) NOT NULL,       -- running, success, failed
    affected_rows INTEGER,
    error_message TEXT,
    started_at TIMESTAMP NOT NULL,
    completed_at TIMESTAMP,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 插入默认策略
INSERT INTO storage_policies 
(name, data_type, retention_days, compression_enabled, compression_after_days, backup_enabled, backup_schedule)
VALUES
('default_metrics', 'metrics', 90, true, 30, true, '0 0 1 * *'),
('default_logs', 'logs', 30, true, 7, true, '0 0 * * *'),
('default_alerts', 'alerts', 180, false, null, true, '0 0 1 * *'),
('default_backups', 'backups', 365, false, null, false, null); 