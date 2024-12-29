-- 租户表
CREATE TABLE tenants (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    code VARCHAR(50) NOT NULL UNIQUE,  -- 租户唯一标识符
    status VARCHAR(20) NOT NULL DEFAULT 'active',  -- active, suspended, deleted
    max_users INTEGER,  -- 最大用户数限制
    max_projects INTEGER,  -- 最大项目数限制
    max_servers INTEGER,  -- 最大服务器数限制
    settings JSONB,  -- 租户特定设置
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 用户-租户关联表
CREATE TABLE user_tenants (
    user_id INTEGER REFERENCES users(id),
    tenant_id INTEGER REFERENCES tenants(id),
    role VARCHAR(50) NOT NULL,  -- owner, admin, member
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, tenant_id)
);

-- 修改现有表，添加租户关联
ALTER TABLE projects ADD COLUMN tenant_id INTEGER REFERENCES tenants(id);
ALTER TABLE servers ADD COLUMN tenant_id INTEGER REFERENCES tenants(id);
ALTER TABLE alert_rules ADD COLUMN tenant_id INTEGER REFERENCES tenants(id);
ALTER TABLE backup_configs ADD COLUMN tenant_id INTEGER REFERENCES tenants(id);
ALTER TABLE notification_channels ADD COLUMN tenant_id INTEGER REFERENCES tenants(id);

-- 创建租户隔离视图
CREATE OR REPLACE VIEW v_tenant_projects AS
SELECT p.*, t.name as tenant_name
FROM projects p
JOIN tenants t ON p.tenant_id = t.id;

CREATE OR REPLACE VIEW v_tenant_servers AS
SELECT s.*, t.name as tenant_name
FROM servers s
JOIN tenants t ON s.tenant_id = t.id; 