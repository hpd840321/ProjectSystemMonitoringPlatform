from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional

class AlertSeverity(str, Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"

class AlertStatus(str, Enum):
    PENDING = "pending"
    FIRING = "firing"
    RESOLVED = "resolved"

class NotificationType(str, Enum):
    EMAIL = "email"
    WEBHOOK = "webhook"
    SMS = "sms"
    SLACK = "slack"

@dataclass
class AlertRule:
    """告警规则聚合根"""
    id: str
    project_id: str
    name: str
    description: str
    metric_type: str
    condition: str  # 如: "value > 90"
    severity: AlertSeverity
    interval: int  # 检查间隔(秒)
    enabled: bool
    created_at: datetime
    updated_at: datetime

@dataclass
class AlertEvent:
    """告警事件聚合根"""
    id: str
    rule_id: str
    server_id: str
    status: AlertStatus
    severity: AlertSeverity
    summary: str
    details: Dict
    first_occurred_at: datetime
    last_occurred_at: datetime
    resolved_at: Optional[datetime]
    notification_sent: bool

@dataclass
class NotificationChannel:
    """通知渠道聚合根"""
    id: str
    name: str
    type: NotificationType
    config: Dict
    enabled: bool
    created_at: datetime
    updated_at: datetime

@dataclass
class AlertLevel:
    """告警级别"""
    id: str
    name: str
    description: Optional[str]
    color: str
    priority: int
    created_at: datetime
    updated_at: datetime 