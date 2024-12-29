from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.interface.api.v1.dependencies import get_db, get_current_user
from app.interface.api.v1.schemas.tenant import (
    TenantCreate,
    TenantUpdate,
    TenantInDB,
    UserTenantCreate,
    UserTenantUpdate,
    UserTenantInDB,
    TenantStats
)
from app.crud import tenant
from app.models.user import User
from app.application.tenant.service import TenantApplicationService
from app.application.tenant.dto import TenantDTO

router = APIRouter()

@router.get("/tenants", response_model=List[TenantInDB])
async def list_tenants(
    status: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取租户列表"""
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return await tenant.get_multi(db, skip=skip, limit=limit, status=status)

@router.post("/tenants", response_model=TenantInDB)
async def create_tenant(
    tenant_in: TenantCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """创建租户"""
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    db_obj = await tenant.get_by_code(db, code=tenant_in.code)
    if db_obj:
        raise HTTPException(
            status_code=400,
            detail="Tenant with this code already exists"
        )
    return await tenant.create(db, obj_in=tenant_in)

@router.put("/tenants/{tenant_id}", response_model=TenantInDB)
async def update_tenant(
    tenant_id: int,
    tenant_in: TenantUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """更新租户"""
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    db_obj = await tenant.get(db, id=tenant_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Tenant not found")
    return await tenant.update(db, db_obj=db_obj, obj_in=tenant_in)

@router.delete("/tenants/{tenant_id}")
async def delete_tenant(
    tenant_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """删除租户"""
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    await tenant.delete(db, id=tenant_id)
    return {"msg": "Tenant deleted successfully"}

@router.get("/tenants/{tenant_id}/stats", response_model=TenantStats)
async def get_tenant_stats(
    tenant_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取租户统计信息"""
    if not current_user.is_superuser:
        user_tenants = await tenant.get_user_tenants(db, user_id=current_user.id)
        if not any(ut.tenant_id == tenant_id for ut in user_tenants):
            raise HTTPException(status_code=403, detail="Not enough permissions")
    
    return await tenant.get_tenant_stats(db, tenant_id=tenant_id)

@router.post("/tenants/{tenant_id}/users", response_model=UserTenantInDB)
async def add_user_to_tenant(
    tenant_id: int,
    user_tenant_in: UserTenantCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """添加用户到租户"""
    if not current_user.is_superuser:
        user_tenants = await tenant.get_user_tenants(db, user_id=current_user.id)
        if not any(ut.tenant_id == tenant_id and ut.role == "owner" for ut in user_tenants):
            raise HTTPException(status_code=403, detail="Not enough permissions")
    
    return await tenant.add_user_to_tenant(db, obj_in=user_tenant_in)

@router.put("/tenants/{tenant_id}/users/{user_id}", response_model=UserTenantInDB)
async def update_user_role(
    tenant_id: int,
    user_id: int,
    role_in: UserTenantUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """更新用户在租户中的角色"""
    if not current_user.is_superuser:
        user_tenants = await tenant.get_user_tenants(db, user_id=current_user.id)
        if not any(ut.tenant_id == tenant_id and ut.role == "owner" for ut in user_tenants):
            raise HTTPException(status_code=403, detail="Not enough permissions")
    
    return await tenant.update_user_role(
        db,
        user_id=user_id,
        tenant_id=tenant_id,
        obj_in=role_in
    )

@router.delete("/tenants/{tenant_id}/users/{user_id}")
async def remove_user_from_tenant(
    tenant_id: int,
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """从租户中移除用户"""
    if not current_user.is_superuser:
        user_tenants = await tenant.get_user_tenants(db, user_id=current_user.id)
        if not any(ut.tenant_id == tenant_id and ut.role == "owner" for ut in user_tenants):
            raise HTTPException(status_code=403, detail="Not enough permissions")
    
    success = await tenant.remove_user_from_tenant(
        db,
        user_id=user_id,
        tenant_id=tenant_id
    )
    if not success:
        raise HTTPException(status_code=404, detail="User not found in tenant")
    return {"msg": "User removed from tenant successfully"}

@router.get("")
async def list_tenants(
    service: TenantApplicationService = Depends()
) -> List[TenantDTO]:
    """获取租户列表"""
    return await service.list_active_tenants() 