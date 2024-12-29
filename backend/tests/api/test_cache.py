import pytest
import time

async def test_cache_get_set(client, admin_token):
    """测试缓存的设置和获取"""
    # 设置缓存
    response = await client.post(
        "/api/v1/cache/data",
        json={
            "key": "test_key",
            "value": "test_value",
            "expire": 60
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200

    # 获取缓存
    response = await client.get(
        "/api/v1/cache/data/test_key",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    assert response.json()["value"] == "test_value"

async def test_cache_expiration(client, admin_token):
    """测试缓存过期"""
    # 设置短期缓存
    await client.post(
        "/api/v1/cache/data",
        json={
            "key": "expire_key",
            "value": "expire_value",
            "expire": 1
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    # 等待缓存过期
    time.sleep(2)

    # 获取过期缓存
    response = await client.get(
        "/api/v1/cache/data/expire_key",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 404

async def test_cache_clear(client, admin_token):
    """测试清除缓存"""
    response = await client.delete(
        "/api/v1/cache/data/test_key",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200 