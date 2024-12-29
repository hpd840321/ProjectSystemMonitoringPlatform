import pytest

async def test_health_check(client):
    """测试系统健康检查"""
    response = await client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data
    assert "uptime" in data

async def test_component_health(client, admin_token):
    """测试组件健康状态"""
    response = await client.get(
        "/api/v1/health/components",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "database" in data
    assert "redis" in data
    assert "elasticsearch" in data 