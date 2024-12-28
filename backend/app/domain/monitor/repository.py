from abc import ABC, abstractmethod
from typing import Optional, List, Dict
from .aggregate import MonitoringTarget, Agent, MetricPoint, MetricType

class MonitoringTargetRepository(ABC):
    """监控目标仓储接口"""
    
    @abstractmethod
    async def get_by_id(self, id: str) -> Optional[MonitoringTarget]:
        pass
        
    @abstractmethod
    async def save(self, target: MonitoringTarget) -> None:
        pass
        
    @abstractmethod
    async def list_by_tenant(self, tenant_id: str) -> List[MonitoringTarget]:
        pass

class AgentRepository(ABC):
    """Agent仓储接口"""
    
    @abstractmethod
    async def get_by_id(self, id: str) -> Optional[Agent]:
        pass
        
    @abstractmethod
    async def save(self, agent: Agent) -> None:
        pass
        
    @abstractmethod
    async def list_by_target(self, target_id: str) -> List[Agent]:
        pass 

class MetricRepository(ABC):
    """监控数据仓储接口"""
    
    @abstractmethod
    async def save_metrics(self, points: List[MetricPoint]) -> None:
        """保存监控数据点"""
        pass
    
    @abstractmethod
    async def query_metrics(
        self,
        server_id: str,
        metric_type: MetricType,
        start_time: datetime,
        end_time: datetime,
        interval: str = "1m"
    ) -> List[Dict]:
        """查询监控数据"""
        pass
    
    @abstractmethod
    async def aggregate_metrics(
        self,
        server_ids: List[str],
        metric_type: MetricType,
        start_time: datetime,
        end_time: datetime,
        group_by: str = "1h"
    ) -> Dict:
        """聚合监控数据"""
        pass 