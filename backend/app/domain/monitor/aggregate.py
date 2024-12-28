from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Dict, Optional

class MetricType(str, Enum):
    CPU = "cpu"
    MEMORY = "memory"
    DISK = "disk"
    NETWORK = "network"

@dataclass
class MetricPoint:
    """监控数据点"""
    server_id: str
    metric_type: MetricType
    value: float
    timestamp: datetime
    labels: Dict[str, str]

@dataclass
class MetricConfig:
    """监控配置"""
    enabled: bool = True
    interval: int = 60  # 采集间隔(秒)
    retention: int = 30  # 保留天数

@dataclass
class ServerMetrics:
    """服务器监控配置"""
    server_id: str
    configs: Dict[MetricType, MetricConfig]
    created_at: datetime
    updated_at: datetime 