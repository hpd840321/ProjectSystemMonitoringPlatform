from datetime import datetime
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, constr

class TimeRange(BaseModel):
    start_time: datetime
    end_time: datetime

class ResourceUsageReport(BaseModel):
    time_range: TimeRange
    servers: List[Dict[str, Any]]  # 每个服务器的资源使用情况
    total_stats: Dict[str, float]  # 总体统计
    trends: Dict[str, List[float]]  # 趋势数据

class AlertReport(BaseModel):
    time_range: TimeRange
    total_count: int
    by_severity: Dict[str, int]
    by_status: Dict[str, int]
    by_server: Dict[str, int]
    trends: Dict[str, List[int]]  # 按天统计的趋势

class PerformanceReport(BaseModel):
    time_range: TimeRange
    metrics: Dict[str, List[float]]  # 各项性能指标
    stats: Dict[str, Dict[str, float]]  # 统计数据(min/max/avg)
    anomalies: List[Dict[str, Any]]  # 异常点

class ReportExportFormat(BaseModel):
    format: constr(regex='^(csv|pdf|excel)$')
    include_charts: bool = True 