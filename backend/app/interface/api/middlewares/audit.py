from fastapi import Request
from app.domain.audit.service import AuditService
from app.domain.audit.aggregate import AuditAction

class AuditMiddleware:
    """审计中间件"""
    
    def __init__(self, audit_service: AuditService):
        self.audit_service = audit_service
    
    async def __call__(self, request: Request, call_next):
        # 获取当前用户
        user = request.state.user
        
        # 记录请求日志
        if user:
            await self.audit_service.log_action(
                user_id=user.id,
                action=self._get_action(request.method),
                resource_type=self._get_resource_type(request.url.path),
                resource_id=self._get_resource_id(request.url.path),
                details={
                    "method": request.method,
                    "path": request.url.path,
                    "query_params": dict(request.query_params),
                    "client_ip": request.client.host
                }
            )
        
        response = await call_next(request)
        return response
    
    def _get_action(self, method: str) -> AuditAction:
        """根据HTTP方法获取操作类型"""
        method_map = {
            "POST": AuditAction.CREATE,
            "PUT": AuditAction.UPDATE,
            "DELETE": AuditAction.DELETE
        }
        return method_map.get(method, AuditAction.UPDATE)
    
    def _get_resource_type(self, path: str) -> str:
        """从路径获取资源类型"""
        parts = path.strip("/").split("/")
        return parts[1] if len(parts) > 1 else "unknown"
    
    def _get_resource_id(self, path: str) -> Optional[str]:
        """从路径获取资源ID"""
        parts = path.strip("/").split("/")
        for i, part in enumerate(parts):
            if part.isalnum() and len(part) == 36:  # UUID格式
                return part
        return None 