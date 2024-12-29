from typing import Dict, Set, Optional
from fastapi import WebSocket
from datetime import datetime
import asyncio
import logging

logger = logging.getLogger(__name__)

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, Set[WebSocket]] = {
            "alerts": set(),
            "metrics": set(),
            "logs": set()
        }
        self.heartbeat_tasks: Dict[WebSocket, asyncio.Task] = {}
    
    async def connect(self, websocket: WebSocket, channel: str) -> bool:
        """建立WebSocket连接"""
        if channel not in self.active_connections:
            await websocket.close(code=4004, reason="Invalid channel")
            return False
            
        await websocket.accept()
        self.active_connections[channel].add(websocket)
        
        # 启动心跳检测
        self.heartbeat_tasks[websocket] = asyncio.create_task(
            self._heartbeat_check(websocket, channel)
        )
        
        logger.info(f"New WebSocket connection: channel={channel}")
        return True
    
    def disconnect(self, websocket: WebSocket, channel: str):
        """断开WebSocket连接"""
        if channel in self.active_connections:
            self.active_connections[channel].discard(websocket)
        
        # 停止心跳检测
        task = self.heartbeat_tasks.pop(websocket, None)
        if task:
            task.cancel()
        
        logger.info(f"WebSocket disconnected: channel={channel}")
    
    async def _heartbeat_check(self, websocket: WebSocket, channel: str):
        """心跳检测"""
        try:
            while True:
                try:
                    # 每30秒发送一次ping
                    await asyncio.sleep(30)
                    await websocket.send_text("ping")
                    # 等待pong响应
                    await asyncio.wait_for(
                        websocket.receive_text(),
                        timeout=10
                    )
                except asyncio.TimeoutError:
                    logger.warning(f"WebSocket heartbeat timeout: channel={channel}")
                    await websocket.close(code=4000, reason="Heartbeat timeout")
                    self.disconnect(websocket, channel)
                    break
        except asyncio.CancelledError:
            pass
        except Exception as e:
            logger.error(f"WebSocket heartbeat error: {e}")
            self.disconnect(websocket, channel)
    
    async def broadcast(self, channel: str, message: dict):
        """广播消息到指定频道"""
        if channel not in self.active_connections:
            return
            
        # 添加时间戳
        message["timestamp"] = datetime.now().isoformat()
        
        for connection in self.active_connections[channel]:
            try:
                await connection.send_json(message)
            except:
                # 连接可能已断开
                await self.disconnect(connection, channel)

# 创建全局连接管理器
manager = ConnectionManager() 