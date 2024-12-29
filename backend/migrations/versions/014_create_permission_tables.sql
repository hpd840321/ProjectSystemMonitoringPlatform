-- 角色表
CREATE TABLE roles (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    description TEXT,
    is_system BOOLEAN NOT NULL DEFAULT false,  -- 是否为系统内置角色
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 权限表
CREATE TABLE permissions (
    id SERIAL PRIMARY KEY,
    code VARCHAR(100) NOT NULL UNIQUE,  -- 权限代码，如: project:create
    name VARCHAR(100) NOT NULL,         -- 权限名称
    description TEXT,
    module VARCHAR(50) NOT NULL,        -- 所属模块
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 角色权限关联表
CREATE TABLE role_permissions (
    role_id INTEGER REFERENCES roles(id),
    permission_id INTEGER REFERENCES permissions(id),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (role_id, permission_id)
);

-- 用户角色关联表
CREATE TABLE user_roles (
    user_id INTEGER REFERENCES users(id),
    role_id INTEGER REFERENCES roles(id),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, role_id)
);

-- 插入默认角色
INSERT INTO roles (name, description, is_system) VALUES
('superadmin', '超级管理员，拥有所有权限', true),
('admin', '管理员，拥有大部分管理权限', true),
('operator', '运维人员，拥有操作权限', true),
('viewer', '观察者，仅有查看权限', true);

-- 插入基础权限
INSERT INTO permissions (code, name, description, module) VALUES
-- 项目管理权限
('project:create', '创建项目', '允许创建新项目', 'project'),
('project:read', '查看项目', '允许查看项目信息', 'project'),
('project:update', '更新项目', '允许更新项目信息', 'project'),
('project:delete', '删除项目', '允许删除项目', 'project'),

-- 服务器管理权限
('server:create', '创建服务器', '允许添加新服务器', 'server'),
('server:read', '查看服务器', '允许查看服务器信息', 'server'),
('server:update', '更新服务器', '允许更新服务器信息', 'server'),
('server:delete', '删除服务器', '允许删除服务器', 'server'),

-- 告警管理权限
('alert:create', '创建告警规则', '允许创建告警规则', 'alert'),
('alert:read', '查看告警', '允许查看告警信息', 'alert'),
('alert:update', '更新告警规则', '允许更新告警规则', 'alert'),
('alert:delete', '删除告警规则', '允许���除告警规则', 'alert'),

-- 日志管理权限
('log:read', '查看日志', '允许查看系统日志', 'log'),
('log:export', '导出日志', '允许导出系统日志', 'log'),

-- 备份管理权限
('backup:create', '创建备份', '允许创建系统备份', 'backup'),
('backup:read', '查看备份', '允许查看备份信息', 'backup'),
('backup:restore', '恢复备份', '允许从备份恢复', 'backup'),
('backup:delete', '删除备份', '允许删除备份', 'backup'),

-- 系统设置权限
('settings:read', '查看设置', '允许查看系统设置', 'settings'),
('settings:update', '更新设置', '允许更新系统设置', 'settings'),

-- 用户管理权限
('user:create', '创建用户', '允许创建新用户', 'user'),
('user:read', '查看用户', '允许查看用户信息', 'user'),
('user:update', '更新用户', '允许更新用户信息', 'user'),
('user:delete', '删除用户', '允许删除用户', 'user');

-- 为默认角色分配权限
-- 超级管理员拥有所有权限
INSERT INTO role_permissions (role_id, permission_id)
SELECT 
    (SELECT id FROM roles WHERE name = 'superadmin'),
    id
FROM permissions;

-- 管理员拥有除系统设置外的所有权限
INSERT INTO role_permissions (role_id, permission_id)
SELECT 
    (SELECT id FROM roles WHERE name = 'admin'),
    id
FROM permissions
WHERE module != 'settings';

-- 运维人员拥有操作权限
INSERT INTO role_permissions (role_id, permission_id)
SELECT 
    (SELECT id FROM roles WHERE name = 'operator'),
    id
FROM permissions
WHERE code IN (
    'project:read', 'project:update',
    'server:read', 'server:update',
    'alert:read', 'alert:update',
    'log:read', 'log:export',
    'backup:read', 'backup:create'
);

-- 观察者只有查看权限
INSERT INTO role_permissions (role_id, permission_id)
SELECT 
    (SELECT id FROM roles WHERE name = 'viewer'),
    id
FROM permissions
WHERE code LIKE '%:read'; 