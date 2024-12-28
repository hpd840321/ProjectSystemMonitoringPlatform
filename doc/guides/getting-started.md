# 快速入门指南

## 简介

这是一个基于Python+Vue3的项目状态监控系统，提供实时数据展示、状态监控、告警管理等功能。主要用于：

- 项目进度监控
- 资源使用状态展示
- 系统性能指标监控
- 告警信息管理

## 系统架构

### 核心组件

1. 监控中心
   - 数据接收与处理
   - 数据存储与分析
   - Web管理界面

2. Agent采集器
   - 日志文件采集
   - 服务器资源监控
   - 实时数据推送
   - 心跳检测

## 系统要求

- Python 3.10+
- Node.js 16+
- MariaDB 10+
- Redis 6.0+

## 安装部署

### Agent部署

1. 安装Agent：

    ```bash
    pip install monitor-agent
    ```

2. 配置Agent：

    ```bash
    cp agent.conf.example agent.conf
    ```

    配置文件主要参数：
    ```ini
    [server]
    # 监控中心地址
    server_url = http://monitor-center:8000
    # Agent ID
    agent_id = agent_001
    # 项目标识
    project_id = project_001
    
    [log_collect]
    # 日志文件路径
    log_paths = [
        "/path/to/app1/*.log",
        "/path/to/app2/error.log"
    ]
    # 日志采集间隔(秒)
    collect_interval = 60
    # 日志关键字过滤
    keywords = ["ERROR", "FATAL", "WARNING"]
    
    [resource_monitor]
    # 资源监控间隔(秒)
    monitor_interval = 30
    # 监控项
    items = [
        "cpu_usage",
        "memory_usage",
        "disk_usage",
        "network_io",
        "process_count"
    ]
    # 告警阈值
    thresholds = {
        "cpu_usage": 80,
        "memory_usage": 85,
        "disk_usage": 90
    }
    
    [security]
    # 认证密钥
    auth_key = your_auth_key
    
    [alert]
    # 告警配置
    enable_alert = true
    # 告警级别
    alert_levels = ["critical", "warning", "info"]
    
    # 日志告警规则
    log_alert_rules = [
        {
            "keywords": ["ERROR", "FATAL"],
            "level": "critical",
            "min_occurrences": 3,
            "time_window": 300
        },
        {
            "keywords": ["WARNING"],
            "level": "warning",
            "min_occurrences": 5,
            "time_window": 600
        }
    ]
    
    # 资源告警规则
    resource_alert_rules = {
        "cpu_usage": {
            "critical": 90,
            "warning": 80
        },
        "memory_usage": {
            "critical": 90,
            "warning": 85
        },
        "disk_usage": {
            "critical": 95,
            "warning": 90
        }
    }
    
    [notification]
    # 通知方式配置
    channels = ["wechat", "email"]
    
    # 微信通知配置
    [notification.wechat]
    corp_id = "your_corp_id"
    corp_secret = "your_corp_secret"
    agent_id = "your_agent_id"
    to_user = "@all"
    
    # 邮件通知配置
    [notification.email]
    smtp_server = "smtp.example.com"
    smtp_port = 587
    username = "your_email@example.com"
    password = "your_password"
    from_addr = "monitor@example.com"
    to_addrs = ["admin@example.com", "dev@example.com"]
    ```

3. 运行Agent：

    ```bash
    python -m monitor_agent start
    ```

### 后端部署

1. 创建虚拟环境：

    ```bash
    python -m venv venv
    source venv/bin/activate  # Windows使用: venv\Scripts\activate
    ```

2. 安装依赖：

    ```bash
    pip install -r requirements.txt
    ```

3. 配置环境变量：

    ```bash
    cp .env.example .env
    # 编辑.env文件配置数据库等信息
    ```

4. 初始化数据库：

    ```bash
    python manage.py init-db
    ```

### 前端部署

1. 安装依赖：

    ```bash
    npm install
    ```

2. 开���环境运行：

    ```bash
    npm run dev
    ```

3. 生产环境构建：

    ```bash
    npm run build
    ```

## 基本功能

### 1. 监控大屏

- 项目状态概览
- 实时数据展示
- 性能指标图表
- 告警信息展示

### 2. 项目管理

- 项目信息配置
- 状态指标设置
- 监控规则管理
- Agent管理
  - Agent部署状态
  - Agent配置管理
  - Agent升级管理

### 3. 数据采集

- 日志采集管理
  - 日志文件配置
  - 关键字过滤设置
  - 采集频率控制
  - 日志解析规则
- 资源监控管理
  - CPU使用率监控
  - 内存使用监控
  - 磁盘使用监控
  - 网络IO监控
  - 进程数量监控
- Agent状态监控
  - 在线状态检测
  - 采集任务管理
  - 数据推送监控
- 采集配置管理
  - 采集项配置
  - 采集频率设置
  - 实时推送配置
- 数据传输管理
  - 数据压缩
  - 断点续传
  - 数据加密

### 4. 告警管理

- 告警规则配置
  - 日志关键字告警
  - 资源阈值告警
  - 自定义告警规则
- 告警级别设置
  - 严重告警
  - 警告
  - 提示
- 通知方式配置
  - 微信企业号推送
  - 邮件通知
  - 短信通知
  - 钉钉/企业微信群通知
- 通知对象管理
  - 人员/群组管理
  - 值班表配置
  - 告警升级策���
- 告警历史查询
  - 告警记录查询
  - 通知发送记录
  - 处理状态跟踪

### 5. 系统配置

- 租户管理
  - 租户信息配置
  - 租户资源配额
  - 租户隔离设置

- 用户权限管理
  - 用户管理
    - 用户信息维护
    - 用户组管理
    - 用户状态控制
  - 角色管理
    - 预设角色
      - 系统管理员：系统全局配置权限
      - 租户管理员：租户内全部权限
      - 项目管理员：指定项目的管理权限
      - 运维人员：监控和告警处理权限
      - 普通用户：查看权限
    - 自定义角色
      - 自定义权限组合
      - 权限继承关系
  - 权限配置
    - 功能权限
      - 监控配置权限
      - 告警配置权限
      - 系统管理权限
    - 数据权限
      - 项目数据权限
      - 告警数据权限
      - 日志数据权限
    - 操作权限
      - 查看权限
      - 配置权限
      - 管理权限

- 审计日志
  - 用户操作日志
  - 权限变更日志
  - 系统配置变更日志

## 数据源配置 