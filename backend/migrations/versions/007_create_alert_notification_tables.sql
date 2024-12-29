-- 创建告警级别配置表
CREATE TABLE alert_levels (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    description TEXT,
    severity INTEGER NOT NULL, -- 严重程度 1-5
    color VARCHAR(20), -- 显示颜色
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
);

-- 创建通知渠道表
CREATE TABLE notification_channels (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    type VARCHAR(20) NOT NULL, -- email/webhook/sms
    config JSONB NOT NULL, -- 渠道配置
    enabled BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
);

-- 创建告警规则-通知渠道关联表
CREATE TABLE alert_rule_channels (
    rule_id VARCHAR(36) NOT NULL REFERENCES alert_rules(id),
    channel_id VARCHAR(36) NOT NULL REFERENCES notification_channels(id),
    created_at TIMESTAMP NOT NULL,
    PRIMARY KEY (rule_id, channel_id)
);

-- 插入默认告警级别
INSERT INTO alert_levels (id, name, description, severity, color, created_at, updated_at)
VALUES
    ('1', '严重', '需要立即处理的严重问题', 1, '#F56C6C', NOW(), NOW()),
    ('2', '警告', '需要关注的重要问题', 2, '#E6A23C', NOW(), NOW()),
    ('3', '注意', '需要留意的一般问题', 3, '#409EFF', NOW(), NOW()); 