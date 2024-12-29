-- 创建系统设置表
CREATE TABLE settings (
    id VARCHAR(36) PRIMARY KEY,
    type VARCHAR(20) NOT NULL,  -- system/security/monitor/backup/alert/log
    key VARCHAR(100) NOT NULL UNIQUE,
    value JSONB NOT NULL,
    description TEXT,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
);

-- 创建索引
CREATE INDEX idx_settings_type ON settings(type);
CREATE INDEX idx_settings_key ON settings(key);

-- 插入默认设置
INSERT INTO settings (
    id, type, key, value, description, created_at, updated_at
) VALUES
-- 系统设置
(uuid_generate_v4(), 'system', 'site_name', '"Server Monitor"', '站点名称', NOW(), NOW()),
(uuid_generate_v4(), 'system', 'site_url', '"http://localhost"', '站点URL', NOW(), NOW()),
(uuid_generate_v4(), 'system', 'admin_email', '"admin@example.com"', '管理员邮箱', NOW(), NOW()),

-- 安全设置
(uuid_generate_v4(), 'security', 'password_min_length', '8', '密码最小长度', NOW(), NOW()),
(uuid_generate_v4(), 'security', 'password_expire_days', '90', '密码过期天数', NOW(), NOW()),
(uuid_generate_v4(), 'security', 'session_timeout', '30', '会话超时时间(分钟)', NOW(), NOW()),
(uuid_generate_v4(), 'security', 'allowed_ips', '[]', '允许访问的IP列表', NOW(), NOW()),

-- 监控设置
(uuid_generate_v4(), 'monitor', 'metric_retention_days', '30', '监控数据保留天数', NOW(), NOW()),
(uuid_generate_v4(), 'monitor', 'metric_collect_interval', '60', '监控数据采集间隔(秒)', NOW(), NOW()),

-- 备份设置
(uuid_generate_v4(), 'backup', 'backup_retention_days', '7', '备份保留天数', NOW(), NOW()),
(uuid_generate_v4(), 'backup', 'backup_max_size', '1073741824', '备份最大大小(字节)', NOW(), NOW()),

-- 告警设置
(uuid_generate_v4(), 'alert', 'alert_check_interval', '60', '告警检查间隔(秒)', NOW(), NOW()),
(uuid_generate_v4(), 'alert', 'alert_max_retry', '3', '告警通知重试次数', NOW(), NOW()),

-- 日志设置
(uuid_generate_v4(), 'log', 'log_retention_days', '30', '日志保留天数', NOW(), NOW()),
(uuid_generate_v4(), 'log', 'log_max_size', '104857600', '日志最大大小(字节)', NOW(), NOW()); 