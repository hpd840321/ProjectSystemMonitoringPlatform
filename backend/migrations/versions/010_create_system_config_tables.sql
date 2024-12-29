-- 创建通知渠道配置表
CREATE TABLE notification_settings (
    id VARCHAR(36) PRIMARY KEY,
    type VARCHAR(20) NOT NULL, -- email/webhook/sms
    name VARCHAR(100) NOT NULL,
    config JSONB NOT NULL,
    enabled BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
);

-- 创建存储策略配置表
CREATE TABLE storage_settings (
    id VARCHAR(36) PRIMARY KEY,
    type VARCHAR(20) NOT NULL, -- local/s3/oss
    name VARCHAR(100) NOT NULL,
    config JSONB NOT NULL,
    is_default BOOLEAN NOT NULL DEFAULT false,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
);

-- 创建数据保留策略表
CREATE TABLE retention_settings (
    id VARCHAR(36) PRIMARY KEY,
    data_type VARCHAR(50) NOT NULL, -- metrics/logs/backups
    retention_days INTEGER NOT NULL,
    compression_enabled BOOLEAN NOT NULL DEFAULT true,
    compression_days INTEGER,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
); 