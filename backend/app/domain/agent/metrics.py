from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from abc import ABC, abstractmethod

@dataclass
class AgentMetrics:
    """Agent指标"""
    id: str
    agent_id: str
    timestamp: datetime
    cpu_percent: float
    memory_percent: float
    disk_usage: float
    network_in: int
    network_out: int
    created_at: datetime

@dataclass
class AgentMetricsHourly:
    """Agent指标小时聚合"""
    id: str
    agent_id: str
    hour: datetime
    cpu_percent_avg: float
    cpu_percent_max: float
    memory_percent_avg: float
    memory_percent_max: float
    disk_usage_avg: float
    disk_usage_max: float
    network_in_total: int
    network_out_total: int
    created_at: datetime

class AgentMetricsRepository(ABC):
    """Agent指标仓储接口"""
    
    @abstractmethod
    async def save_metrics(self, metrics: AgentMetrics) -> None:
        """保存指标"""
        pass
    
    @abstractmethod
    async def save_hourly_metrics(self, metrics: AgentMetricsHourly) -> None:
        """保存小时聚合指标"""
        pass
    
    @abstractmethod
    async def get_metrics(
        self,
        agent_id: str,
        start_time: datetime,
        end_time: datetime
    ) -> List[AgentMetrics]:
        """获取指标"""
        pass
    
    @abstractmethod
    async def get_hourly_metrics(
        self,
        agent_id: str,
        start_time: datetime,
        end_time: datetime
    ) -> List[AgentMetricsHourly]:
        """获取小时聚合指标"""
        pass
    
    @abstractmethod
    async def cleanup_metrics(self, before: datetime) -> None:
        """清理指标"""
        pass 