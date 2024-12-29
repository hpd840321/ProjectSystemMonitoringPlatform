from typing import Dict, Any
from app.infrastructure.gateway.base import GatewayPlugin
from app.core.security import verify_token

class AuthPlugin(GatewayPlugin):
    """认证插件"""

    async def pre_request(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """请求前处理"""
        # 检查是否需要认证
        if self._need_auth(context["path"]):
            token = context["headers"].get("Authorization")
            if not token:
                raise ValueError("Missing authorization token")
            
            # 验证token
            payload = await verify_token(token.replace("Bearer ", ""))
            context["user"] = payload
            
        return context

    async def post_request(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """请求后处理"""
        return context

    async def on_error(self, context: Dict[str, Any], error: Exception) -> None:
        """错误处理"""
        pass

    def _need_auth(self, path: str) -> bool:
        """判断是否需要认证"""
        # 这里可以配置白名单
        whitelist = ["/api/v1/auth/login", "/api/v1/docs"]
        return path not in whitelist

class RateLimitPlugin(GatewayPlugin):
    """限流插件"""
    
    def __init__(self, rate_limit: int = 100):
        self._rate_limit = rate_limit
        self._counters = {}

    async def pre_request(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """请求前处理"""
        client_ip = context["client"]["host"]
        
        # 简单的计数器限流
        if client_ip not in self._counters:
            self._counters[client_ip] = 1
        else:
            self._counters[client_ip] += 1
            
        if self._counters[client_ip] > self._rate_limit:
            raise ValueError("Rate limit exceeded")
            
        return context

    async def post_request(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """请求后处理"""
        return context

    async def on_error(self, context: Dict[str, Any], error: Exception) -> None:
        """错误处理"""
        pass

class LoggingPlugin(GatewayPlugin):
    """日志插件"""

    async def pre_request(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """请求前处理"""
        logger.info(
            f"Gateway request: {context['method']} {context['path']} "
            f"from {context['client']['host']}"
        )
        return context

    async def post_request(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """请求后处理"""
        response = context.get("response")
        if response:
            logger.info(
                f"Gateway response: {response.status_code} for "
                f"{context['method']} {context['path']}"
            )
        return context

    async def on_error(self, context: Dict[str, Any], error: Exception) -> None:
        """错误处理"""
        logger.error(
            f"Gateway error: {str(error)} for "
            f"{context['method']} {context['path']}"
        ) 