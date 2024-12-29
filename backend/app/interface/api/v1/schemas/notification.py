from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, constr, validator

class EmailConfig(BaseModel):
    host: str
    port: int
    username: str
    password: str
    use_tls: bool = True
    from_email: str
    from_name: str

class WebhookConfig(BaseModel):
    url: str
    method: str = "POST"
    headers: Optional[Dict[str, str]] = None
    timeout: int = 30

class SMSConfig(BaseModel):
    provider: str
    api_key: str
    api_secret: str
    sign_name: str

class NotificationChannelBase(BaseModel):
    name: constr(min_length=1, max_length=50)
    type: constr(regex='^(email|webhook|sms)$')
    config: Dict[str, Any]
    enabled: bool = True
    description: Optional[str] = None

    @validator('config')
    def validate_config(cls, v, values):
        channel_type = values.get('type')
        if channel_type == 'email':
            EmailConfig(**v)
        elif channel_type == 'webhook':
            WebhookConfig(**v)
        elif channel_type == 'sms':
            SMSConfig(**v)
        return v

class NotificationChannelCreate(NotificationChannelBase):
    pass

class NotificationChannelUpdate(NotificationChannelBase):
    pass

class NotificationChannelInDB(NotificationChannelBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class NotificationTemplateBase(BaseModel):
    name: constr(min_length=1, max_length=50)
    type: constr(regex='^(alert|backup|system)$')
    subject_template: str
    content_template: str
    description: Optional[str] = None

class NotificationTemplateCreate(NotificationTemplateBase):
    pass

class NotificationTemplateUpdate(NotificationTemplateBase):
    pass

class NotificationTemplateInDB(NotificationTemplateBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class NotificationLogBase(BaseModel):
    channel_id: int
    template_id: int
    event_type: str
    recipients: List[str]
    subject: str
    content: str
    status: constr(regex='^(success|failed)$')
    error_message: Optional[str] = None

class NotificationLogCreate(NotificationLogBase):
    pass

class NotificationLogInDB(NotificationLogBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True 