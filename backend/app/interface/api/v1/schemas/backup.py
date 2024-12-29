from datetime import datetime
from typing import Optional
from pydantic import BaseModel, constr, conint, validator

class BackupConfigBase(BaseModel):
    name: constr(min_length=1, max_length=50)
    type: constr(regex='^(system|database|files)$')
    target_path: str
    retention_count: conint(ge=1)
    schedule: str  # cron表达式
    enabled: bool = True

    @validator('target_path')
    def validate_target_path(cls, v):
        if not v.startswith('/'):
            raise ValueError('Target path must be absolute')
        return v

    @validator('schedule')
    def validate_schedule(cls, v):
        from croniter.croniter import croniter
        if not croniter.is_valid(v):
            raise ValueError('Invalid cron expression')
        return v

class BackupConfigCreate(BackupConfigBase):
    pass

class BackupConfigUpdate(BackupConfigBase):
    pass

class BackupConfigInDB(BackupConfigBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class BackupRecordBase(BaseModel):
    config_id: int
    file_path: str
    file_size: int
    status: str
    error_message: Optional[str] = None
    started_at: datetime
    completed_at: Optional[datetime] = None

class BackupRecordCreate(BackupRecordBase):
    pass

class BackupRecordInDB(BackupRecordBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True 