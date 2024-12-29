import pytest
import asyncio
import time
from concurrent.futures import ThreadPoolExecutor
from locust import HttpUser, task, between

class StressTest:
    """压力测试基类"""
    async def test_high_concurrency(client, admin_token):
        """高并发测试"""
        async def make_request():
            return await client.get(
                "/api/v1/system/resources",
                headers={"Authorization": f"Bearer {admin_token}"}
            )
        
        # 创建1000个并发请求
        start_time = time.time()
        tasks = [make_request() for _ in range(1000)]
        responses = await asyncio.gather(*tasks)
        end_time = time.time()
        
        # 验证响应
        success_count = sum(1 for r in responses if r.status_code == 200)
        total_time = end_time - start_time
        
        assert success_count >= 950  # 95%成功率
        assert total_time < 30  # 30秒内完成

    async def test_long_connection(client, normal_token):
        """长连接测试"""
        async with client.websocket_connect(
            f"/ws/notifications?token={normal_token}"
        ) as websocket:
            # 保持连接10秒
            for _ in range(10):
                await asyncio.sleep(1)
                await websocket.send_json({"type": "ping"})
                data = await websocket.receive_json()
                assert data["type"] == "pong"

    async def test_large_data_transfer(client, admin_token):
        """大数据传输测试"""
        # 生成1MB的测试数据
        large_data = "x" * (1024 * 1024)
        
        response = await client.post(
            "/api/v1/data/process",
            json={"data": large_data},
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert response.status_code == 200 