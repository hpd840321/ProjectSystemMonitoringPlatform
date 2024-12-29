-- 资源配额表
CREATE TABLE project_quotas (
    id SERIAL PRIMARY KEY,
    project_id INTEGER REFERENCES projects(id),
    resource_type VARCHAR(50) NOT NULL,  -- 资源类型：server, cpu, memory, disk
    quota_limit INTEGER NOT NULL,        -- 配额限制
    used_amount INTEGER DEFAULT 0,       -- 已使用量
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 资源使用记录表
CREATE TABLE resource_usage (
    id SERIAL PRIMARY KEY,
    project_id INTEGER REFERENCES projects(id),
    resource_type VARCHAR(50) NOT NULL,
    amount INTEGER NOT NULL,             -- 使用量变化
    operation VARCHAR(20) NOT NULL,      -- 操作类型：increase, decrease
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
); 