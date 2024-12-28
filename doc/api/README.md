# API文档

此目录包含所有API相关文档。 

## 用户认证

### 登录
POST /api/v1/auth/login
```json
{
  "username": "string",
  "password": "string"
}
```

### 获取当前用户信息
GET /api/v1/users/me

### 修改密码
PUT /api/v1/users/me/password
```json
{
  "old_password": "string",
  "new_password": "string"
}
```

## 项目管理API

### 项目管理
```http
# 创建项目
POST /api/v1/projects
Content-Type: application/json

{
  "name": "示例项目",
  "description": "项目描述",
  "config": {
    "quota": {
      "max_servers": 10,
      "max_agents": 10
    }
  }
}

# 获取项目列表
GET /api/v1/projects

# 获取项目详情
GET /api/v1/projects/{project_id}

# 更新项目
PUT /api/v1/projects/{project_id}

# 删除项目
DELETE /api/v1/projects/{project_id}
```

### 服务器管理
```http
# 添加服务器
POST /api/v1/projects/{project_id}/servers
Content-Type: application/json

{
  "name": "web-server-1",
  "host": "192.168.1.100",
  "type": "web",
  "description": "Web服务器1",
  "log_paths": [
    "/var/log/nginx/access.log",
    "/var/log/nginx/error.log"
  ],
  "metrics_config": {
    "cpu": {
      "enabled": true,
      "interval": 60
    },
    "memory": {
      "enabled": true,
      "interval": 60
    }
  }
}

# 获取服务器列表
GET /api/v1/projects/{project_id}/servers

# 获取服务器详情
GET /api/v1/projects/{project_id}/servers/{server_id}

# 更新服务器配置
PUT /api/v1/projects/{project_id}/servers/{server_id}

# 删除服务器
DELETE /api/v1/projects/{project_id}/servers/{server_id}

# 获取服务器指标
GET /api/v1/projects/{project_id}/servers/{server_id}/metrics

# 获取服务器日志
GET /api/v1/projects/{project_id}/servers/{server_id}/logs
``` 

## 项目成员管理

### 添加项目成员
POST /api/v1/projects/{project_id}/members
```json
{
  "user_id": "string",
  "role": "admin|member|viewer"
}
```

### 移除项目成员
DELETE /api/v1/projects/{project_id}/members/{user_id}

### 获取项目成员列表
GET /api/v1/projects/{project_id}/members 

## 认证接口

### 用户注册
POST /api/v1/auth/register
```json
{
  "username": "string",
  "email": "string", 
  "password": "string"
}
```

### 用户登录
POST /api/v1/auth/login
```json
{
  "username": "string",
  "password": "string"
}
```

### 获取当前用户信息
GET /api/v1/users/me
Authorization: Bearer <token>

### 修改密码
PUT /api/v1/users/me/password
Authorization: Bearer <token>
```json
{
  "old_password": "string",
  "new_password": "string"
}
```

### 添加项目成员
POST /api/v1/projects/{project_id}/members
Authorization: Bearer <token>
```json
{
  "user_id": "string",
  "role": "admin|member|viewer"
}
```

### 移除项目成员
DELETE /api/v1/projects/{project_id}/members/{user_id}
Authorization: Bearer <token>

### 获取项目成员列表
GET /api/v1/projects/{project_id}/members
Authorization: Bearer <token> 

## Agent管理

### 注册Agent
POST /api/v1/agents/register
```json
{
  "server_id": "string",
  "hostname": "string",
  "ip_address": "string",
  "system_info": {},
  "version": "string"
}
```

### 获取Agent信息
GET /api/v1/agents/{agent_id}

### 获取服务器Agent列表
GET /api/v1/servers/{server_id}/agents

### 更新Agent心跳
POST /api/v1/agents/{agent_id}/heartbeat
```json
{
  "cpu_usage": 0.0,
  "memory_usage": 0.0,
  "disk_usage": {},
  "network_io": {}
}
``` 

## 系统管理

### 备份管理

#### 创建备份
POST /api/v1/backups

需要管理员权限

响应:
```json
"backup_20240315_123456.tar.gz"
```

#### 恢复备份
POST /api/v1/backups/{backup_file}/restore

需要管理员权限

#### 获取备份列表
GET /api/v1/backups

需要管理员权限

响应:
```json
[
  "backup_20240315_123456.tar.gz",
  "backup_20240314_123456.tar.gz"
]
``` 