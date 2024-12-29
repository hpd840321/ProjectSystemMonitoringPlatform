-- 创建告警级别表
CREATE TABLE alert_levels (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    description TEXT,
    color VARCHAR(7) NOT NULL,  -- 颜色代码，如 #FF0000
    priority INTEGER NOT NULL,   -- 优先级，数字越小优先级越高
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
);

-- 创建通知渠道表
CREATE TABLE notification_channels (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    type VARCHAR(20) NOT NULL,  -- email/webhook/sms
    config JSONB NOT NULL,      -- 渠道配置
    enabled BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
);

-- 创建告警级别-通知渠道关联表
CREATE TABLE alert_level_channels (
    level_id VARCHAR(36) REFERENCES alert_levels(id),
    channel_id VARCHAR(36) REFERENCES notification_channels(id),
    PRIMARY KEY (level_id, channel_id)
);

-- 插入默认告警级别
INSERT INTO alert_levels (id, name, description, color, priority, created_at, updated_at)
VALUES
    ('critical', '严重', '需要立即处理的严重问题', '#FF0000', 1, NOW(), NOW()),
    ('warning', '警告', '需要关注的潜在问题', '#FFA500', 2, NOW(), NOW()),
    ('info', '信息', '一般提示信息', '#0000FF', 3, NOW(), NOW()); 