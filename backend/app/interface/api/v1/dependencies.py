from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.persistence.database import get_session
from app.infrastructure.persistence.repositories.user import (
    SQLUserRepository,
    SQLProjectMemberRepository
)
from app.domain.user.service import UserService
from app.application.user.service import UserApplicationService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

async def get_user_service(
    session: AsyncSession = Depends(get_session)
) -> UserApplicationService:
    user_repo = SQLUserRepository(session)
    member_repo = SQLProjectMemberRepository(session)
    user_service = UserService(user_repo, member_repo)
    return UserApplicationService(user_service)

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    service: UserApplicationService = Depends(get_user_service)
):
    try:
        # TODO: 实现token验证
        return await service.get_current_user(token)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        ) 