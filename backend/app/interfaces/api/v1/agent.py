from fastapi import APIRouter, Depends
from typing import List, Optional
from datetime import datetime
from app.domain.models.agent import AgentData, AgentMetrics, AgentStatus
from app.application.services.agent_service import AgentService

router = APIRouter(prefix="/api/v1/agent")

@router.post("/register")
async def register_agent(agent_info: dict):
    """注册新的agent"""
    return await AgentService.register_agent(agent_info)

@router.post("/heartbeat/{agent_id}")
async def agent_heartbeat(agent_id: str, status: AgentStatus):
    """Agent心跳检测"""
    return await AgentService.update_agent_status(agent_id, status)

@router.post("/metrics/{agent_id}")
async def report_metrics(agent_id: str, metrics: List[AgentMetrics]):
    """上报监控指标"""
    return await AgentService.save_metrics(agent_id, metrics)

@router.post("/logs/{agent_id}")
async def upload_logs(agent_id: str, logs: List[dict]):
    """上传日志数据"""
    return await AgentService.process_logs(agent_id, logs) 