from datetime import datetime
from typing import Optional, Any, Dict
from pydantic import BaseModel, constr, validator

class SystemSettingBase(BaseModel):
    category: constr(min_length=1, max_length=50)
    key: constr(min_length=1, max_length=100)
    value: Any
    description: Optional[str] = None

class SystemSettingCreate(SystemSettingBase):
    pass

class SystemSettingUpdate(SystemSettingBase):
    pass

class SystemSettingInDB(SystemSettingBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class UserPreferenceBase(BaseModel):
    user_id: int
    key: constr(min_length=1, max_length=100)
    value: Any

class UserPreferenceCreate(UserPreferenceBase):
    pass

class UserPreferenceUpdate(UserPreferenceBase):
    pass

class UserPreferenceInDB(UserPreferenceBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# 特定设置的验证模型
class SMTPConfig(BaseModel):
    host: str
    port: int
    username: str
    password: str
    use_tls: bool = True
    from_email: str
    from_name: str

class PasswordPolicy(BaseModel):
    min_length: int
    require_uppercase: bool
    require_lowercase: bool
    require_numbers: bool
    require_special_chars: bool
    max_age_days: int

class SessionConfig(BaseModel):
    timeout_minutes: int
    max_sessions_per_user: int

class SeverityLevel(BaseModel):
    name: str
    color: str

class BackupPaths(BaseModel):
    system: str
    database: str
    files: str 