from fastapi import WebSocket, WebSocketDisconnect
from typing import Dict
import json
import logging
from ...domain.agent.service import AgentService
from ...domain.agent.aggregate import AgentStatus
from ...domain.agent.metrics import AgentMetrics
from datetime import datetime
from uuid import uuid4

logger = logging.getLogger(__name__)

class AgentWebSocketManager:
    """Agent WebSocket连接管理器"""
    
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
    
    async def connect(self, agent_id: str, websocket: WebSocket):
        """建立连接"""
        await websocket.accept()
        self.active_connections[agent_id] = websocket
    
    def disconnect(self, agent_id: str):
        """断开连接"""
        self.active_connections.pop(agent_id, None)
    
    async def broadcast(self, message: dict):
        """广播消息"""
        for websocket in self.active_connections.values():
            try:
                await websocket.send_json(message)
            except Exception as e:
                logger.error(f"Failed to broadcast message: {str(e)}")

ws_manager = AgentWebSocketManager()

async def agent_websocket_endpoint(
    websocket: WebSocket,
    agent_id: str,
    service: AgentService
):
    """Agent WebSocket处理"""
    try:
        await ws_manager.connect(agent_id, websocket)
        
        # 更新Agent状态为在线
        agent = await service.agent_repo.get_by_id(agent_id)
        if agent:
            agent.status = AgentStatus.ONLINE
            await service.agent_repo.save(agent)
        
        while True:
            # 接收消息
            data = await websocket.receive_text()
            message = json.loads(data)
            
            # 处理不同类型的消息
            msg_type = message.get("type")
            if msg_type == "heartbeat":
                # 更新心跳
                await service.update_heartbeat(agent_id)
            elif msg_type == "metrics":
                # 处理指标数据
                data = message.get("data", {})
                metrics = AgentMetrics(
                    id=str(uuid4()),
                    agent_id=agent_id,
                    timestamp=datetime.fromisoformat(message["timestamp"]),
                    cpu_percent=data["cpu_percent"],
                    memory_percent=data["memory_percent"],
                    disk_usage=data["disk_usage"],
                    network_in=data["network"]["bytes_recv"],
                    network_out=data["network"]["bytes_sent"],
                    created_at=datetime.now()
                )
                await service.metrics_repo.save_metrics(metrics)
            elif msg_type == "upgrade_result":
                # 处理升级结果
                status = message.get("status")
                error = message.get("error")
                task_id = message.get("task_id")
                await service.update_task_status(task_id, status, error)
    
    except WebSocketDisconnect:
        # 断开连接时更新状态
        if agent:
            agent.status = AgentStatus.OFFLINE
            await service.agent_repo.save(agent)
    
    finally:
        ws_manager.disconnect(agent_id) 