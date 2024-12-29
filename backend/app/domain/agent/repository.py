from abc import ABC, abstractmethod
from typing import List, Optional
from .aggregate import Agent, AgentVersion, UpgradeTask

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
    async def get_by_server(self, server_id: str) -> Optional[Agent]:
        """获取服务器的Agent"""
        pass
    
    @abstractmethod
    async def list_by_status(self, status: str) -> List[Agent]:
        """获取指定状态的Agent列表"""
        pass

class AgentVersionRepository(ABC):
    """Agent版本仓储接口"""
    
    @abstractmethod
    async def save(self, version: AgentVersion) -> None:
        """保存版本"""
        pass
    
    @abstractmethod
    async def get_by_version(self, version: str) -> Optional[AgentVersion]:
        """获取指定版本"""
        pass
    
    @abstractmethod
    async def get_latest(self) -> Optional[AgentVersion]:
        """获取最新版本"""
        pass
    
    @abstractmethod
    async def list_all(self) -> List[AgentVersion]:
        """获取所有版本"""
        pass

class UpgradeTaskRepository(ABC):
    """升级任务仓储接口"""
    
    @abstractmethod
    async def save(self, task: UpgradeTask) -> None:
        """保存任务"""
        pass
    
    @abstractmethod
    async def get_by_id(self, task_id: str) -> Optional[UpgradeTask]:
        """获取任务"""
        pass
    
    @abstractmethod
    async def list_by_agent(self, agent_id: str) -> List[UpgradeTask]:
        """获取Agent的升级任务列表"""
        pass 