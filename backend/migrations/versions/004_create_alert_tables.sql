-- 创建告警规则表
CREATE TABLE alert_rules (
    id VARCHAR(36) PRIMARY KEY,
    project_id VARCHAR(36) NOT NULL,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    metric_type VARCHAR(20) NOT NULL,
    condition TEXT NOT NULL,
    severity VARCHAR(20) NOT NULL,
    interval INTEGER NOT NULL,
    enabled BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
);

-- 创建告警事件表
CREATE TABLE alert_events (
    id VARCHAR(36) PRIMARY KEY,
    rule_id VARCHAR(36) NOT NULL,
    server_id VARCHAR(36) NOT NULL,
    status VARCHAR(20) NOT NULL,
    severity VARCHAR(20) NOT NULL,
    summary TEXT NOT NULL,
    details JSONB,
    first_occurred_at TIMESTAMP NOT NULL,
    last_occurred_at TIMESTAMP NOT NULL,
    resolved_at TIMESTAMP,
    notification_sent BOOLEAN NOT NULL DEFAULT false,
    FOREIGN KEY (rule_id) REFERENCES alert_rules(id) ON DELETE CASCADE,
    FOREIGN KEY (server_id) REFERENCES servers(id) ON DELETE CASCADE
);

-- 创建通知渠道表
CREATE TABLE notification_channels (
    id VARCHAR(36) PRIMARY KEY,
    project_id VARCHAR(36) NOT NULL,
    name VARCHAR(100) NOT NULL,
    type VARCHAR(20) NOT NULL,
    config JSONB NOT NULL,
    enabled BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
);

-- 创建索引
CREATE INDEX idx_alert_rules_project ON alert_rules(project_id);
CREATE INDEX idx_alert_events_rule ON alert_events(rule_id);
CREATE INDEX idx_alert_events_server ON alert_events(server_id);
CREATE INDEX idx_notification_channels_project ON notification_channels(project_id); 