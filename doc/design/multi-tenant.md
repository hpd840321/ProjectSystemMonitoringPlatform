# 多租户设计方案

## 1. 概述

系统采用多租户架构，实现租户间的数据隔离和资源管理。每个租户可以管理多个项目，每个项目下可以管理多个服务器。

## 2. 租户模型

### 2.1 租户实体
```typescript
interface Tenant {
  id: string;          // 租户ID
  name: string;        // 租户名称
  status: TenantStatus;// 租户状态
  quota: TenantQuota;  // 租户配额
  created_at: Date;    // 创建时间
  updated_at: Date;    // 更新时间
}

interface TenantQuota {
  max_projects: number;  // 最大项目数
  max_servers: number;   // 最大服务器数
  max_users: number;     // 最大用户数
  storage_limit: number; // 存储限制(GB)
}
```

### 2.2 租户状态
```typescript
enum TenantStatus {
  ACTIVE = 'active',         // 正常
  SUSPENDED = 'suspended',   // 已暂停
  EXPIRED = 'expired',      // 已过期
  DELETED = 'deleted'       // 已删除
}
```

## 3. 数据隔离

### 3.1 数据库隔离
- 采用共享数据库，独立Schema的方式
- 所有业务表都包含tenant_id字段
- 通过数据库视图实现租户数据过滤
- 使用Row Level Security确保数据隔离

### 3.2 缓存隔离
```
# Redis Key格式
{tenant_id}:{resource_type}:{resource_id}

# 示例
tenant_123:project:456
tenant_123:server:789
```

### 3.3 文件存储隔离
```
/storage
  /{tenant_id}
    /logs
    /metrics
    /backups
```

## 4. 权限控制

### 4.1 租户角色
- TENANT_ADMIN: 租户管理员
- TENANT_MEMBER: 租户普通成员
- PROJECT_ADMIN: 项目管理员
- PROJECT_MEMBER: 项目成员

### 4.2 权限矩阵
| 权限项 | TENANT_ADMIN | TENANT_MEMBER | PROJECT_ADMIN | PROJECT_MEMBER |
|--------|--------------|---------------|---------------|----------------|
| 租户管理 | ✓ | - | - | - |
| 项目管理 | ✓ | - | ✓ | - |
| 服务器管理| ✓ | - | ✓ | - |
| 监控查看 | ✓ | ✓ | ✓ | ✓ |
| 告警配置 | ✓ | - | ✓ | - |
| 日志查看 | ✓ | ✓ | ✓ | ✓ |

## 5. 资源管理

### 5.1 配额控制
```python
def check_quota(tenant: Tenant, resource_type: str, count: int) -> bool:
    """检查租户配额"""
    if resource_type == 'project':
        return tenant.quota.max_projects >= count
    elif resource_type == 'server':
        return tenant.quota.max_servers >= count
    elif resource_type == 'user':
        return tenant.quota.max_users >= count
    return False
```

### 5.2 资源计费
```python
def calculate_usage(tenant: Tenant) -> Dict:
    """计算租户资源使用情况"""
    return {
        'projects': len(tenant.projects),
        'servers': sum(len(p.servers) for p in tenant.projects),
        'storage': calculate_storage_usage(tenant.id),
        'users': len(tenant.users)
    }
```

## 6. 接口设计

### 6.1 租户管理接口
```typescript
// 创建租户
POST /api/v1/tenants
{
  "name": string,
  "quota": {
    "max_projects": number,
    "max_servers": number,
    "max_users": number,
    "storage_limit": number
  }
}

// 获取租户信息
GET /api/v1/tenants/{tenant_id}

// 更新租户配额
PUT /api/v1/tenants/{tenant_id}/quota
{
  "max_projects": number,
  "max_servers": number,
  "max_users": number,
  "storage_limit": number
}
```

### 6.2 租户成员管理
```typescript
// 添加租户成员
POST /api/v1/tenants/{tenant_id}/members
{
  "user_id": string,
  "role": string
}

// 移除租户成员
DELETE /api/v1/tenants/{tenant_id}/members/{user_id}
```

## 7. 实现注意事项

### 7.1 性能优化
1. 租户数据缓存策略
2. 数据库索引优化
3. 大租户数据处理

### 7.2 安全考虑
1. 租户间数据隔离验证
2. 跨租户访问控制
3. 租户资源限制
4. 操作审计日志

### 7.3 可扩展性
1. 支���租户自定义配置
2. 支持租户特性开关
3. 支持租户插件扩展
4. 支持多级租户结构 