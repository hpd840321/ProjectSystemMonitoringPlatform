from typing import Optional, List
from fastapi import Request, HTTPException, status
from app.domain.user.aggregate import UserRole

class PermissionChecker:
    """权限检查器"""
    
    def __init__(self, required_roles: Optional[List[UserRole]] = None):
        self.required_roles = required_roles or []
    
    async def __call__(self, request: Request):
        # 获取当前用户
        user = request.state.user
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated"
            )
        
        # 如果没有指定角色要求，只需要认证即可
        if not self.required_roles:
            return True
            
        # 检查项目相关权限
        project_id = request.path_params.get("project_id")
        if project_id:
            member = await self._get_project_member(project_id, user.id)
            if not member or member.role not in self.required_roles:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Permission denied"
                )
        
        return True
    
    async def _get_project_member(self, project_id: str, user_id: str):
        # TODO: 实现从数据库获取项目成员信息
        pass 