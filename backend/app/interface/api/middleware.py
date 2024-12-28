import logging
from fastapi import Request
from fastapi.responses import JSONResponse
from app.domain.common.exceptions import (
    DomainException,
    ResourceNotFoundException,
    ValidationException
)
from app.domain.audit.service import AuditService
from app.domain.audit.aggregate import AuditAction
from app.domain.user.service import get_current_user

logger = logging.getLogger(__name__)

async def exception_handler(request: Request, exc: Exception):
    """全局异常处理"""
    if isinstance(exc, ResourceNotFoundException):
        return JSONResponse(
            status_code=404,
            content={"message": str(exc)}
        )
    
    if isinstance(exc, ValidationException):
        return JSONResponse(
            status_code=400,
            content={"message": str(exc)}
        )
    
    if isinstance(exc, DomainException):
        return JSONResponse(
            status_code=400,
            content={"message": str(exc)}
        )
    
    # 未知异常记录错误日志
    logger.error(
        f"Unhandled exception: {str(exc)}",
        exc_info=True,
        extra={
            "path": request.url.path,
            "method": request.method,
            "client": request.client.host
        }
    )
    
    return JSONResponse(
        status_code=500,
        content={"message": "Internal server error"}
    ) 

class AuditMiddleware:
    """审计日志中间件"""
    
    def __init__(self, audit_service: AuditService):
        self.audit_service = audit_service
    
    async def __call__(self, request: Request, call_next):
        # 获取当前用户
        try:
            user = await get_current_user(request)
        except:
            user = None
        
        response = await call_next(request)
        
        # 记录审计日志
        if user and request.method in ["POST", "PUT", "DELETE"]:
            try:
                path_parts = request.url.path.split("/")
                if len(path_parts) >= 4:
                    resource_type = path_parts[3]  # /api/v1/{resource_type}/...
                    resource_id = path_parts[4] if len(path_parts) > 4 else None
                    
                    action = AuditAction.CREATE
                    if request.method == "PUT":
                        action = AuditAction.UPDATE
                    elif request.method == "DELETE":
                        action = AuditAction.DELETE
                    
                    await self.audit_service.log_action(
                        user_id=user.id,
                        action=action,
                        resource_type=resource_type,
                        resource_id=resource_id,
                        details={
                            "method": request.method,
                            "path": str(request.url),
                            "status_code": response.status_code
                        },
                        ip_address=request.client.host,
                        user_agent=request.headers.get("user-agent", "")
                    )
            except Exception as e:
                logger.error(f"Failed to log audit: {str(e)}", exc_info=True)
        
        return response 