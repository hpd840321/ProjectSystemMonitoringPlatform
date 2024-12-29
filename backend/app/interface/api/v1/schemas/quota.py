from datetime import datetime
from typing import Optional
from pydantic import BaseModel, conint

class QuotaBase(BaseModel):
    resource_type: str
    quota_limit: conint(ge=0)  # 配额必须大于等于0

class QuotaCreate(QuotaBase):
    project_id: int

class QuotaUpdate(QuotaBase):
    pass

class QuotaInDB(QuotaBase):
    id: int
    project_id: int
    used_amount: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class ResourceUsageCreate(BaseModel):
    project_id: int
    resource_type: str
    amount: int
    operation: str 