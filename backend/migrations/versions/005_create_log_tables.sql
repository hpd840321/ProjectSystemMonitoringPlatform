-- 创建日志表
CREATE TABLE logs (
    id VARCHAR(36) PRIMARY KEY,
    server_id VARCHAR(36) NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    level VARCHAR(20) NOT NULL,
    message TEXT NOT NULL,
    source VARCHAR(50) NOT NULL,
    metadata JSONB,
    raw TEXT NOT NULL,
    FOREIGN KEY (server_id) REFERENCES servers(id) ON DELETE CASCADE
);

-- 转换为超表
SELECT create_hypertable('logs', 'timestamp');

-- 创建索引
CREATE INDEX idx_logs_server ON logs(server_id);
CREATE INDEX idx_logs_level ON logs(level);
CREATE INDEX idx_logs_source ON logs(source);
CREATE INDEX idx_logs_timestamp ON logs(timestamp DESC);

-- 创建保留策略
SELECT add_retention_policy('logs', INTERVAL '30 days'); 