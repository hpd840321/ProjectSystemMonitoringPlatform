from fastapi import Request
import aiohttp
from app.gateway.services.discovery import ServiceInstance

class ServiceRouter:
    async def forward_request(
        self,
        request: Request,
        service: ServiceInstance,
        path: str
    ):
        """转发请求到目标服务"""
        target_url = f"http://{service.host}:{service.port}/{path}"
        
        # 获取原始请求数据
        body = await request.body()
        headers = dict(request.headers)
        
        async with aiohttp.ClientSession() as session:
            async with session.request(
                method=request.method,
                url=target_url,
                headers=headers,
                data=body
            ) as response:
                return await response.json() 