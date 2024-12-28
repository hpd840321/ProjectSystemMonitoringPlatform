from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict
from enum import Enum

class AgentStatus(Enum):
    ONLINE = "online"
    OFFLINE = "offline"
    ERROR = "error"

@dataclass(frozen=True)
class LogEntry:
    """日志条目值对象"""
    timestamp: datetime
    level: str
    message: str
    source: str
    tags: List[str]

@dataclass(frozen=True)
class ResourceMetric:
    """资源指标值对象"""
    timestamp: datetime
    metric_type: str
    value: float
    unit: str
    host: str
    tags: Dict[str, str] 