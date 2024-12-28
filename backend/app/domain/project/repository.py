from abc import ABC, abstractmethod
from typing import List, Optional
from .aggregate import Project, Server

class ProjectRepository(ABC):
    """项目仓储接口"""
    
    @abstractmethod
    async def save(self, project: Project) -> None:
        """保存项目"""
        pass

    @abstractmethod
    async def get_by_id(self, project_id: str) -> Optional[Project]:
        """根据ID获取项目"""
        pass

    @abstractmethod
    async def list_active(self) -> List[Project]:
        """获取所有活动项目"""
        pass

    @abstractmethod
    async def delete(self, project_id: str) -> None:
        """删除项目"""
        pass

    @abstractmethod
    async def list_by_tenant(self, tenant_id: str) -> List[Project]:
        """获取租户下的所有项目"""
        pass

class ServerRepository(ABC):
    """服务器仓储接口"""
    
    @abstractmethod
    async def save(self, server: Server) -> None:
        """保存服务器"""
        pass

    @abstractmethod
    async def get_by_id(self, server_id: str) -> Optional[Server]:
        """根据ID获取服务器"""
        pass

    @abstractmethod
    async def list_by_project(self, project_id: str) -> List[Server]:
        """获取项目下的所有服务器"""
        pass

    @abstractmethod
    async def get_by_agent(self, agent_id: str) -> Optional[Server]:
        """根据Agent ID获取服务器"""
        pass 