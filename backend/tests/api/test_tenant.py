import pytest
from httpx import AsyncClient

async def test_create_tenant(client, admin_token):
    """测试创建租户"""
    response = await client.post(
        "/api/v1/tenants",
        json={
            "name": "Test Tenant",
            "code": "test",
            "description": "Test tenant description"
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Tenant"

async def test_list_tenants(client, admin_token):
    """测试获取租户列表"""
    response = await client.get(
        "/api/v1/tenants",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list) 