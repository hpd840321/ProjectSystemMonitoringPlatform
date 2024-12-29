from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, constr

class AuditLogBase(BaseModel):
    user_id: Optional[int]
    username: Optional[str]
    action: constr(min_length=1, max_length=50)  # 操作类型
    resource_type: constr(min_length=1, max_length=50)  # 资源类型
    resource_id: Optional[str]  # 资源ID
    status: constr(regex='^(success|failed)$')  # 操作状态
    ip_address: Optional[str]  # 客户端IP
    user_agent: Optional[str]  # 用户代理
    details: Optional[Dict[str, Any]]  # 详细信息
    error_message: Optional[str]  # 错误信息

class AuditLogCreate(AuditLogBase):
    pass

class AuditLogInDB(AuditLogBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class AuditLogFilter(BaseModel):
    user_id: Optional[int] = None
    username: Optional[str] = None
    action: Optional[str] = None
    resource_type: Optional[str] = None
    resource_id: Optional[str] = None
    status: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None 