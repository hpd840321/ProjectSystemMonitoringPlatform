from typing import List
from datetime import datetime
from app.domain.user.service import UserService
from app.domain.user.aggregate import UserRole
from .dto import (
    UserLoginDTO,
    UserDTO,
    UserCreateDTO,
    TokenDTO,
    ProjectMemberDTO,
    AddMemberDTO
)

class UserApplicationService:
    """用户应用服务"""
    
    def __init__(self, user_service: UserService):
        self.user_service = user_service
    
    async def create_user(self, dto: UserCreateDTO) -> UserDTO:
        """创建用户"""
        user = await self.user_service.create_user(
            username=dto.username,
            email=dto.email,
            password=dto.password
        )
        return UserDTO.from_domain(user)
    
    async def login(self, dto: UserLoginDTO) -> TokenDTO:
        """用户登录"""
        user, access_token = await self.user_service.authenticate(
            username=dto.username,
            password=dto.password
        )
        return TokenDTO(
            access_token=access_token,
            token_type="bearer"
        )
    
    async def get_current_user(self, token: str) -> UserDTO:
        """获取当前用户"""
        user = await self.user_service.get_current_user(token)
        return UserDTO.from_domain(user)
    
    async def add_project_member(
        self,
        project_id: str,
        dto: AddMemberDTO
    ) -> ProjectMemberDTO:
        """添加项目成员"""
        member = await self.user_service.add_project_member(
            project_id=project_id,
            user_id=dto.user_id,
            role=UserRole(dto.role)
        )
        return ProjectMemberDTO.from_domain(member)
    
    async def remove_project_member(
        self,
        project_id: str,
        user_id: str
    ) -> None:
        """移除项目成员"""
        await self.user_service.remove_project_member(project_id, user_id) 