import pytest

async def test_api_rate_limit(client, admin_token):
    """测试API限流"""
    # 快速连续发送请求测试限流
    for _ in range(10):
        response = await client.get(
            "/api/v1/users/me",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
    
    # 第11次请求应该被限流
    response = await client.get(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 429

async def test_api_metrics(client, admin_token):
    """测试API指标收集"""
    response = await client.get(
        "/api/v1/metrics/api",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "requests_total" in data
    assert "latency_ms" in data 