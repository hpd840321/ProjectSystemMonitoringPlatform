-- 日志源配置表
CREATE TABLE log_sources (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    type VARCHAR(20) NOT NULL,  -- file, syslog, journald, etc.
    config JSONB NOT NULL,      -- 不同类型的配置信息
    enabled BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 日志解析规则表
CREATE TABLE log_parse_rules (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    pattern TEXT NOT NULL,      -- 解析模式（正则表达式）
    fields JSONB NOT NULL,      -- 字段映射配置
    sample TEXT,                -- 示例日志
    enabled BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 日志源和解析规则的关联表
CREATE TABLE log_source_rules (
    source_id INTEGER REFERENCES log_sources(id),
    rule_id INTEGER REFERENCES log_parse_rules(id),
    priority INTEGER NOT NULL,   -- 规则优先级
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (source_id, rule_id)
);

-- 日志数据表（按时间分区）
CREATE TABLE logs (
    id BIGSERIAL PRIMARY KEY,
    source_id INTEGER REFERENCES log_sources(id),
    timestamp TIMESTAMP NOT NULL,
    level VARCHAR(20),
    message TEXT NOT NULL,
    parsed_fields JSONB,        -- 解析后的字段
    metadata JSONB,             -- 元数据（如主机信息等）
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
) PARTITION BY RANGE (timestamp);

-- 创建最近30天的分区
CREATE TABLE logs_recent PARTITION OF logs
    FOR VALUES FROM ('2024-01-01') TO ('2024-12-31');

-- 创建索引
CREATE INDEX idx_logs_timestamp ON logs USING btree (timestamp);
CREATE INDEX idx_logs_source_id ON logs USING btree (source_id);
CREATE INDEX idx_logs_level ON logs USING btree (level);
CREATE INDEX idx_logs_parsed_fields ON logs USING gin (parsed_fields); 