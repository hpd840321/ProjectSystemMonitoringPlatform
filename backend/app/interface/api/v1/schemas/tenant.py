from datetime import datetime
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, constr

class TenantBase(BaseModel):
    name: constr(min_length=1, max_length=100)
    code: constr(min_length=1, max_length=50)
    status: constr(regex='^(active|suspended|deleted)$') = 'active'
    max_users: Optional[int] = None
    max_projects: Optional[int] = None
    max_servers: Optional[int] = None
    settings: Optional[Dict[str, Any]] = None

class TenantCreate(TenantBase):
    pass

class TenantUpdate(TenantBase):
    name: Optional[constr(min_length=1, max_length=100)] = None
    code: Optional[constr(min_length=1, max_length=50)] = None
    status: Optional[constr(regex='^(active|suspended|deleted)$')] = None

class TenantInDB(TenantBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class UserTenantBase(BaseModel):
    user_id: int
    tenant_id: int
    role: constr(regex='^(owner|admin|member)$')

class UserTenantCreate(UserTenantBase):
    pass

class UserTenantUpdate(BaseModel):
    role: constr(regex='^(owner|admin|member)$')

class UserTenantInDB(UserTenantBase):
    created_at: datetime

    class Config:
        orm_mode = True

class TenantStats(BaseModel):
    total_users: int
    total_projects: int
    total_servers: int
    resource_usage: Dict[str, float] 