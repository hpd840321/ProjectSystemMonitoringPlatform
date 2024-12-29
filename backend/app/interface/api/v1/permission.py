from typing import List, Set
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.interface.api.v1.dependencies import get_db, get_current_user
from app.interface.api.v1.schemas.permission import (
    PermissionCreate,
    PermissionUpdate,
    PermissionInDB,
    RoleCreate,
    RoleUpdate,
    RoleInDB,
    UserRoleUpdate
)
from app.crud import permission, role
from app.models.user import User

router = APIRouter()

# 权限管理接口
@router.get("/permissions", response_model=List[PermissionInDB])
async def list_permissions(
    skip: int = 0,
    limit: int = 100,
    module: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取权限列表"""
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    if module:
        return await permission.get_by_module(db, module=module)
    return await permission.get_multi(db, skip=skip, limit=limit)

@router.post("/permissions", response_model=PermissionInDB)
async def create_permission(
    permission_in: PermissionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """创建权限"""
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    db_obj = await permission.get_by_code(db, code=permission_in.code)
    if db_obj:
        raise HTTPException(
            status_code=400,
            detail="Permission with this code already exists"
        )
    return await permission.create(db, obj_in=permission_in)

# 角色管理接口
@router.get("/roles", response_model=List[RoleInDB])
async def list_roles(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取角色列表"""
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return await role.get_multi(db, skip=skip, limit=limit)

@router.post("/roles", response_model=RoleInDB)
async def create_role(
    role_in: RoleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """创建角色"""
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    db_obj = await role.get_by_name(db, name=role_in.name)
    if db_obj:
        raise HTTPException(
            status_code=400,
            detail="Role with this name already exists"
        )
    return await role.create(db, obj_in=role_in)

@router.get("/roles/{role_id}", response_model=RoleInDB)
async def get_role(
    role_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取角色详情"""
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    db_obj = await role.get(db, id=role_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Role not found")
    return db_obj

@router.put("/roles/{role_id}", response_model=RoleInDB)
async def update_role(
    role_id: int,
    role_in: RoleUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """更新角色"""
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    db_obj = await role.get(db, id=role_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Role not found")
    if db_obj.is_system:
        raise HTTPException(status_code=400, detail="Cannot modify system role")
    return await role.update(db, db_obj=db_obj, obj_in=role_in)

@router.delete("/roles/{role_id}")
async def delete_role(
    role_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """删除角色"""
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    db_obj = await role.get(db, id=role_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Role not found")
    if db_obj.is_system:
        raise HTTPException(status_code=400, detail="Cannot delete system role")
    
    await role.delete(db, id=role_id)
    return {"msg": "Role deleted successfully"}

# 用户角色管理接口
@router.get("/users/{user_id}/roles", response_model=List[RoleInDB])
async def get_user_roles(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取用户的角色列表"""
    if not current_user.is_superuser and current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return await role.get_user_roles(db, user_id=user_id)

@router.put("/users/{user_id}/roles")
async def update_user_roles(
    user_id: int,
    role_update: UserRoleUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """更新用户的角色"""
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    await role.assign_users(db, role_id=role_update.role_ids, user_ids=[user_id])
    return {"msg": "User roles updated successfully"}

@router.get("/users/{user_id}/permissions", response_model=Set[str])
async def get_user_permissions(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取用户的所有权限"""
    if not current_user.is_superuser and current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return await role.get_user_permissions(db, user_id=user_id) 