-- 创建备份记录表
CREATE TABLE backups (
    id VARCHAR(36) PRIMARY KEY,
    filename VARCHAR(255) NOT NULL,
    size BIGINT NOT NULL,
    created_at TIMESTAMP NOT NULL,
    created_by VARCHAR(36) NOT NULL REFERENCES users(id),
    status VARCHAR(20) NOT NULL, -- pending/success/failed
    error_message TEXT,
    backup_type VARCHAR(20) NOT NULL, -- full/config/database
    metadata JSONB
);

-- 创建备份恢复记录表
CREATE TABLE backup_restores (
    id VARCHAR(36) PRIMARY KEY,
    backup_id VARCHAR(36) NOT NULL REFERENCES backups(id),
    restored_at TIMESTAMP NOT NULL,
    restored_by VARCHAR(36) NOT NULL REFERENCES users(id),
    status VARCHAR(20) NOT NULL, -- pending/success/failed
    error_message TEXT
); 