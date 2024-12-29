import pytest
from fastapi.testclient import TestClient
from fastapi.websockets import WebSocket

async def test_websocket_connection(client, normal_token):
    """测试WebSocket连接"""
    with client.websocket_connect(
        f"/ws/notifications?token={normal_token}"
    ) as websocket:
        data = websocket.receive_json()
        assert data["type"] == "connection_established"

async def test_alert_notification(client, admin_token):
    """测试告警实时推送"""
    # 创建WebSocket连接
    with client.websocket_connect(
        f"/ws/notifications?token={admin_token}"
    ) as websocket:
        # 触发一个告警
        await client.post(
            "/api/v1/alerts",
            json={
                "level": "critical",
                "message": "Test alert",
                "source": "test"
            },
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        
        # 验证收到告警通知
        data = websocket.receive_json()
        assert data["type"] == "alert"
        assert data["data"]["message"] == "Test alert"

async def test_broadcast_message(client, admin_token):
    """测试广播消息"""
    with client.websocket_connect(
        f"/ws/notifications?token={admin_token}"
    ) as websocket:
        await client.post(
            "/api/v1/notifications/broadcast",
            json={
                "message": "System maintenance",
                "level": "info"
            },
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        
        data = websocket.receive_json()
        assert data["type"] == "broadcast"
        assert "System maintenance" in data["data"]["message"] 