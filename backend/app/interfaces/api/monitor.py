from fastapi import APIRouter, Depends
from typing import List

from app.application.monitor.service import MonitoringService
from app.domain.monitor.entity import LogEntry, ResourceMetric

router = APIRouter()

@router.post("/agent/register")
async def register_agent(agent_info: dict):
    """注册Agent"""
    return await MonitoringService.register_agent(agent_info)

@router.post("/data/logs")
async def receive_logs(logs: List[LogEntry]):
    """接收日志数据"""
    return await MonitoringService.process_logs(logs)

@router.post("/data/metrics")
async def receive_metrics(metrics: List[ResourceMetric]):
    """接收资源指标"""
    return await MonitoringService.process_metrics(metrics) 