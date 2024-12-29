-- 创建Agent表
CREATE TABLE agents (
    id VARCHAR(36) PRIMARY KEY,
    server_id VARCHAR(36) NOT NULL,
    version VARCHAR(10) NOT NULL,
    status VARCHAR(20) NOT NULL,
    last_heartbeat TIMESTAMP NOT NULL,
    config JSONB NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    FOREIGN KEY (server_id) REFERENCES servers(id) ON DELETE CASCADE
);

-- 创建Agent更新包表
CREATE TABLE agent_updates (
    id VARCHAR(36) PRIMARY KEY,
    version VARCHAR(10) NOT NULL,
    file_path VARCHAR(255) NOT NULL,
    checksum VARCHAR(64) NOT NULL,
    release_notes TEXT,
    created_at TIMESTAMP NOT NULL
);

-- 创建索引
CREATE INDEX idx_agent_server ON agents(server_id);
CREATE INDEX idx_agent_status ON agents(status);
CREATE INDEX idx_agent_heartbeat ON agents(last_heartbeat);
CREATE INDEX idx_agent_update_version ON agent_updates(version); 