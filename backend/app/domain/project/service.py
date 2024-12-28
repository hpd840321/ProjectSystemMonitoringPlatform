from typing import List, Optional, Dict
from datetime import datetime, timedelta
from uuid import uuid4
from .aggregate import Project, Server
from .value_objects import ProjectStatus, ResourceQuota, ServerMetrics
from .repository import ProjectRepository, ServerRepository
from .exceptions import ProjectNotFoundError, ServerNotFoundError

class ProjectService:
    """项目领域服务"""
    
    def __init__(
        self,
        project_repo: ProjectRepository,
        server_repo: ServerRepository
    ):
        self.project_repo = project_repo
        self.server_repo = server_repo
    
    async def create_project(
        self,
        name: str,
        description: str,
        max_servers: int = 10,
        max_agents: int = 10
    ) -> Project:
        """创建项目"""
        quota = ResourceQuota(max_servers=max_servers, max_agents=max_agents)
        project = Project.create(name=name, description=description, quota=quota)
        await self.project_repo.save(project)
        return project

    async def add_server(
        self,
        project_id: str,
        name: str,
        host: str,
        description: str
    ) -> Server:
        """添加服务器"""
        project = await self.project_repo.get_by_id(project_id)
        if not project:
            raise ProjectNotFoundError(f"Project {project_id} not found")

        server = Server.create(name=name, host=host, description=description)
        project.add_server(server)
        
        await self.server_repo.save(server)
        await self.project_repo.save(project)
        
        return server

    async def update_server_metrics(
        self,
        server_id: str,
        metrics: ServerMetrics
    ) -> None:
        """更新服务器指标"""
        server = await self.server_repo.get_by_id(server_id)
        if not server:
            raise ServerNotFoundError(f"Server {server_id} not found")

        server.update_metrics(metrics)
        await self.server_repo.save(server) 

    async def get_project_stats(self, project_id: str) -> Dict:
        """获取项目统计数据"""
        # 获取服务器统计
        servers = await self.server_repo.list_by_project(project_id)
        server_count = len(servers)
        
        # 获取在线Agent统计
        online_agents = 0
        for server in servers:
            agents = await self.agent_repo.list_by_server(server.id)
            online_agents += len([a for a in agents if a.status == AgentStatus.ONLINE])
        
        # 获取告警统计
        alerts = await self.alert_repo.list_by_project(
            project_id,
            datetime.now() - timedelta(days=7)
        )
        alert_count = len(alerts)
        
        return {
            "server_count": server_count,
            "online_agents": online_agents,
            "alert_count": alert_count,
            "resource_usage": {
                "cpu": await self._get_avg_cpu_usage(servers),
                "memory": await self._get_avg_memory_usage(servers),
                "disk": await self._get_avg_disk_usage(servers)
            }
        } 