from functools import wraps
from typing import List, Optional
from fastapi import HTTPException, status
from app.domain.user.aggregate import UserRole

def require_roles(roles: Optional[List[UserRole]] = None):
    """角色权限检查装饰器"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            request = kwargs.get("request")
            if not request:
                raise ValueError("Missing request parameter")
                
            user = request.state.user
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated"
                )
            
            if roles:
                project_id = kwargs.get("project_id")
                if project_id:
                    member = await get_project_member(project_id, user.id)
                    if not member or member.role not in roles:
                        raise HTTPException(
                            status_code=status.HTTP_403_FORBIDDEN,
                            detail="Permission denied"
                        )
            
            return await func(*args, **kwargs)
        return wrapper
    return decorator 