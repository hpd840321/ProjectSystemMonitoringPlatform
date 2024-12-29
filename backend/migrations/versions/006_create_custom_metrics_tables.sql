-- 创建自定义监控指标表
CREATE TABLE custom_metrics (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    metric_type VARCHAR(20) NOT NULL, -- counter/gauge
    unit VARCHAR(20),
    created_at TIMESTAMP NOT NULL,
    created_by VARCHAR(36) NOT NULL REFERENCES users(id)
);

-- 创建自定义监控数据表
CREATE TABLE custom_metric_values (
    metric_id VARCHAR(36) NOT NULL REFERENCES custom_metrics(id),
    timestamp TIMESTAMP NOT NULL,
    value DOUBLE PRECISION NOT NULL,
    labels JSONB,
    PRIMARY KEY (metric_id, timestamp)
);

-- 创建监控数据聚合配置表
CREATE TABLE metric_aggregations (
    id VARCHAR(36) PRIMARY KEY,
    metric_type VARCHAR(50) NOT NULL, -- system/custom
    metric_id VARCHAR(100) NOT NULL,
    aggregation_type VARCHAR(20) NOT NULL, -- avg/max/min/sum
    interval VARCHAR(20) NOT NULL, -- 1m/5m/1h/1d
    retention_period INTEGER NOT NULL, -- 保留天数
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
);

-- 创建监控数据清理策略表
CREATE TABLE metric_retention_policies (
    id VARCHAR(36) PRIMARY KEY,
    metric_type VARCHAR(50) NOT NULL, -- system/custom
    raw_data_retention INTEGER NOT NULL, -- 原始数据保留天数
    aggregated_data_retention INTEGER NOT NULL, -- 聚合数据保留天数
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
); 