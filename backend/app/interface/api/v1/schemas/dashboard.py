from typing import List, Dict, Any, Optional
from datetime import datetime
from pydantic import BaseModel

class ResourceUsage(BaseModel):
    cpu_usage: float
    memory_usage: float
    disk_usage: float
    network_in: float
    network_out: float
    timestamp: datetime

class ResourceTrend(BaseModel):
    timestamps: List[datetime]
    cpu_usage: List[float]
    memory_usage: List[float]
    disk_usage: List[float]
    network_in: List[float]
    network_out: List[float]

class AlertSummary(BaseModel):
    total: int
    by_severity: Dict[str, int]  # 按严重程度统计
    by_status: Dict[str, int]    # 按状态统计
    recent_alerts: List[Dict[str, Any]]  # 最近的告警

class SystemStatus(BaseModel):
    total_servers: int
    online_servers: int
    total_projects: int
    active_projects: int

class RecentEvent(BaseModel):
    id: int
    event_type: str
    resource_type: str
    resource_name: str
    message: str
    severity: str
    timestamp: datetime

class DashboardOverview(BaseModel):
    system_status: SystemStatus
    resource_usage: ResourceUsage
    alert_summary: AlertSummary
    recent_events: List[RecentEvent]

class DashboardTrends(BaseModel):
    resource_trends: ResourceTrend
    alert_trends: Dict[str, List[int]]  # 按天统计的告警数量