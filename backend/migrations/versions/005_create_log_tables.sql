-- 创建日志表
CREATE TABLE logs (
    id VARCHAR(36) PRIMARY KEY,
    server_id VARCHAR(36) NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    level VARCHAR(20) NOT NULL,
    message TEXT NOT NULL,
    source VARCHAR(50) NOT NULL,
    metadata JSONB,
    raw TEXT NOT NULL,
    FOREIGN KEY (server_id) REFERENCES servers(id) ON DELETE CASCADE
);

-- 转换为超表
SELECT create_hypertable('logs', 'timestamp');

-- 创建索引
CREATE INDEX idx_logs_server ON logs(server_id);
CREATE INDEX idx_logs_level ON logs(level);
CREATE INDEX idx_logs_source ON logs(source);
CREATE INDEX idx_logs_timestamp ON logs(timestamp DESC);

-- 创建保留策略
SELECT add_retention_policy('logs', INTERVAL '30 days'); 

-- 创建日志配置表
CREATE TABLE log_configs (
    id VARCHAR(36) PRIMARY KEY,
    server_id VARCHAR(36) NOT NULL,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    file_path VARCHAR(255) NOT NULL,
    format VARCHAR(20) NOT NULL,  -- syslog/json/nginx/apache/custom
    pattern TEXT,  -- 自定义格式的正则表达式
    fields JSONB,  -- 字段映射
    enabled BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    FOREIGN KEY (server_id) REFERENCES servers(id) ON DELETE CASCADE
);

-- 创建日志条目表
CREATE TABLE log_entries (
    id VARCHAR(36) PRIMARY KEY,
    config_id VARCHAR(36) NOT NULL,
    server_id VARCHAR(36) NOT NULL,
    level VARCHAR(20) NOT NULL,  -- debug/info/warning/error/critical
    message TEXT NOT NULL,
    timestamp TIMESTAMP NOT NULL,  -- 日志产生时间
    fields JSONB NOT NULL,  -- 解析后的字段
    raw TEXT NOT NULL,  -- 原始日志行
    created_at TIMESTAMP NOT NULL,  -- 采集时间
    FOREIGN KEY (config_id) REFERENCES log_configs(id) ON DELETE CASCADE,
    FOREIGN KEY (server_id) REFERENCES servers(id) ON DELETE CASCADE
);

-- 创建索引
CREATE INDEX idx_log_config_server ON log_configs(server_id);
CREATE INDEX idx_log_entry_config ON log_entries(config_id);
CREATE INDEX idx_log_entry_server ON log_entries(server_id);
CREATE INDEX idx_log_entry_level ON log_entries(level);
CREATE INDEX idx_log_entry_timestamp ON log_entries(timestamp);
CREATE INDEX idx_log_entry_created ON log_entries(created_at);

-- 创建全文搜索索引
CREATE INDEX idx_log_entry_message_gin ON log_entries USING gin(to_tsvector('chinese', message));
CREATE INDEX idx_log_entry_raw_gin ON log_entries USING gin(to_tsvector('chinese', raw));

-- 创建分区表(按时间分区)
CREATE TABLE log_entries_partitioned (
    LIKE log_entries INCLUDING ALL
) PARTITION BY RANGE (timestamp);

-- 创建初始分区(按月分区)
CREATE TABLE log_entries_y2024m01 PARTITION OF log_entries_partitioned
    FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');
CREATE TABLE log_entries_y2024m02 PARTITION OF log_entries_partitioned
    FOR VALUES FROM ('2024-02-01') TO ('2024-03-01');
CREATE TABLE log_entries_y2024m03 PARTITION OF log_entries_partitioned
    FOR VALUES FROM ('2024-03-01') TO ('2024-04-01');

-- 创建触发器函数(自动创建新分区)
CREATE OR REPLACE FUNCTION create_log_partition()
RETURNS TRIGGER AS $$
DECLARE
    partition_date DATE;
    partition_name TEXT;
    start_date TEXT;
    end_date TEXT;
BEGIN
    partition_date := date_trunc('month', NEW.timestamp);
    partition_name := 'log_entries_y' || 
        to_char(partition_date, 'YYYY') ||
        'm' || to_char(partition_date, 'MM');
    
    start_date := to_char(partition_date, 'YYYY-MM-DD');
    end_date := to_char(partition_date + INTERVAL '1 month', 'YYYY-MM-DD');
    
    -- 检查分区是否存在
    IF NOT EXISTS (
        SELECT 1
        FROM pg_class c
        JOIN pg_namespace n ON n.oid = c.relnamespace
        WHERE c.relname = partition_name
    ) THEN
        -- 创建新分区
        EXECUTE format(
            'CREATE TABLE %I PARTITION OF log_entries_partitioned
            FOR VALUES FROM (%L) TO (%L)',
            partition_name, start_date, end_date
        );
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- 创建触发器
CREATE TRIGGER log_partition_trigger
    BEFORE INSERT ON log_entries_partitioned
    FOR EACH ROW
    EXECUTE FUNCTION create_log_partition();

-- 创建清理函数
CREATE OR REPLACE FUNCTION cleanup_old_log_partitions(days INTEGER)
RETURNS void AS $$
DECLARE
    partition_name TEXT;
BEGIN
    FOR partition_name IN
        SELECT tablename
        FROM pg_tables
        WHERE tablename LIKE 'log_entries_y%'
        AND to_date(
            substring(tablename from 'y(\d{4})m(\d{2})'),
            'YYYYMM'
        ) < current_date - days
    LOOP
        EXECUTE format('DROP TABLE %I', partition_name);
    END LOOP;
END;
$$ LANGUAGE plpgsql; 