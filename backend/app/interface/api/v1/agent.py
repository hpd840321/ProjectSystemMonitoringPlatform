from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict
from app.application.agent.service import AgentApplicationService
from app.application.agent.dto import (
    AgentDTO,
    AgentRegisterDTO,
    AgentMetricsDTO
)
from .dependencies import get_agent_service, get_current_user

router = APIRouter()

@router.post("/agents/register", response_model=AgentDTO)
async def register_agent(
    dto: AgentRegisterDTO,
    service: AgentApplicationService = Depends(get_agent_service)
) -> AgentDTO:
    """注册Agent"""
    return await service.register_agent(dto)

@router.get("/agents/{agent_id}", response_model=AgentDTO)
async def get_agent(
    agent_id: str,
    service: AgentApplicationService = Depends(get_agent_service),
    current_user = Depends(get_current_user)
) -> AgentDTO:
    """获取Agent信息"""
    agent = await service.get_agent(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent

@router.get("/servers/{server_id}/agents", response_model=List[AgentDTO])
async def list_server_agents(
    server_id: str,
    service: AgentApplicationService = Depends(get_agent_service),
    current_user = Depends(get_current_user)
) -> List[AgentDTO]:
    """获取服务器的Agent列表"""
    return await service.list_server_agents(server_id)

@router.post("/agents/{agent_id}/heartbeat")
async def update_heartbeat(
    agent_id: str,
    metrics: Dict = None,
    service: AgentApplicationService = Depends(get_agent_service)
) -> None:
    """更新Agent心跳"""
    await service.update_heartbeat(agent_id, metrics) 