-- 创建Agent指标表
CREATE TABLE agent_metrics (
    id VARCHAR(36) PRIMARY KEY,
    agent_id VARCHAR(36) NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    cpu_percent FLOAT NOT NULL,
    memory_percent FLOAT NOT NULL,
    disk_usage FLOAT NOT NULL,
    network_in BIGINT NOT NULL,
    network_out BIGINT NOT NULL,
    created_at TIMESTAMP NOT NULL,
    FOREIGN KEY (agent_id) REFERENCES agents(id) ON DELETE CASCADE
);

-- 创建Agent指标聚合表(按小时)
CREATE TABLE agent_metrics_hourly (
    id VARCHAR(36) PRIMARY KEY,
    agent_id VARCHAR(36) NOT NULL,
    hour TIMESTAMP NOT NULL,
    cpu_percent_avg FLOAT NOT NULL,
    cpu_percent_max FLOAT NOT NULL,
    memory_percent_avg FLOAT NOT NULL,
    memory_percent_max FLOAT NOT NULL,
    disk_usage_avg FLOAT NOT NULL,
    disk_usage_max FLOAT NOT NULL,
    network_in_total BIGINT NOT NULL,
    network_out_total BIGINT NOT NULL,
    created_at TIMESTAMP NOT NULL,
    FOREIGN KEY (agent_id) REFERENCES agents(id) ON DELETE CASCADE
);

-- 创建索引
CREATE INDEX idx_agent_metrics_agent_id_timestamp ON agent_metrics(agent_id, timestamp);
CREATE INDEX idx_agent_metrics_hourly_agent_id_hour ON agent_metrics_hourly(agent_id, hour); 