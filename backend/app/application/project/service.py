from typing import List, Optional
from datetime import datetime
from app.domain.project.service import ProjectService
from app.domain.project.value_objects import ServerMetrics
from .dto import (
    ProjectCreateDTO,
    ProjectDTO,
    ServerCreateDTO,
    ServerDTO,
    ServerMetricsDTO
)

class ProjectApplicationService:
    """项目应用服务"""

    def __init__(self, project_service: ProjectService):
        self.project_service = project_service

    async def create_project(
        self,
        tenant_id: str,
        dto: ProjectCreateDTO
    ) -> ProjectDTO:
        """创建项目"""
        project = await self.project_service.create_project(
            tenant_id=tenant_id,
            name=dto.name,
            description=dto.description,
            max_servers=dto.max_servers,
            max_agents=dto.max_agents
        )
        return ProjectDTO.from_domain(project)

    async def add_server(self, project_id: str, dto: ServerCreateDTO) -> ServerDTO:
        """添加服务器"""
        server = await self.project_service.add_server(
            project_id=project_id,
            name=dto.name,
            host=dto.host,
            description=dto.description
        )
        return ServerDTO.from_domain(server)

    async def update_server_metrics(
        self,
        server_id: str,
        dto: ServerMetricsDTO
    ) -> None:
        """更新服务器指标"""
        metrics = ServerMetrics(
            cpu_usage=dto.cpu_usage,
            memory_usage=dto.memory_usage,
            disk_usage=dto.disk_usage,
            network_io=dto.network_io,
            timestamp=datetime.now()
        )
        await self.project_service.update_server_metrics(server_id, metrics) 