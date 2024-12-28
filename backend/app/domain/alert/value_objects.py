from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Dict, Any, List

class AlertSeverity(Enum):
    CRITICAL = "critical"
    WARNING = "warning"
    INFO = "info"

class AlertStatus(Enum):
    ACTIVE = "active"
    ACKNOWLEDGED = "acknowledged"
    RESOLVED = "resolved"
    SUPPRESSED = "suppressed"

@dataclass(frozen=True)
class AlertCondition:
    """告警条件值对象"""
    metric_type: str
    operator: str  # >, <, >=, <=, ==, !=
    threshold: float
    duration: int  # 持续时间(秒)

@dataclass(frozen=True)
class AlertEvent:
    """告警事件值对象"""
    timestamp: datetime
    target_id: str
    agent_id: str
    metric_type: str
    value: float
    message: str 