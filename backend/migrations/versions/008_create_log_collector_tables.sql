-- 创建日志采集配置表
CREATE TABLE log_collectors (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    type VARCHAR(20) NOT NULL, -- file/syslog/journald
    config JSONB NOT NULL, -- 采集配置
    enabled BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
);

-- 创建日志解析规则表
CREATE TABLE log_parsers (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    pattern TEXT NOT NULL, -- 解析正则表达式
    fields JSONB NOT NULL, -- 字段映射
    sample TEXT, -- 样例日志
    enabled BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
);

-- 创建采集器-解析器关联表
CREATE TABLE collector_parsers (
    collector_id VARCHAR(36) NOT NULL REFERENCES log_collectors(id),
    parser_id VARCHAR(36) NOT NULL REFERENCES log_parsers(id),
    created_at TIMESTAMP NOT NULL,
    PRIMARY KEY (collector_id, parser_id)
); 