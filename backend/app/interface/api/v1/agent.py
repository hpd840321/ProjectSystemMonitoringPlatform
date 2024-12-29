from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from typing import List, Union
import os
from .dependencies import get_current_user, get_agent_service
from .schemas.agent import (
    AgentRegisterRequest,
    AgentResponse,
    AgentVersionCreate,
    AgentVersionResponse,
    UpgradeTaskCreate,
    UpgradeTaskResponse,
    MetricsQuery,
    MetricsResponse,
    HourlyMetricsResponse
)
from ...domain.agent.exceptions import AgentMetricsError, MetricsNotFoundError, InvalidTimeRangeError

router = APIRouter()

# Agent管理
@router.post("/servers/{server_id}/agent", response_model=AgentResponse)
async def register_agent(
    server_id: str,
    data: AgentRegisterRequest,
    service = Depends(get_agent_service),
    user = Depends(get_current_user)
):
    """注册Agent"""
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="需要管理员权限")
    
    agent = await service.register_agent(
        server_id=server_id,
        version=data.version,
        config=data.config
    )
    return AgentResponse.from_domain(agent)

@router.post("/agents/{agent_id}/heartbeat")
async def update_heartbeat(
    agent_id: str,
    service = Depends(get_agent_service)
):
    """更新Agent心跳"""
    await service.update_heartbeat(agent_id)
    return {"message": "心跳更新成功"}

# Agent版本管理
@router.post("/agent-versions", response_model=AgentVersionResponse)
async def create_agent_version(
    data: AgentVersionCreate,
    file: UploadFile = File(...),
    service = Depends(get_agent_service),
    user = Depends(get_current_user)
):
    """创建Agent版本"""
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="需要管理员权限")
    
    # 保存上传文件
    file_path = f"uploads/agents/{data.version}/{file.filename}"
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)
    
    version = await service.create_version(
        version=data.version,
        file_path=file_path,
        description=data.description,
        is_latest=data.is_latest
    )
    return AgentVersionResponse.from_domain(version)

@router.get("/agent-versions", response_model=List[AgentVersionResponse])
async def list_agent_versions(
    service = Depends(get_agent_service)
):
    """获取Agent版本列表"""
    versions = await service.version_repo.list_all()
    return [AgentVersionResponse.from_domain(v) for v in versions]

@router.get("/agent-versions/latest", response_model=AgentVersionResponse)
async def get_latest_version(
    service = Depends(get_agent_service)
):
    """获取最新Agent版本"""
    version = await service.version_repo.get_latest()
    if not version:
        raise HTTPException(status_code=404, detail="未找到最新版本")
    return AgentVersionResponse.from_domain(version)

# Agent升级管理
@router.post("/agents/{agent_id}/upgrade", response_model=UpgradeTaskResponse)
async def create_upgrade_task(
    agent_id: str,
    data: UpgradeTaskCreate,
    service = Depends(get_agent_service),
    user = Depends(get_current_user)
):
    """创建升级任务"""
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="需要管理员权限")
    
    try:
        task = await service.create_upgrade_task(
            agent_id=agent_id,
            to_version=data.to_version
        )
        return UpgradeTaskResponse.from_domain(task)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/agents/{agent_id}/upgrade-tasks", response_model=List[UpgradeTaskResponse])
async def list_upgrade_tasks(
    agent_id: str,
    service = Depends(get_agent_service)
):
    """获取Agent的升级任务列表"""
    tasks = await service.task_repo.list_by_agent(agent_id)
    return [UpgradeTaskResponse.from_domain(t) for t in tasks]

@router.get("/agents/{agent_id}/metrics", response_model=List[Union[MetricsResponse, HourlyMetricsResponse]])
async def get_agent_metrics(
    agent_id: str,
    query: MetricsQuery,
    service = Depends(get_agent_service)
):
    """获取Agent指标"""
    try:
        if query.interval == "hourly":
            metrics = await service.get_hourly_metrics(
                agent_id=agent_id,
                start_time=query.start_time,
                end_time=query.end_time
            )
            return [HourlyMetricsResponse.from_domain(m) for m in metrics]
        else:
            metrics = await service.get_metrics(
                agent_id=agent_id,
                start_time=query.start_time,
                end_time=query.end_time
            )
            return [MetricsResponse.from_domain(m) for m in metrics]
            
    except MetricsNotFoundError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )
    except InvalidTimeRangeError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except AgentMetricsError as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        ) 