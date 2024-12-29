-- 告警级别表
CREATE TABLE alert_levels (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    description TEXT,
    color VARCHAR(7) NOT NULL,  -- 颜色代码，如 #FF0000
    priority INTEGER NOT NULL,   -- 优先级，数字越小优先级越高
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 添加默认告警级别
INSERT INTO alert_levels (name, description, color, priority) VALUES
    ('critical', '严重告警，需要立即处理', '#FF0000', 1),
    ('error', '错误告警，需要尽快处理', '#FFA500', 2),
    ('warning', '警告信息，需要关注', '#FFFF00', 3),
    ('info', '普通信息，可稍后处理', '#00FF00', 4);

-- 修改告警表，添加级别关联
ALTER TABLE alerts ADD COLUMN level_id INTEGER REFERENCES alert_levels(id);
UPDATE alerts SET level_id = (SELECT id FROM alert_levels WHERE name = 'info');
ALTER TABLE alerts ALTER COLUMN level_id SET NOT NULL; 