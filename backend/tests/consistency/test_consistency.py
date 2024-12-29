import pytest
import asyncio
from datetime import datetime, timedelta

async def test_transaction_consistency(client, admin_token):
    """测试事务一致性"""
    # 创建测试数据
    create_response = await client.post(
        "/api/v1/users",
        json={
            "username": "test_user",
            "email": "test@example.com",
            "password": "Test123456"
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert create_response.status_code == 200
    user_id = create_response.json()["id"]
    
    try:
        # 模拟失败的事务
        response = await client.post(
            "/api/v1/users/batch",
            json={
                "operations": [
                    {"type": "update", "id": user_id, "data": {"status": "active"}},
                    {"type": "update", "id": "invalid_id", "data": {"status": "active"}}
                ]
            },
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert response.status_code == 400
        
        # 验证数据未被部分更新
        user_response = await client.get(
            f"/api/v1/users/{user_id}",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert user_response.json()["status"] != "active"
        
    finally:
        # 清理测试数据
        await client.delete(
            f"/api/v1/users/{user_id}",
            headers={"Authorization": f"Bearer {admin_token}"}
        )

async def test_cache_consistency(client, admin_token):
    """测试缓存一致性"""
    # 创建测试数据
    response = await client.post(
        "/api/v1/settings",
        json={"key": "test_key", "value": "test_value"},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    
    # 更新数据
    update_response = await client.put(
        "/api/v1/settings/test_key",
        json={"value": "new_value"},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert update_response.status_code == 200
    
    # 立即读取数据，验证缓存是否同步
    get_response = await client.get(
        "/api/v1/settings/test_key",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert get_response.json()["value"] == "new_value"

async def test_concurrent_modifications(client, admin_token):
    """测试并发修改"""
    # 创建测试资源
    create_response = await client.post(
        "/api/v1/resources",
        json={"name": "test_resource", "value": 0},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    resource_id = create_response.json()["id"]
    
    async def update_resource():
        return await client.put(
            f"/api/v1/resources/{resource_id}",
            json={"value": 1},
            headers={"Authorization": f"Bearer {admin_token}"}
        )
    
    # 并发更新
    tasks = [update_resource() for _ in range(10)]
    responses = await asyncio.gather(*tasks)
    
    # 验证最终状态
    get_response = await client.get(
        f"/api/v1/resources/{resource_id}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert get_response.json()["value"] == 1 