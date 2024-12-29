from .manager import manager
from datetime import datetime

async def broadcast_alert(alert: dict):
    """广播告警消息"""
    message = {
        "type": "alert",
        "data": alert,
        "timestamp": datetime.now().isoformat()
    }
    await manager.broadcast_to_project(alert["project_id"], message)

async def broadcast_metrics(server_id: str, metrics: dict):
    """广播监控数据"""
    message = {
        "type": "metrics",
        "data": metrics,
        "timestamp": datetime.now().isoformat()
    }
    await manager.broadcast_to_server(server_id, message)

async def broadcast_logs(server_id: str, logs: list):
    """广播日志数据"""
    message = {
        "type": "logs",
        "data": logs,
        "timestamp": datetime.now().isoformat()
    }
    await manager.broadcast_to_server(server_id, message)

async def broadcast_agent_status(server_id: str, status: dict):
    """广播Agent状态"""
    message = {
        "type": "agent_status",
        "data": status,
        "timestamp": datetime.now().isoformat()
    }
    await manager.broadcast_to_server(server_id, message) 