from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.project.aggregate import Project, Server
from app.domain.project.repository import ProjectRepository, ServerRepository
from app.domain.project.value_objects import ResourceQuota, ServerMetrics
from ..models.project import ProjectModel, ServerModel

class SQLAlchemyProjectRepository(ProjectRepository):
    """项目仓储SQLAlchemy实现"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, project: Project) -> None:
        """保存项目"""
        project_model = await self.session.get(ProjectModel, project.id)
        
        if not project_model:
            project_model = ProjectModel(
                id=project.id,
                name=project.name,
                description=project.description,
                status=project.status,
                max_servers=project.quota.max_servers,
                max_agents=project.quota.max_agents,
                config=project.config,
                created_at=project.created_at,
                updated_at=project.updated_at
            )
            self.session.add(project_model)
        else:
            project_model.name = project.name
            project_model.description = project.description
            project_model.status = project.status
            project_model.max_servers = project.quota.max_servers
            project_model.max_agents = project.quota.max_agents
            project_model.config = project.config
            project_model.updated_at = project.updated_at

        await self.session.commit()

    async def get_by_id(self, project_id: str) -> Optional[Project]:
        """根据ID获取项目"""
        stmt = select(ProjectModel).where(ProjectModel.id == project_id)
        result = await self.session.execute(stmt)
        project_model = result.scalar_one_or_none()
        
        if not project_model:
            return None
            
        return self._to_domain(project_model)

    async def list_active(self) -> List[Project]:
        """获取所有活动项目"""
        stmt = select(ProjectModel).where(ProjectModel.status == "active")
        result = await self.session.execute(stmt)
        return [self._to_domain(p) for p in result.scalars()]

    async def delete(self, project_id: str) -> None:
        """删除项目"""
        project_model = await self.session.get(ProjectModel, project_id)
        if project_model:
            await self.session.delete(project_model)
            await self.session.commit()

    def _to_domain(self, model: ProjectModel) -> Project:
        """转换为领域对象"""
        quota = ResourceQuota(
            max_servers=model.max_servers,
            max_agents=model.max_agents
        )
        
        return Project(
            id=model.id,
            name=model.name,
            description=model.description,
            status=model.status,
            quota=quota,
            created_at=model.created_at,
            updated_at=model.updated_at,
            config=model.config,
            servers=[self._server_to_domain(s) for s in model.servers]
        )

    def _server_to_domain(self, model: ServerModel) -> Server:
        """服务器模型转换为领域对象"""
        metrics = None
        if model.metrics:
            metrics = ServerMetrics(**model.metrics)
            
        return Server(
            id=model.id,
            name=model.name,
            host=model.host,
            description=model.description,
            status=model.status,
            last_heartbeat=model.last_heartbeat,
            metrics=metrics,
            agent_id=model.agent_id
        )

class SQLAlchemyServerRepository(ServerRepository):
    """服务器仓储SQLAlchemy实现"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, server: Server) -> None:
        """保存服务器"""
        server_model = await self.session.get(ServerModel, server.id)
        
        metrics_data = None
        if server.metrics:
            metrics_data = {
                "cpu_usage": server.metrics.cpu_usage,
                "memory_usage": server.metrics.memory_usage,
                "disk_usage": server.metrics.disk_usage,
                "network_io": server.metrics.network_io,
                "timestamp": server.metrics.timestamp.isoformat()
            }
        
        if not server_model:
            server_model = ServerModel(
                id=server.id,
                name=server.name,
                host=server.host,
                description=server.description,
                status=server.status,
                agent_id=server.agent_id,
                last_heartbeat=server.last_heartbeat,
                metrics=metrics_data
            )
            self.session.add(server_model)
        else:
            server_model.name = server.name
            server_model.host = server.host
            server_model.description = server.description
            server_model.status = server.status
            server_model.agent_id = server.agent_id
            server_model.last_heartbeat = server.last_heartbeat
            server_model.metrics = metrics_data

        await self.session.commit()

    async def get_by_id(self, server_id: str) -> Optional[Server]:
        """根据ID获取服务器"""
        stmt = select(ServerModel).where(ServerModel.id == server_id)
        result = await self.session.execute(stmt)
        server_model = result.scalar_one_or_none()
        
        if not server_model:
            return None
            
        return self._to_domain(server_model)

    async def list_by_project(self, project_id: str) -> List[Server]:
        """获取项目下的所有服务器"""
        stmt = select(ServerModel).where(ServerModel.project_id == project_id)
        result = await self.session.execute(stmt)
        return [self._to_domain(s) for s in result.scalars()]

    async def get_by_agent(self, agent_id: str) -> Optional[Server]:
        """根据Agent ID获取服务器"""
        stmt = select(ServerModel).where(ServerModel.agent_id == agent_id)
        result = await self.session.execute(stmt)
        server_model = result.scalar_one_or_none()
        
        if not server_model:
            return None
            
        return self._to_domain(server_model)

    def _to_domain(self, model: ServerModel) -> Server:
        """转换为领域对象"""
        metrics = None
        if model.metrics:
            metrics = ServerMetrics(
                cpu_usage=model.metrics["cpu_usage"],
                memory_usage=model.metrics["memory_usage"],
                disk_usage=model.metrics["disk_usage"],
                network_io=model.metrics["network_io"],
                timestamp=datetime.fromisoformat(model.metrics["timestamp"])
            )
            
        return Server(
            id=model.id,
            name=model.name,
            host=model.host,
            description=model.description,
            status=model.status,
            last_heartbeat=model.last_heartbeat,
            metrics=metrics,
            agent_id=model.agent_id
        ) 