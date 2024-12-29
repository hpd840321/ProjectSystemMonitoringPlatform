-- 创建Agent版本表
CREATE TABLE agent_versions (
    id VARCHAR(36) PRIMARY KEY,
    version VARCHAR(20) NOT NULL,
    description TEXT,
    package_url VARCHAR(255) NOT NULL,
    checksum VARCHAR(64) NOT NULL,
    is_latest BOOLEAN NOT NULL DEFAULT false,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
);

-- 创建Agent状态表
CREATE TABLE agent_status (
    agent_id VARCHAR(36) PRIMARY KEY,
    server_id VARCHAR(36) NOT NULL REFERENCES servers(id),
    version VARCHAR(20) NOT NULL,
    status VARCHAR(20) NOT NULL, -- online/offline/updating
    last_heartbeat TIMESTAMP NOT NULL,
    system_info JSONB,
    metrics JSONB,
    error TEXT,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
);

-- 创建Agent更新任务表
CREATE TABLE agent_update_tasks (
    id VARCHAR(36) PRIMARY KEY,
    agent_id VARCHAR(36) NOT NULL,
    from_version VARCHAR(20) NOT NULL,
    to_version VARCHAR(20) NOT NULL,
    status VARCHAR(20) NOT NULL, -- pending/running/success/failed
    error TEXT,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
); 