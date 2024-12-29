import pytest

async def test_unauthorized_access(client):
    """测试未授权访问"""
    response = await client.get("/api/v1/users/me")
    assert response.status_code == 401

async def test_forbidden_access(client, normal_token):
    """测试无权限访问"""
    response = await client.post(
        "/api/v1/tenants",
        json={
            "name": "Test Tenant",
            "code": "test"
        },
        headers={"Authorization": f"Bearer {normal_token}"}
    )
    assert response.status_code == 403

async def test_role_permissions(client, admin_token):
    """测试角色权限"""
    response = await client.get(
        "/api/v1/roles/1/permissions",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list) 