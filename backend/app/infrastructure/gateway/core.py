import aiohttp
import logging
from typing import Dict, Any, List, Optional
from fastapi import Request, Response
from urllib.parse import urljoin

from app.infrastructure.gateway.base import (
    ServiceConfig,
    RouteConfig,
    GatewayPlugin
)
from app.infrastructure.discovery.client import discovery_client

logger = logging.getLogger(__name__)

class APIGateway:
    """API网关核心"""

    def __init__(self):
        self._services: Dict[str, ServiceConfig] = {}
        self._plugins: Dict[str, GatewayPlugin] = {}
        self._routes: Dict[str, RouteConfig] = {}

    def add_service(self, service: ServiceConfig) -> None:
        """添加服务"""
        self._services[service.name] = service
        for route in service.routes:
            self._routes[route.path] = route

    def remove_service(self, service_name: str) -> None:
        """移除服务"""
        if service_name in self._services:
            service = self._services[service_name]
            for route in service.routes:
                self._routes.pop(route.path, None)
            del self._services[service_name]

    def register_plugin(self, name: str, plugin: GatewayPlugin) -> None:
        """注册插件"""
        self._plugins[name] = plugin

    def unregister_plugin(self, name: str) -> None:
        """注销插件"""
        self._plugins.pop(name, None)

    async def handle_request(self, request: Request) -> Response:
        """处理请求"""
        context = {
            "request": request,
            "path": request.url.path,
            "method": request.method,
            "headers": dict(request.headers),
            "query_params": dict(request.query_params),
            "client": {
                "host": request.client.host,
                "port": request.client.port
            }
        }

        try:
            # 运行前置插件
            for plugin in self._plugins.values():
                context = await plugin.pre_request(context)

            # 查找路由
            route = self._find_route(context["path"])
            if not route:
                return Response(
                    content="Service not found",
                    status_code=404
                )

            # 转发请求
            response = await self._forward_request(route, context)
            
            # 运行后置插件
            for plugin in self._plugins.values():
                context = await plugin.post_request({
                    **context,
                    "response": response
                })

            return response

        except Exception as e:
            logger.error(f"Gateway error: {str(e)}")
            # 运行错误处理插件
            for plugin in self._plugins.values():
                await plugin.on_error(context, e)
            return Response(
                content="Internal gateway error",
                status_code=500
            )

    def _find_route(self, path: str) -> Optional[RouteConfig]:
        """查找路由"""
        # 这里可以实现更复杂的路由匹配逻辑
        return self._routes.get(path)

    async def _forward_request(
        self,
        route: RouteConfig,
        context: Dict[str, Any]
    ) -> Response:
        """转发请求"""
        # 从服务发现获取服务实例
        service_instance = await discovery_client.get_service(route.target)
        if not service_instance:
            return Response(
                content="Service unavailable",
                status_code=503
            )
        
        # 构建目标URL
        target_url = f"{service_instance.protocol}://{service_instance.host}:{service_instance.port}"
        if route.strip_path:
            path = context["path"].replace(route.path, "", 1)
        else:
            path = context["path"]
        url = urljoin(target_url, path)

        # 转发请求
        async with aiohttp.ClientSession() as session:
            async with session.request(
                method=context["method"],
                url=url,
                headers=context["headers"],
                params=context["query_params"],
                timeout=aiohttp.ClientTimeout(
                    total=route.read_timeout / 1000,
                    connect=route.connect_timeout / 1000
                )
            ) as response:
                return Response(
                    content=await response.read(),
                    status_code=response.status,
                    headers=dict(response.headers)
                )

gateway = APIGateway() 