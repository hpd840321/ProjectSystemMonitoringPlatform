import pytest
from datetime import datetime

async def test_user_workflow(client):
    """测试完整的用户工作流"""
    # 1. 注册
    register_response = await client.post(
        "/api/v1/auth/register",
        json={
            "username": "integration_test",
            "email": "integration@test.com",
            "password": "Test123456",
            "confirm_password": "Test123456",
            "captcha": "1234"
        }
    )
    assert register_response.status_code == 200

    # 2. 登录
    login_response = await client.post(
        "/api/v1/auth/login",
        json={
            "username": "integration_test",
            "password": "Test123456"
        }
    )
    assert login_response.status_code == 200
    token = login_response.json()["token"]

    # 3. 更新个人信息
    update_response = await client.put(
        "/api/v1/users/me",
        json={
            "nickname": "Integration Test",
            "avatar": "test.jpg"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert update_response.status_code == 200

    # 4. 创建监控
    monitor_response = await client.post(
        "/api/v1/monitors",
        json={
            "name": "Test Monitor",
            "type": "http",
            "target": "http://example.com",
            "interval": 60
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert monitor_response.status_code == 200
    monitor_id = monitor_response.json()["id"]

    # 5. 创建告警规则
    alert_response = await client.post(
        "/api/v1/alert-rules",
        json={
            "name": "Test Alert",
            "monitor_id": monitor_id,
            "condition": {"operator": ">", "threshold": 80},
            "severity": "high"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert alert_response.status_code == 200

    # 6. 登出
    logout_response = await client.post(
        "/api/v1/auth/logout",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert logout_response.status_code == 200 