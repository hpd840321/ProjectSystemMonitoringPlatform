from fastapi import APIRouter, WebSocket, Query, HTTPException
from .events import manager
from ..api.auth import verify_token
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

async def authenticate_ws(websocket: WebSocket, token: str) -> dict:
    """WebSocket连接认证"""
    try:
        user = await verify_token(token)
        return user
    except Exception as e:
        logger.warning(f"WebSocket authentication failed: {e}")
        await websocket.close(code=4003, reason="Invalid token")
        raise HTTPException(status_code=401, detail="Invalid token")

@router.websocket("/ws/alerts")
async def alerts_ws(
    websocket: WebSocket,
    token: str = Query(...),
    retry: int = Query(0)
):
    """告警实时推送
    
    参数:
        token: 认证令牌
        retry: 重试次数，用于客户端重连
    """
    user = await authenticate_ws(websocket, token)
    logger.info(f"Alert WebSocket connection: user={user['username']}, retry={retry}")
    
    if await manager.connect(websocket, "alerts"):
        try:
            while True:
                data = await websocket.receive_text()
                if data == "ping":
                    await websocket.send_text("pong")
        except Exception as e:
            logger.error(f"Alert WebSocket error: {e}")
            manager.disconnect(websocket, "alerts")

@router.websocket("/ws/metrics")
async def metrics_ws(
    websocket: WebSocket,
    token: str = Query(...),
    retry: int = Query(0)
):
    """监控指标实时推送"""
    user = await authenticate_ws(websocket, token)
    logger.info(f"Metrics WebSocket connection: user={user['username']}, retry={retry}")
    
    if await manager.connect(websocket, "metrics"):
        try:
            while True:
                data = await websocket.receive_text()
                if data == "ping":
                    await websocket.send_text("pong")
        except Exception as e:
            logger.error(f"Metrics WebSocket error: {e}")
            manager.disconnect(websocket, "metrics")

@router.websocket("/ws/logs")
async def logs_ws(
    websocket: WebSocket,
    token: str = Query(...),
    retry: int = Query(0)
):
    """日志实时推送"""
    user = await authenticate_ws(websocket, token)
    logger.info(f"Logs WebSocket connection: user={user['username']}, retry={retry}")
    
    if await manager.connect(websocket, "logs"):
        try:
            while True:
                data = await websocket.receive_text()
                if data == "ping":
                    await websocket.send_text("pong")
        except Exception as e:
            logger.error(f"Logs WebSocket error: {e}")
            manager.disconnect(websocket, "logs") 