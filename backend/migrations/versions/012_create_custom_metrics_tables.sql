-- 创建自定义监控指标表
CREATE TABLE custom_metrics (
    id VARCHAR(36) PRIMARY KEY,
    project_id VARCHAR(36) NOT NULL,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    metric_type VARCHAR(20) NOT NULL,  -- counter/gauge
    unit VARCHAR(20),                  -- 单位(如: bytes/seconds)
    labels JSONB,                      -- 标签配置
    collection_script TEXT NOT NULL,    -- 采集脚本
    interval INTEGER NOT NULL,          -- 采集间隔(秒)
    enabled BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
);

-- 创建自定义指标数据表
CREATE TABLE custom_metric_values (
    id VARCHAR(36) PRIMARY KEY,
    metric_id VARCHAR(36) NOT NULL,
    server_id VARCHAR(36) NOT NULL,
    value DOUBLE PRECISION NOT NULL,
    labels JSONB,                      -- 实际标签值
    timestamp TIMESTAMP NOT NULL,
    FOREIGN KEY (metric_id) REFERENCES custom_metrics(id) ON DELETE CASCADE,
    FOREIGN KEY (server_id) REFERENCES servers(id) ON DELETE CASCADE
);

-- 创建指标聚合���置表
CREATE TABLE metric_aggregations (
    id VARCHAR(36) PRIMARY KEY,
    metric_id VARCHAR(36) NOT NULL,    -- 基础指标或自定义指标ID
    name VARCHAR(100) NOT NULL,
    description TEXT,
    aggregation_type VARCHAR(20) NOT NULL,  -- avg/max/min/sum
    interval VARCHAR(20) NOT NULL,          -- 聚合间隔(如: 5m/1h/1d)
    retention_days INTEGER NOT NULL,        -- 保留天数
    enabled BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    FOREIGN KEY (metric_id) REFERENCES custom_metrics(id) ON DELETE CASCADE
);

-- 创建聚合数据表
CREATE TABLE aggregated_metrics (
    id VARCHAR(36) PRIMARY KEY,
    aggregation_id VARCHAR(36) NOT NULL,
    server_id VARCHAR(36) NOT NULL,
    value DOUBLE PRECISION NOT NULL,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP NOT NULL,
    FOREIGN KEY (aggregation_id) REFERENCES metric_aggregations(id) ON DELETE CASCADE,
    FOREIGN KEY (server_id) REFERENCES servers(id) ON DELETE CASCADE
);

-- 创建指标清理策略表
CREATE TABLE metric_retention_policies (
    id VARCHAR(36) PRIMARY KEY,
    metric_id VARCHAR(36) NOT NULL,
    raw_data_retention_days INTEGER NOT NULL,  -- 原始数据保留天数
    aggregated_data_retention_days INTEGER NOT NULL,  -- 聚合数据保留天数
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    FOREIGN KEY (metric_id) REFERENCES custom_metrics(id) ON DELETE CASCADE
);

-- 创建索引
CREATE INDEX idx_custom_metric_values_timestamp ON custom_metric_values(timestamp);
CREATE INDEX idx_custom_metric_values_metric_server ON custom_metric_values(metric_id, server_id);
CREATE INDEX idx_aggregated_metrics_time ON aggregated_metrics(start_time, end_time); 