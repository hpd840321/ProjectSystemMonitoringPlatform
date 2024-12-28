from datetime import datetime
from typing import Optional
from uuid import uuid4
from .repository import UserRepository, ProjectMemberRepository
from .aggregate import User, ProjectMember, UserRole
from .exceptions import UserNotFoundError, InvalidPasswordError
from app.infrastructure.security.password import hash_password, verify_password
from app.infrastructure.security.jwt import create_access_token, verify_token

class UserService:
    """用户领域服务"""
    
    def __init__(
        self,
        user_repo: UserRepository,
        member_repo: ProjectMemberRepository
    ):
        self.user_repo = user_repo
        self.member_repo = member_repo
    
    async def create_user(
        self,
        username: str,
        email: str,
        password: str
    ) -> User:
        """创建用户"""
        now = datetime.now()
        user = User(
            id=str(uuid4()),
            username=username,
            email=email,
            password_hash=hash_password(password),
            status="active",
            created_at=now,
            updated_at=now
        )
        await self.user_repo.save(user)
        return user
    
    async def authenticate(self, username: str, password: str) -> tuple[User, str]:
        """用户认证"""
        user = await self.user_repo.get_by_username(username)
        if not user:
            raise UserNotFoundError("User not found")
            
        if not verify_password(password, user.password_hash):
            raise InvalidPasswordError("Invalid password")
        
        # 生成访问令牌    
        access_token = create_access_token(user)
        return user, access_token
    
    async def get_current_user(self, token: str) -> User:
        """获取当前用户"""
        payload = verify_token(token)
        if not payload:
            raise ValueError("Invalid token")
            
        user = await self.user_repo.get_by_id(payload["sub"])
        if not user:
            raise UserNotFoundError("User not found")
            
        return user
    
    async def add_project_member(
        self,
        project_id: str,
        user_id: str,
        role: UserRole
    ) -> ProjectMember:
        """添加项目成员"""
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise UserNotFoundError("User not found")
            
        member = ProjectMember(
            user_id=user_id,
            project_id=project_id,
            role=role,
            joined_at=datetime.now()
        )
        
        await self.member_repo.save(member)
        return member
    
    async def remove_project_member(self, project_id: str, user_id: str) -> None:
        """移除项目成员"""
        await self.member_repo.remove(project_id, user_id)
    
    def _verify_password(self, password: str, password_hash: str) -> bool:
        """验证密码"""
        # TODO: 实现密码验证
        return True 