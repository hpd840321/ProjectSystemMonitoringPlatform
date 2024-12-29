from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class MetricsQuery(BaseModel):
    """指标查询参数"""
    start_time: datetime
    end_time: datetime
    interval: str = "raw"  # raw/hourly

class MetricsResponse(BaseModel):
    """指标响应"""
    timestamp: datetime
    cpu_percent: float
    memory_percent: float
    disk_usage: float
    network_in: int
    network_out: int

class HourlyMetricsResponse(BaseModel):
    """小时聚合指标响应"""
    hour: datetime
    cpu_percent_avg: float
    cpu_percent_max: float
    memory_percent_avg: float
    memory_percent_max: float
    disk_usage_avg: float
    disk_usage_max: float
    network_in_total: int
    network_out_total: int 