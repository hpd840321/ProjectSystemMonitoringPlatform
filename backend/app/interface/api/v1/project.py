from typing import List
from fastapi import APIRouter, Depends, HTTPException
from app.application.project.service import ProjectApplicationService
from app.application.project.dto import (
    ProjectCreateDTO,
    ProjectDTO,
    ServerCreateDTO,
    ServerDTO,
    ServerMetricsDTO
)
from .dependencies import get_project_service
from app.application.tenant.service import get_current_tenant

router = APIRouter(prefix="/projects", tags=["projects"])

@router.post("", response_model=ProjectDTO)
async def create_project(
    dto: ProjectCreateDTO,
    current_tenant = Depends(get_current_tenant),
    service: ProjectApplicationService = Depends(get_project_service)
) -> ProjectDTO:
    """创建项目"""
    return await service.create_project(tenant_id=current_tenant.id, dto=dto)

@router.post("/{project_id}/servers", response_model=ServerDTO)
async def add_server(
    project_id: str,
    dto: ServerCreateDTO,
    service: ProjectApplicationService = Depends(get_project_service)
) -> ServerDTO:
    """添加服务器"""
    try:
        return await service.add_server(project_id, dto)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.put("/servers/{server_id}/metrics")
async def update_server_metrics(
    server_id: str,
    dto: ServerMetricsDTO,
    service: ProjectApplicationService = Depends(get_project_service)
) -> None:
    """更新服务器指标"""
    try:
        await service.update_server_metrics(server_id, dto)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) 