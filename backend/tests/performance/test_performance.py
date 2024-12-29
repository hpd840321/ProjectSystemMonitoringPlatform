import pytest
import asyncio
import time
from concurrent.futures import ThreadPoolExecutor

async def test_api_response_time(client, normal_token):
    """测试API响应时间"""
    start_time = time.time()
    response = await client.get(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {normal_token}"}
    )
    end_time = time.time()
    
    assert response.status_code == 200
    assert end_time - start_time < 0.5  # 响应时间应小于500ms

async def test_concurrent_requests(client, normal_token):
    """测试并发请求"""
    async def make_request():
        return await client.get(
            "/api/v1/users/me",
            headers={"Authorization": f"Bearer {normal_token}"}
        )
    
    # 创建100个并发请求
    tasks = [make_request() for _ in range(100)]
    responses = await asyncio.gather(*tasks)
    
    # 验证所有请求都成功
    assert all(r.status_code == 200 for r in responses)

async def test_database_query_performance(client, admin_token):
    """测试数据库查询性能"""
    start_time = time.time()
    response = await client.get(
        "/api/v1/users",
        params={"page": 1, "page_size": 100},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    end_time = time.time()
    
    assert response.status_code == 200
    assert end_time - start_time < 1.0  # 查询时间应小于1秒 