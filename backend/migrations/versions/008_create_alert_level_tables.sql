-- 创建告警级别表
CREATE TABLE alert_levels (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    description TEXT,
    color VARCHAR(20) NOT NULL,  -- 显示颜色
    priority INTEGER NOT NULL,   -- 优先级(1-5)
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
);

-- 创建通知渠道表
CREATE TABLE notification_channels (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    type VARCHAR(20) NOT NULL,  -- email/sms/webhook/slack
    config JSONB NOT NULL,      -- 渠道配置
    enabled BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
);

-- 创建告警级别-通知渠道关联表
CREATE TABLE alert_level_channels (
    level_id VARCHAR(36) NOT NULL,
    channel_id VARCHAR(36) NOT NULL,
    PRIMARY KEY (level_id, channel_id),
    FOREIGN KEY (level_id) REFERENCES alert_levels(id) ON DELETE CASCADE,
    FOREIGN KEY (channel_id) REFERENCES notification_channels(id) ON DELETE CASCADE
);

-- 插入默认告警级别
INSERT INTO alert_levels (id, name, description, color, priority, created_at, updated_at)
VALUES
('1', 'Critical', '严重告警', '#FF0000', 1, NOW(), NOW()),
('2', 'Error', '错误告警', '#FFA500', 2, NOW(), NOW()),
('3', 'Warning', '警告', '#FFFF00', 3, NOW(), NOW()),
('4', 'Info', '信息', '#00FF00', 4, NOW(), NOW()),
('5', 'Debug', '调试', '#808080', 5, NOW(), NOW()); 