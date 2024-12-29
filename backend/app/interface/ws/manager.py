from typing import Dict, Set
from fastapi import WebSocket
import json
import logging

logger = logging.getLogger(__name__)

class ConnectionManager:
    def __init__(self):
        # 所有连接
        self.active_connections: Set[WebSocket] = set()
        # 按项目分组的连接
        self.project_connections: Dict[str, Set[WebSocket]] = {}
        # 按服务器分组的连接
        self.server_connections: Dict[str, Set[WebSocket]] = {}
    
    async def connect(
        self,
        websocket: WebSocket,
        project_id: str = None,
        server_id: str = None
    ):
        """建立连接"""
        await websocket.accept()
        self.active_connections.add(websocket)
        
        if project_id:
            if project_id not in self.project_connections:
                self.project_connections[project_id] = set()
            self.project_connections[project_id].add(websocket)
        
        if server_id:
            if server_id not in self.server_connections:
                self.server_connections[server_id] = set()
            self.server_connections[server_id].add(websocket)
        
        logger.info(f"New WebSocket connection: {websocket.client}")
    
    async def disconnect(
        self,
        websocket: WebSocket,
        project_id: str = None,
        server_id: str = None
    ):
        """断开连接"""
        self.active_connections.remove(websocket)
        
        if project_id and project_id in self.project_connections:
            self.project_connections[project_id].remove(websocket)
            if not self.project_connections[project_id]:
                del self.project_connections[project_id]
        
        if server_id and server_id in self.server_connections:
            self.server_connections[server_id].remove(websocket)
            if not self.server_connections[server_id]:
                del self.server_connections[server_id]
        
        logger.info(f"WebSocket disconnected: {websocket.client}")
    
    async def broadcast(self, message: dict):
        """广播消息到所有连接"""
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception as e:
                logger.error(f"Failed to send message: {e}")
    
    async def broadcast_to_project(self, project_id: str, message: dict):
        """广播消息到项目的所有连接"""
        if project_id not in self.project_connections:
            return
        
        for connection in self.project_connections[project_id]:
            try:
                await connection.send_json(message)
            except Exception as e:
                logger.error(f"Failed to send message to project {project_id}: {e}")
    
    async def broadcast_to_server(self, server_id: str, message: dict):
        """广播消息到服务器的所有连接"""
        if server_id not in self.server_connections:
            return
        
        for connection in self.server_connections[server_id]:
            try:
                await connection.send_json(message)
            except Exception as e:
                logger.error(f"Failed to send message to server {server_id}: {e}")

# 全局WebSocket连接管理器
manager = ConnectionManager() 