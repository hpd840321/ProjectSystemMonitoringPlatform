from pydantic import BaseModel, Field
from typing import Optional, Dict, List
from datetime import datetime

class AlertLevelCreate(BaseModel):
    """创建告警级别请求"""
    name: str = Field(..., description="级别名称")
    color: str = Field(..., description="显示颜色")
    priority: int = Field(..., ge=1, le=5, description="优先级(1-5)")
    description: Optional[str] = Field(None, description="级别描述")

class AlertLevelResponse(BaseModel):
    """告警级别响应"""
    id: str
    name: str
    color: str
    priority: int
    description: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    @classmethod
    def from_domain(cls, level):
        return cls(
            id=level.id,
            name=level.name,
            color=level.color,
            priority=level.priority,
            description=level.description,
            created_at=level.created_at,
            updated_at=level.updated_at
        )

class NotificationChannelCreate(BaseModel):
    """创建通知渠道请求"""
    name: str = Field(..., description="渠道名称")
    type: str = Field(..., description="渠道类型(email/sms/webhook/slack)")
    config: Dict = Field(..., description="渠道配置")
    enabled: bool = Field(True, description="是否启用")

class NotificationChannelResponse(BaseModel):
    """通知渠道响应"""
    id: str
    name: str
    type: str
    config: Dict
    enabled: bool
    created_at: datetime
    updated_at: datetime
    
    @classmethod
    def from_domain(cls, channel):
        return cls(
            id=channel.id,
            name=channel.name,
            type=channel.type.value,
            config=channel.config,
            enabled=channel.enabled,
            created_at=channel.created_at,
            updated_at=channel.updated_at
        )

class ChannelTestRequest(BaseModel):
    """测试通知渠道请求"""
    title: str = Field(..., description="测试消息标题")
    content: str = Field(..., description="测试消息内容") 