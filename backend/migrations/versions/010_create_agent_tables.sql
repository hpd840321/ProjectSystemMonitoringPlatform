-- 创建Agent表
CREATE TABLE agents (
    id VARCHAR(36) PRIMARY KEY,
    server_id VARCHAR(36) NOT NULL,
    version VARCHAR(20) NOT NULL,
    status VARCHAR(20) NOT NULL,  -- online/offline/error
    last_heartbeat TIMESTAMP,
    config JSONB NOT NULL,        -- Agent配置
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    FOREIGN KEY (server_id) REFERENCES servers(id) ON DELETE CASCADE
);

-- 创建Agent版本表
CREATE TABLE agent_versions (
    id VARCHAR(36) PRIMARY KEY,
    version VARCHAR(20) NOT NULL UNIQUE,
    file_path VARCHAR(500) NOT NULL,  -- 安装包路径
    checksum VARCHAR(64) NOT NULL,    -- SHA256校验和
    description TEXT,
    is_latest BOOLEAN NOT NULL DEFAULT false,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
);

-- 创建Agent升级任务表
CREATE TABLE agent_upgrade_tasks (
    id VARCHAR(36) PRIMARY KEY,
    agent_id VARCHAR(36) NOT NULL,
    from_version VARCHAR(20) NOT NULL,
    to_version VARCHAR(20) NOT NULL,
    status VARCHAR(20) NOT NULL,  -- pending/running/success/failed
    error TEXT,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    FOREIGN KEY (agent_id) REFERENCES agents(id) ON DELETE CASCADE
);

-- 创建索引
CREATE INDEX idx_agents_server_id ON agents(server_id);
CREATE INDEX idx_agents_status ON agents(status);
CREATE INDEX idx_agent_versions_version ON agent_versions(version);
CREATE INDEX idx_agent_upgrade_tasks_agent_id ON agent_upgrade_tasks(agent_id); 