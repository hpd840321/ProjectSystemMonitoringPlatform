from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

@dataclass
class LogEntry:
    """日志条目实体"""
    id: str
    timestamp: datetime
    level: str
    message: str
    source: str
    tags: List[str]

@dataclass
class ResourceMetric:
    """资源指标实体"""
    id: str
    timestamp: datetime
    metric_type: str  # cpu, memory, disk, network
    value: float
    unit: str
    host: str
    tags: dict

@dataclass
class Agent:
    """Agent实体"""
    id: str
    host: str
    status: str
    last_heartbeat: datetime
    version: str
    config: dict 