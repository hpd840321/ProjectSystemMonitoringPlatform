from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from pydantic import BaseModel

class RouteConfig(BaseModel):
    """路由配置"""
    path: str
    target: str
    methods: List[str] = ["*"]
    strip_path: bool = True
    preserve_host: bool = False
    connect_timeout: int = 60000
    write_timeout: int = 60000
    read_timeout: int = 60000
    retries: int = 5

class PluginConfig(BaseModel):
    """网关插件配置"""
    name: str
    enabled: bool = True
    config: Dict[str, Any] = {}

class ServiceConfig(BaseModel):
    """服务配置"""
    name: str
    host: str
    port: int
    protocol: str = "http"
    path: str = "/"
    retries: int = 5
    connect_timeout: int = 60000
    routes: List[RouteConfig]
    plugins: List[PluginConfig] = []

class GatewayPlugin(ABC):
    """网关插件基类"""

    @abstractmethod
    async def pre_request(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """请求前处理"""
        pass

    @abstractmethod
    async def post_request(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """请求后处理"""
        pass

    @abstractmethod
    async def on_error(self, context: Dict[str, Any], error: Exception) -> None:
        """错误处理"""
        pass 