-- 服务器基础信息表
CREATE TABLE servers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    hostname VARCHAR(255) NOT NULL,
    ip_address VARCHAR(39) NOT NULL,
    os_type VARCHAR(50),
    os_version VARCHAR(50),
    cpu_cores INTEGER,
    memory_size BIGINT,
    disk_size BIGINT,
    status VARCHAR(20) NOT NULL DEFAULT 'inactive',
    agent_version VARCHAR(50),
    last_seen_at TIMESTAMP,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 服务器分组表
CREATE TABLE server_groups (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 服务器和分组的关联表
CREATE TABLE server_group_relations (
    server_id INTEGER REFERENCES servers(id),
    group_id INTEGER REFERENCES server_groups(id),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (server_id, group_id)
); 