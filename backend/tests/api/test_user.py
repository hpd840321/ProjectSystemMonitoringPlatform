import pytest
from httpx import AsyncClient

async def test_get_user_profile(client, normal_token):
    """测试获取用户信息"""
    response = await client.get(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {normal_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "username" in data
    assert "email" in data

async def test_update_user_profile(client, normal_token):
    """测试更新用户信息"""
    response = await client.put(
        "/api/v1/users/me",
        json={
            "nickname": "New Name",
            "avatar": "new_avatar.jpg"
        },
        headers={"Authorization": f"Bearer {normal_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["nickname"] == "New Name"

async def test_change_password(client, normal_token):
    """测试修改密码"""
    response = await client.post(
        "/api/v1/users/me/password",
        json={
            "old_password": "Test123456",
            "new_password": "NewTest123456",
            "confirm_password": "NewTest123456"
        },
        headers={"Authorization": f"Bearer {normal_token}"}
    )
    assert response.status_code == 200 