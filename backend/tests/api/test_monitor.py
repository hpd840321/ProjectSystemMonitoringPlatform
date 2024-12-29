import pytest
from datetime import datetime, timedelta

async def test_create_monitor(client, admin_token):
    """测试创建监控项"""
    response = await client.post(
        "/api/v1/monitors",
        json={
            "name": "CPU Usage",
            "type": "system",
            "target": "cpu",
            "interval": 60,
            "config": {
                "threshold": 80,
                "duration": 300
            }
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "CPU Usage"

async def test_get_metrics(client, admin_token):
    """测试获取监控指标"""
    response = await client.get(
        "/api/v1/metrics",
        params={
            "monitor_id": 1,
            "start_time": (datetime.now() - timedelta(hours=1)).isoformat(),
            "end_time": datetime.now().isoformat()
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list) 