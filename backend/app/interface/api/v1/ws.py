from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query
from typing import Dict, Set
from ..auth import verify_token
import logging
from datetime import datetime

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/ws")

# 存储活跃的WebSocket连接
connections: Dict[str, Set[WebSocket]] = {
    "alerts": set(),
    "metrics": set(),
    "logs": set()
}

@router.websocket("/alerts")
async def alerts_ws(
    websocket: WebSocket,
    token: str = Query(...)
):
    """告警实时推送"""
    try:
        # 验证token
        user = await verify_token(token)
        
        await websocket.accept()
        connections["alerts"].add(websocket)
        logger.info(f"Alert WebSocket connected: user={user['username']}")
        
        try:
            while True:
                await websocket.receive_text()
        except WebSocketDisconnect:
            connections["alerts"].remove(websocket)
            logger.info(f"Alert WebSocket disconnected: user={user['username']}")
    except Exception as e:
        logger.error(f"Alert WebSocket error: {e}")
        await websocket.close(code=4003)

@router.websocket("/metrics")
async def metrics_ws(
    websocket: WebSocket,
    token: str = Query(...)
):
    """监控指标实时推送"""
    try:
        user = await verify_token(token)
        
        await websocket.accept()
        connections["metrics"].add(websocket)
        logger.info(f"Metrics WebSocket connected: user={user['username']}")
        
        try:
            while True:
                await websocket.receive_text()
        except WebSocketDisconnect:
            connections["metrics"].remove(websocket)
            logger.info(f"Metrics WebSocket disconnected: user={user['username']}")
    except Exception as e:
        logger.error(f"Metrics WebSocket error: {e}")
        await websocket.close(code=4003)

@router.websocket("/logs")
async def logs_ws(
    websocket: WebSocket,
    token: str = Query(...)
):
    """日志实时推送"""
    try:
        user = await verify_token(token)
        
        await websocket.accept()
        connections["logs"].add(websocket)
        logger.info(f"Logs WebSocket connected: user={user['username']}")
        
        try:
            while True:
                await websocket.receive_text()
        except WebSocketDisconnect:
            connections["logs"].remove(websocket)
            logger.info(f"Logs WebSocket disconnected: user={user['username']}")
    except Exception as e:
        logger.error(f"Logs WebSocket error: {e}")
        await websocket.close(code=4003)

# 广播消息的辅助函数
async def broadcast_alert(alert: dict):
    """广播告警消息"""
    for ws in list(connections["alerts"]):
        try:
            await ws.send_json({
                "type": "alert",
                "data": alert,
                "timestamp": datetime.now().isoformat()
            })
        except Exception as e:
            logger.error(f"Failed to broadcast alert: {e}")
            try:
                connections["alerts"].remove(ws)
            except KeyError:
                pass

async def broadcast_metrics(metrics: dict):
    """广播监控指标"""
    for ws in list(connections["metrics"]):
        try:
            await ws.send_json({
                "type": "metric",
                "data": metrics,
                "timestamp": datetime.now().isoformat()
            })
        except Exception as e:
            logger.error(f"Failed to broadcast metrics: {e}")
            try:
                connections["metrics"].remove(ws)
            except KeyError:
                pass

async def broadcast_logs(log: dict):
    """广播日志消息"""
    for ws in list(connections["logs"]):
        try:
            await ws.send_json({
                "type": "log",
                "data": log,
                "timestamp": datetime.now().isoformat()
            })
        except Exception as e:
            logger.error(f"Failed to broadcast log: {e}")
            try:
                connections["logs"].remove(ws)
            except KeyError:
                pass

@router.on_event("startup")
async def startup():
    """启动时初始化连接管理"""
    global connections
    connections = {
        "alerts": set(),
        "metrics": set(),
        "logs": set()
    }
    logger.info("WebSocket connections initialized")

@router.on_event("shutdown") 
async def shutdown():
    """关闭时清理所有连接"""
    for channel, connections in connections.items():
        count = len(connections)
        for ws in connections:
            try:
                await ws.close(code=1001)  # Going Away
            except:
                pass
        logger.info(f"Closed {count} {channel} WebSocket connections")
    connections.clear() 