# API 文档

## 概述

本文档描述了运维管理平台的REST API接口。所有接口都需要通过认证才能访问。

## 认证

系统使用JWT Token认证机制。客户端需要在请求头中携带Token:

```
Authorization: Bearer <token>
```

获取Token:
```http
POST /api/v1/auth/login
Content-Type: application/json

{
    "username": "admin",
    "password": "password"
}
```

## API 端点

### 用户管理

#### 获取用户列表
```http
GET /api/v1/users?skip=0&limit=10
```

#### 创建用户
```http
POST /api/v1/users
Content-Type: application/json

{
    "username": "user1",
    "email": "user1@example.com",
    "password": "password",
    "full_name": "User One"
}
```

### 项目管理

#### 获取项目列表
```http
GET /api/v1/projects?skip=0&limit=10
```

#### 创建项目
```http
POST /api/v1/projects
Content-Type: application/json

{
    "name": "Project 1",
    "description": "Project description"
}
```

### 服务器管理

#### 获取服务器列表
```http
GET /api/v1/servers?skip=0&limit=10
```

#### 添加服务器
```http
POST /api/v1/servers
Content-Type: application/json

{
    "hostname": "server1",
    "ip_address": "192.168.1.100",
    "ssh_port": 22
}
```

### 监控告警

#### 获取告警列表
```http
GET /api/v1/alerts?skip=0&limit=10&status=active
```

#### 创建告警规则
```http
POST /api/v1/alert-rules
Content-Type: application/json

{
    "name": "CPU Usage Alert",
    "metric": "cpu_usage",
    "condition": ">",
    "threshold": 90,
    "severity": "high"
}
```

### 备份管理

#### 获取备份列表
```http
GET /api/v1/backups?skip=0&limit=10
```

#### 创建备份
```http
POST /api/v1/backups
Content-Type: application/json

{
    "name": "Backup 1",
    "type": "full",
    "description": "Full system backup"
}
```

### 日志管理

#### 获取日志列表
```http
GET /api/v1/logs?skip=0&limit=10&level=error
```

#### 导出日志
```http
GET /api/v1/logs/export?start_time=2024-01-01T00:00:00Z&end_time=2024-01-02T00:00:00Z
```

### 报表管理

#### 获取资源使用报表
```http
GET /api/v1/reports/resource-usage?start_time=2024-01-01T00:00:00Z&end_time=2024-01-02T00:00:00Z
```

#### 导出报表
```http
POST /api/v1/reports/export
Content-Type: application/json

{
    "report_type": "resource-usage",
    "start_time": "2024-01-01T00:00:00Z",
    "end_time": "2024-01-02T00:00:00Z",
    "format": "pdf",
    "include_charts": true
}
```

### 通知管理

#### 获取通知渠道列表
```http
GET /api/v1/notification-channels?skip=0&limit=10
```

#### 创建通知渠道
```http
POST /api/v1/notification-channels
Content-Type: application/json

{
    "name": "Email Channel",
    "type": "email",
    "config": {
        "host": "smtp.example.com",
        "port": 587,
        "username": "notify@example.com",
        "password": "password",
        "from_email": "notify@example.com",
        "from_name": "System Notification"
    }
}
```

## 错误处理

所有API在发生错误时会返回相应的HTTP状态码和错误信息：

```json
{
    "detail": "Error message"
}
```

常见状态码：
- 400: 请求参数错误
- 401: 未认证
- 403: 权限不足
- 404: 资源不存在
- 500: 服务器内部错误

## 分页

支持分页的接口都接受以下查询参数：
- skip: 跳过的记录数
- limit: 返回的最大记录数

响应中会包含分页信息：
```json
{
    "total": 100,
    "items": [...]
}
``` 