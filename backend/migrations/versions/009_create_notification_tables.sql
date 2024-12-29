-- 通知渠道表
CREATE TABLE notification_channels (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    type VARCHAR(20) NOT NULL,  -- email, webhook, sms, etc.
    config JSONB NOT NULL,      -- 不同类型的配置信息
    enabled BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 告警规则和通知渠道的关联表
CREATE TABLE alert_rule_channels (
    alert_rule_id INTEGER REFERENCES alert_rules(id),
    channel_id INTEGER REFERENCES notification_channels(id),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (alert_rule_id, channel_id)
);

-- 告警通知记录表
CREATE TABLE alert_notifications (
    id SERIAL PRIMARY KEY,
    alert_id INTEGER REFERENCES alerts(id),
    channel_id INTEGER REFERENCES notification_channels(id),
    status VARCHAR(20) NOT NULL,  -- pending, sent, failed
    error_message TEXT,
    sent_at TIMESTAMP,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
); 