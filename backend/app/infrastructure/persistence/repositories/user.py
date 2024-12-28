from datetime import datetime
from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.user.repository import UserRepository, ProjectMemberRepository
from app.domain.user.aggregate import User, ProjectMember
from ..models.user import UserModel, ProjectMemberModel

class SQLUserRepository(UserRepository):
    """SQL用户仓储实现"""
    
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, user: User) -> None:
        model = UserModel(
            id=user.id,
            username=user.username,
            email=user.email,
            password_hash=user.password_hash,
            status=user.status,
            created_at=user.created_at,
            updated_at=user.updated_at
        )
        self.session.add(model)
        await self.session.commit()

    async def get_by_id(self, user_id: str) -> Optional[User]:
        stmt = select(UserModel).where(UserModel.id == user_id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        if not model:
            return None
        return self._to_domain(model)

    async def get_by_username(self, username: str) -> Optional[User]:
        stmt = select(UserModel).where(UserModel.username == username)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        if not model:
            return None
        return self._to_domain(model)

    def _to_domain(self, model: UserModel) -> User:
        return User(
            id=model.id,
            username=model.username,
            email=model.email,
            password_hash=model.password_hash,
            status=model.status,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

class SQLProjectMemberRepository(ProjectMemberRepository):
    """SQL项目成员仓储实现"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, member: ProjectMember) -> None:
        model = ProjectMemberModel(
            project_id=member.project_id,
            user_id=member.user_id,
            role=member.role,
            joined_at=member.joined_at
        )
        self.session.add(model)
        await self.session.commit()

    async def list_by_project(self, project_id: str) -> List[ProjectMember]:
        stmt = select(ProjectMemberModel).where(
            ProjectMemberModel.project_id == project_id
        )
        result = await self.session.execute(stmt)
        return [self._to_domain(m) for m in result.scalars()]

    async def remove(self, project_id: str, user_id: str) -> None:
        stmt = select(ProjectMemberModel).where(
            ProjectMemberModel.project_id == project_id,
            ProjectMemberModel.user_id == user_id
        )
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        if model:
            await self.session.delete(model)
            await self.session.commit()

    def _to_domain(self, model: ProjectMemberModel) -> ProjectMember:
        return ProjectMember(
            project_id=model.project_id,
            user_id=model.user_id,
            role=model.role,
            joined_at=model.joined_at
        ) 