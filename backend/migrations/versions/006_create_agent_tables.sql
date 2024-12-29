-- Agent基础信息表
CREATE TABLE agents (
    id SERIAL PRIMARY KEY,
    agent_id VARCHAR(64) UNIQUE NOT NULL,
    hostname VARCHAR(255) NOT NULL,
    ip_address VARCHAR(39) NOT NULL,
    system_info JSONB,
    status VARCHAR(20) NOT NULL,
    last_heartbeat TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Agent配置表
CREATE TABLE agent_configs (
    id SERIAL PRIMARY KEY,
    agent_id VARCHAR(64) REFERENCES agents(agent_id),
    config_type VARCHAR(50) NOT NULL,
    config_data JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Agent插件表
CREATE TABLE agent_plugins (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    version VARCHAR(20) NOT NULL,
    description TEXT,
    entry_point VARCHAR(255) NOT NULL,
    config_schema JSONB,
    enabled BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Agent插件实例表
CREATE TABLE agent_plugin_instances (
    id SERIAL PRIMARY KEY,
    agent_id VARCHAR(64) REFERENCES agents(agent_id),
    plugin_id INTEGER REFERENCES agent_plugins(id),
    config JSONB,
    status VARCHAR(20) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
); 