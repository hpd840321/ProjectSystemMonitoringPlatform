from typing import Dict, List
from datetime import datetime
from .repository import NotificationChannelRepository
from .aggregate import AlertEvent, NotificationChannel
from app.infrastructure.notification.sender import (
    EmailSender,
    WebhookSender
)
from dataclasses import dataclass
from enum import Enum
from typing import Dict, Optional

class NotificationType(str, Enum):
    EMAIL = "email"
    WEBHOOK = "webhook"
    SMS = "sms"

@dataclass
class AlertLevel:
    id: str
    name: str
    description: Optional[str]
    severity: int
    color: Optional[str]
    created_at: datetime
    updated_at: datetime

@dataclass
class NotificationChannel:
    id: str
    name: str
    type: NotificationType
    config: Dict
    enabled: bool
    created_at: datetime
    updated_at: datetime

@dataclass
class AlertNotification:
    alert_id: str
    channel_id: str
    sent_at: datetime
    status: str
    error: Optional[str]

class NotificationService:
    """告警通知服务"""
    
    def __init__(self, channel_repo: NotificationChannelRepository):
        self.channel_repo = channel_repo
        self.senders = {
            'email': EmailSender(),
            'webhook': WebhookSender()
        }
    
    async def send_notifications(
        self,
        project_id: str,
        alert: AlertEvent
    ) -> None:
        """发送告警通知"""
        channels = await self.channel_repo.list_by_project(project_id)
        
        for channel in channels:
            if not channel.enabled:
                continue
                
            sender = self.senders.get(channel.type)
            if not sender:
                continue
                
            message = self._format_message(alert)
            success = await sender.send(channel.config, message)
            
            if success:
                alert.notification_sent = True
    
    def _format_message(self, alert: AlertEvent) -> str:
        """格式化告警消息"""
        return f"""
Alert: {alert.summary}
Severity: {alert.severity}
Server: {alert.server_id}
Status: {alert.status}
Time: {alert.last_occurred_at}

Details:
{alert.details}
        """.strip() 