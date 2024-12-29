from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from .manager import manager
from ..api.v1.dependencies import get_current_user

router = APIRouter()

@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    project_id: str = None,
    server_id: str = None
):
    """WebSocket连接端点"""
    try:
        # 建立连接
        await manager.connect(websocket, project_id, server_id)
        
        while True:
            try:
                # 接收消息
                data = await websocket.receive_json()
                # TODO: 处理接收到的消息
            except WebSocketDisconnect:
                # 断开连接
                await manager.disconnect(websocket, project_id, server_id)
                break
            except Exception as e:
                logger.error(f"WebSocket error: {e}")
                break
    except Exception as e:
        logger.error(f"Failed to establish WebSocket connection: {e}") 