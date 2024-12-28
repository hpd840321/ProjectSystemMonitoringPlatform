-- 创建监控指标表
CREATE TABLE metrics (
    server_id VARCHAR(36) NOT NULL,
    metric_type VARCHAR(20) NOT NULL,
    value DOUBLE PRECISION NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    labels JSONB,
    FOREIGN KEY (server_id) REFERENCES servers(id) ON DELETE CASCADE
);

-- 转换为超表
SELECT create_hypertable('metrics', 'timestamp');

-- 创建索引
CREATE INDEX idx_metrics_server ON metrics(server_id, metric_type);
CREATE INDEX idx_metrics_timestamp ON metrics(timestamp DESC);

-- 创建压缩策略
SELECT add_compression_policy('metrics', INTERVAL '7 days');

-- 创建保留策略
SELECT add_retention_policy('metrics', INTERVAL '30 days'); 