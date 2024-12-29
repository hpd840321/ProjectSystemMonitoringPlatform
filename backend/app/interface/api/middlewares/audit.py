from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from app.crud.audit import audit_log
from app.interface.api.v1.schemas.audit import AuditLogCreate
from datetime import datetime

class AuditMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # 记录请求开始时间
        start_time = datetime.now()
        
        response = None
        try:
            response = await call_next(request)
            status = "success"
            error_message = None
        except Exception as e:
            status = "failed"
            error_message = str(e)
            raise e
        finally:
            # 获取当前用户
            user = request.state.user if hasattr(request.state, "user") else None
            
            # 创建审计日志
            log_entry = AuditLogCreate(
                user_id=user.id if user else None,
                username=user.username if user else None,
                action=f"{request.method}:{request.url.path}",
                resource_type=request.url.path.split("/")[1],
                status=status,
                ip_address=request.client.host,
                user_agent=request.headers.get("user-agent"),
                details={
                    "method": request.method,
                    "path": str(request.url.path),
                    "query_params": str(request.query_params),
                    "duration_ms": (datetime.now() - start_time).total_seconds() * 1000
                },
                error_message=error_message
            )
            
            # 异步创建审计日志
            await audit_log.create(request.state.db, obj_in=log_entry)
            
        return response 