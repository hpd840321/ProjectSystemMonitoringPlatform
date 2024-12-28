from typing import List, Optional
from fastapi import HTTPException, status
from app.domain.user.aggregate import User, UserRole

def check_project_permission(
    user: User,
    project_id: str,
    required_roles: Optional[List[UserRole]] = None
) -> bool:
    """检查项目权限"""
    # 超级管理员拥有所有权限
    if user.role in settings.SUPER_ADMIN_ROLES:
        return True
        
    # 获取用户在项目中的角色
    member = get_project_member(project_id, user.id)
    if not member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not a project member"
        )
    
    # 检查角色权限
    if required_roles and member.role not in required_roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions"
        )
    
    return True

def check_server_permission(
    user: User,
    server_id: str,
    required_roles: Optional[List[UserRole]] = None
) -> bool:
    """检查服务器权限"""
    # 获取服务器所属项目
    server = get_server(server_id)
    if not server:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Server not found"
        )
    
    # 检查项目权限
    return check_project_permission(user, server.project_id, required_roles) 