from fastapi import APIRouter, Depends, HTTPException
from app.application.user.service import UserApplicationService
from app.application.user.dto import (
    UserLoginDTO,
    UserDTO,
    AddMemberDTO,
    ProjectMemberDTO,
    UserCreateDTO,
    TokenDTO
)
from .dependencies import get_user_service, get_current_user
from app.interface.api.decorators import require_roles
from app.domain.user.aggregate import UserRole

router = APIRouter()

@router.post("/auth/register", response_model=UserDTO)
async def register(
    dto: UserCreateDTO,
    service: UserApplicationService = Depends(get_user_service)
) -> UserDTO:
    """用户注册"""
    try:
        return await service.create_user(dto)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/auth/login", response_model=TokenDTO)
async def login(
    dto: UserLoginDTO,
    service: UserApplicationService = Depends(get_user_service)
) -> TokenDTO:
    """用户登录"""
    try:
        return await service.login(dto)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

@router.post(
    "/projects/{project_id}/members",
    response_model=ProjectMemberDTO,
    dependencies=[Depends(require_roles([UserRole.ADMIN, UserRole.PROJECT_ADMIN]))]
)
async def add_project_member(
    project_id: str,
    dto: AddMemberDTO,
    service: UserApplicationService = Depends(get_user_service),
    current_user = Depends(get_current_user)
) -> ProjectMemberDTO:
    """添加项目成员"""
    try:
        return await service.add_project_member(project_id, dto)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/projects/{project_id}/members/{user_id}")
async def remove_project_member(
    project_id: str,
    user_id: str,
    service: UserApplicationService = Depends(get_user_service),
    current_user = Depends(get_current_user)
) -> None:
    """移除项目成员"""
    try:
        await service.remove_project_member(project_id, user_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) 