from fastapi import APIRouter, Request, HTTPException
from app.gateway.services.router import ServiceRouter
from app.gateway.services.discovery import ServiceDiscovery

api_router = APIRouter()
service_router = ServiceRouter()
service_discovery = ServiceDiscovery()

@api_router.api_route("/{service}/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def route_request(request: Request, service: str, path: str):
    """通用路由处理"""
    try:
        # 获取服务实例
        service_instance = await service_discovery.get_service(service)
        if not service_instance:
            raise HTTPException(status_code=404, detail=f"Service {service} not found")
            
        # 转发请求
        return await service_router.forward_request(
            request,
            service_instance,
            path
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 