-- 创建日志解析规则表
CREATE TABLE log_parse_rules (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    pattern VARCHAR(500) NOT NULL,  -- 正则表达式
    fields JSONB NOT NULL,          -- 字段映射
    description TEXT,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
);

-- 创建日志采集配置表
CREATE TABLE log_collect_configs (
    id VARCHAR(36) PRIMARY KEY,
    server_id VARCHAR(36) NOT NULL,
    name VARCHAR(100) NOT NULL,
    path VARCHAR(500) NOT NULL,     -- 日志文件路径
    rule_id VARCHAR(36) NOT NULL,   -- 解析规则ID
    enabled BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    FOREIGN KEY (server_id) REFERENCES servers(id) ON DELETE CASCADE,
    FOREIGN KEY (rule_id) REFERENCES log_parse_rules(id)
);

-- 插入默认解析规则
INSERT INTO log_parse_rules (id, name, pattern, fields, description, created_at, updated_at)
VALUES
(
    uuid_generate_v4(),
    'Nginx Access Log',
    '^(?P<remote_addr>[\d.]+) - (?P<remote_user>[^ ]*) \[(?P<time_local>.*?)\] "(?P<request>.*?)" (?P<status>\d+) (?P<body_bytes_sent>\d+) "(?P<http_referer>.*?)" "(?P<http_user_agent>.*?)"$',
    '{
        "remote_addr": "string",
        "remote_user": "string",
        "time_local": "datetime",
        "request": "string",
        "status": "integer",
        "body_bytes_sent": "integer",
        "http_referer": "string",
        "http_user_agent": "string"
    }',
    'Nginx访问日志默认格式',
    NOW(),
    NOW()
),
(
    uuid_generate_v4(),
    'Apache Access Log',
    '^(?P<host>[\d.]+) (?P<identd>[^ ]*) (?P<user>[^ ]*) \[(?P<time>.*?)\] "(?P<request>.*?)" (?P<status>\d+) (?P<size>\d+)$',
    '{
        "host": "string",
        "identd": "string",
        "user": "string",
        "time": "datetime",
        "request": "string",
        "status": "integer",
        "size": "integer"
    }',
    'Apache访问日志通用格式',
    NOW(),
    NOW()
); 