import pytest

async def test_create_log_collector(client, admin_token):
    """测试创建日志采集器"""
    response = await client.post(
        "/api/v1/log-collectors",
        json={
            "name": "Nginx Access Log",
            "type": "file",
            "config": {
                "path": "/var/log/nginx/access.log",
                "pattern": "^(?P<ip>\\S+) .*"
            }
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Nginx Access Log"

async def test_search_logs(client, admin_token):
    """测试日志搜索"""
    response = await client.post(
        "/api/v1/logs/search",
        json={
            "query": "error",
            "start_time": "2024-01-01T00:00:00Z",
            "end_time": "2024-01-02T00:00:00Z",
            "limit": 100
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert "logs" in data 