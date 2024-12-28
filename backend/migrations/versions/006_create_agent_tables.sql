-- 创建Agent表
CREATE TABLE agents (
    id VARCHAR(36) PRIMARY KEY,
    server_id VARCHAR(36) NOT NULL,
    version VARCHAR(10) NOT NULL,
    status VARCHAR(20) NOT NULL,
    hostname VARCHAR(255) NOT NULL,
    ip_address VARCHAR(45) NOT NULL,
    system_info JSONB NOT NULL,
    config JSONB NOT NULL,
    last_heartbeat TIMESTAMP NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    FOREIGN KEY (server_id) REFERENCES servers(id) ON DELETE CASCADE
);

-- 创建Agent指标表
CREATE TABLE agent_metrics (
    agent_id VARCHAR(36) NOT NULL,
    cpu_usage FLOAT NOT NULL,
    memory_usage FLOAT NOT NULL,
    disk_usage JSONB NOT NULL,
    network_io JSONB NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    FOREIGN KEY (agent_id) REFERENCES agents(id) ON DELETE CASCADE
);

-- 转换为超表
SELECT create_hypertable('agent_metrics', 'timestamp');

-- 创建索引
CREATE INDEX idx_agents_server ON agents(server_id);
CREATE INDEX idx_agents_status ON agents(status);
CREATE INDEX idx_agent_metrics_agent ON agent_metrics(agent_id);
CREATE INDEX idx_agent_metrics_timestamp ON agent_metrics(timestamp DESC);

-- 创建保留策略
SELECT add_retention_policy('agent_metrics', INTERVAL '7 days'); 