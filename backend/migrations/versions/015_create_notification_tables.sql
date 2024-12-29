-- 通知渠道表
CREATE TABLE notification_channels (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    type VARCHAR(20) NOT NULL,  -- email, webhook, sms
    config JSONB NOT NULL,      -- 渠道配置
    enabled BOOLEAN NOT NULL DEFAULT true,
    description TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 通知模板表
CREATE TABLE notification_templates (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    type VARCHAR(20) NOT NULL,  -- alert, backup, system
    subject_template TEXT NOT NULL,
    content_template TEXT NOT NULL,
    description TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 通知记录表
CREATE TABLE notification_logs (
    id SERIAL PRIMARY KEY,
    channel_id INTEGER REFERENCES notification_channels(id),
    template_id INTEGER REFERENCES notification_templates(id),
    event_type VARCHAR(50) NOT NULL,
    recipients TEXT[],
    subject TEXT NOT NULL,
    content TEXT NOT NULL,
    status VARCHAR(20) NOT NULL,  -- success, failed
    error_message TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 插入默认通知模板
INSERT INTO notification_templates (name, type, subject_template, content_template, description) VALUES
-- 告警通知模板
('alert_notification', 'alert', 
 '[{{ alert.severity | upper }}] {{ alert.name }}',
 'Alert Details:
  - Name: {{ alert.name }}
  - Severity: {{ alert.severity }}
  - Status: {{ alert.status }}
  - Resource: {{ alert.resource_name }}
  - Message: {{ alert.message }}
  - Time: {{ alert.created_at }}',
 '告警通知默认模板'),

-- 备份通知模板
('backup_notification', 'backup',
 'Backup {{ backup.status | upper }}: {{ backup.name }}',
 'Backup Details:
  - Name: {{ backup.name }}
  - Status: {{ backup.status }}
  - Size: {{ backup.size }}
  - Path: {{ backup.path }}
  - Started: {{ backup.started_at }}
  - Completed: {{ backup.completed_at }}',
 '备份通知默认模板'),

-- 系统通知模板
('system_notification', 'system',
 'System Notification: {{ event.type }}',
 'System Event Details:
  - Type: {{ event.type }}
  - Message: {{ event.message }}
  - Time: {{ event.timestamp }}',
 '系统通知默认模板'); 