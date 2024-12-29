import pytest

async def test_add_tenant_member(client, admin_token):
    """测试添加租户成员"""
    # 先创建租户
    tenant_response = await client.post(
        "/api/v1/tenants",
        json={
            "name": "Test Tenant",
            "code": "test"
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    tenant_id = tenant_response.json()["id"]
    
    # 添加成员
    response = await client.post(
        f"/api/v1/tenants/{tenant_id}/users",
        json={
            "user_id": "test_user_id",
            "role": "member"
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200

async def test_list_tenant_members(client, admin_token):
    """测试获取租户成员列表"""
    response = await client.get(
        "/api/v1/tenants/1/users",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list) 