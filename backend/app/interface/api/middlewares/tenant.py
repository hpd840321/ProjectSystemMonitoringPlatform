from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from app.crud.tenant import tenant as tenant_crud

class TenantMiddleware(BaseHTTPMiddleware):
    """租户中间件，用于处理多租户请求"""

    async def dispatch(self, request: Request, call_next):
        # 获取租户标识
        tenant_code = request.headers.get("X-Tenant-Code")
        
        if tenant_code:
            # 获取租户信息
            db = request.state.db
            current_tenant = await tenant_crud.get_by_code(db, code=tenant_code)
            
            if current_tenant:
                if current_tenant.status != "active":
                    return JSONResponse(
                        status_code=403,
                        content={"detail": f"Tenant {tenant_code} is not active"}
                    )
                
                # 将租户信息添加到请求状态
                request.state.tenant = current_tenant
                
                # 检查用户是否属于该租户
                if hasattr(request.state, "user"):
                    user_tenant = await tenant_crud.get_user_tenants(
                        db,
                        user_id=request.state.user.id
                    )
                    if not any(ut.tenant_id == current_tenant.id for ut in user_tenant):
                        return JSONResponse(
                            status_code=403,
                            content={"detail": "User does not belong to this tenant"}
                        )
            else:
                return JSONResponse(
                    status_code=404,
                    content={"detail": f"Tenant {tenant_code} not found"}
                )
        
        response = await call_next(request)
        return response 