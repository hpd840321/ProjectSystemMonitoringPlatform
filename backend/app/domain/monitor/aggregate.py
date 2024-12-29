from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Optional
from enum import Enum

class MetricType(str, Enum):
    COUNTER = "counter"  # 计数器类型(如:请求总数)
    GAUGE = "gauge"      # 仪表盘类型(如:CPU使用率)

class AggregationType(str, Enum):
    AVG = "avg"
    MAX = "max"
    MIN = "min"
    SUM = "sum"

@dataclass
class CustomMetric:
    """自定义监控指标"""
    id: str
    project_id: str
    name: str
    description: Optional[str]
    metric_type: MetricType
    unit: Optional[str]
    labels: Dict
    collection_script: str
    interval: int
    enabled: bool
    created_at: datetime
    updated_at: datetime

@dataclass
class MetricValue:
    """指标数据点"""
    id: str
    metric_id: str
    server_id: str
    value: float
    labels: Dict
    timestamp: datetime

@dataclass
class MetricAggregation:
    """指标聚合配置"""
    id: str
    metric_id: str
    name: str
    description: Optional[str]
    aggregation_type: AggregationType
    interval: str
    retention_days: int
    enabled: bool
    created_at: datetime
    updated_at: datetime

@dataclass
class AggregatedMetric:
    """聚合后的指标数据"""
    id: str
    aggregation_id: str
    server_id: str
    value: float
    start_time: datetime
    end_time: datetime

@dataclass
class RetentionPolicy:
    """数据保留策略"""
    id: str
    metric_id: str
    raw_data_retention_days: int
    aggregated_data_retention_days: int
    created_at: datetime
    updated_at: datetime 