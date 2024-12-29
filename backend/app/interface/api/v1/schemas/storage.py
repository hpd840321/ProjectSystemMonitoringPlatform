from datetime import datetime
from typing import Optional
from pydantic import BaseModel, constr, conint, validator

class StoragePolicyBase(BaseModel):
    name: constr(min_length=1, max_length=50)
    data_type: constr(regex='^(metrics|logs|alerts|backups)$')
    retention_days: conint(ge=1)
    compression_enabled: bool = False
    compression_after_days: Optional[conint(ge=1)] = None
    backup_enabled: bool = False
    backup_schedule: Optional[str] = None

    @validator('compression_after_days')
    def validate_compression_days(cls, v, values):
        if values.get('compression_enabled') and not v:
            raise ValueError('compression_after_days is required when compression is enabled')
        if v and v >= values.get('retention_days', 0):
            raise ValueError('compression_after_days must be less than retention_days')
        return v

    @validator('backup_schedule')
    def validate_backup_schedule(cls, v, values):
        if values.get('backup_enabled') and not v:
            raise ValueError('backup_schedule is required when backup is enabled')
        return v

class StoragePolicyCreate(StoragePolicyBase):
    pass

class StoragePolicyUpdate(StoragePolicyBase):
    pass

class StoragePolicyInDB(StoragePolicyBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class StoragePolicyExecution(BaseModel):
    id: int
    policy_id: int
    action_type: str
    status: str
    affected_rows: Optional[int]
    error_message: Optional[str]
    started_at: datetime
    completed_at: Optional[datetime]
    created_at: datetime

    class Config:
        orm_mode = True 