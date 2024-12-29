-- 系统设置表
CREATE TABLE system_settings (
    id SERIAL PRIMARY KEY,
    category VARCHAR(50) NOT NULL,  -- general, email, security, etc.
    key VARCHAR(100) NOT NULL,
    value JSONB NOT NULL,
    description TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(category, key)
);

-- 用户偏好设置表
CREATE TABLE user_preferences (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    key VARCHAR(100) NOT NULL,
    value JSONB NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, key)
);

-- 插入默认系统设置
INSERT INTO system_settings (category, key, value, description) VALUES
-- 常规设置
('general', 'timezone', '"UTC"', '系统默认时区'),
('general', 'date_format', '"YYYY-MM-DD"', '日期格式'),
('general', 'time_format', '"HH:mm:ss"', '时间格式'),

-- 邮件服务器设置
('email', 'smtp_config', '{
    "host": "smtp.example.com",
    "port": 587,
    "username": "",
    "password": "",
    "use_tls": true,
    "from_email": "monitor@example.com",
    "from_name": "Server Monitor"
}', '邮件服务器配置'),

-- 安全设置
('security', 'password_policy', '{
    "min_length": 8,
    "require_uppercase": true,
    "require_lowercase": true,
    "require_numbers": true,
    "require_special_chars": true,
    "max_age_days": 90
}', '密码策略'),
('security', 'session_config', '{
    "timeout_minutes": 30,
    "max_sessions_per_user": 3
}', '会话配置'),

-- 告警设置
('alert', 'default_severity_levels', '[
    {"name": "critical", "color": "#ff0000"},
    {"name": "error", "color": "#ffa500"},
    {"name": "warning", "color": "#ffff00"},
    {"name": "info", "color": "#00ff00"}
]', '默认告警级别'),

-- 备份设置
('backup', 'default_paths', '{
    "system": "/backups/system",
    "database": "/backups/database",
    "files": "/backups/files"
}', '默认备份路径'); 