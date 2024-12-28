from abc import ABC, abstractmethod
from typing import List, Optional
from .aggregate import Agent, AgentMetrics

class AgentRepository(ABC):
    """Agent仓储接口"""
    
    @abstractmethod
    async def save(self, agent: Agent) -> None:
        """保存Agent"""
        pass
    
    @abstractmethod
    async def get_by_id(self, agent_id: str) -> Optional[Agent]:
        """获取Agent"""
        pass
    
    @abstractmethod
    async def list_by_server(self, server_id: str) -> List[Agent]:
        """获取服务器的Agent列表"""
        pass
    
    @abstractmethod
    async def update_status(
        self,
        agent_id: str,
        status: str,
        heartbeat: datetime
    ) -> None:
        """更新Agent状态"""
        pass

class AgentMetricsRepository(ABC):
    """Agent指标仓储接口"""
    
    @abstractmethod
    async def save_metrics(self, metrics: AgentMetrics) -> None:
        """保存Agent指标"""
        pass
    
    @abstractmethod
    async def get_latest_metrics(self, agent_id: str) -> Optional[AgentMetrics]:
        """获取���新指标"""
        pass 