from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.interface.api.v1.dependencies import get_db
from app.interface.api.v1.schemas.storage import (
    StoragePolicyCreate,
    StoragePolicyUpdate,
    StoragePolicyInDB,
    StoragePolicyExecution
)
from app.crud import storage_policy

router = APIRouter()

@router.post("/storage-policies", response_model=StoragePolicyInDB)
async def create_storage_policy(
    policy_in: StoragePolicyCreate,
    db: Session = Depends(get_db)
):
    """创建存储策略"""
    db_obj = await storage_policy.get_by_name(db, name=policy_in.name)
    if db_obj:
        raise HTTPException(
            status_code=400,
            detail="Storage policy with this name already exists"
        )
    return await storage_policy.create(db, obj_in=policy_in)

@router.get("/storage-policies", response_model=List[StoragePolicyInDB])
async def list_storage_policies(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """获取存储策略列表"""
    return await storage_policy.get_multi(db, skip=skip, limit=limit)

@router.get("/storage-policies/{policy_id}", response_model=StoragePolicyInDB)
async def get_storage_policy(
    policy_id: int,
    db: Session = Depends(get_db)
):
    """获取存储策略详情"""
    db_obj = await storage_policy.get(db, id=policy_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Storage policy not found")
    return db_obj

@router.put("/storage-policies/{policy_id}", response_model=StoragePolicyInDB)
async def update_storage_policy(
    policy_id: int,
    policy_in: StoragePolicyUpdate,
    db: Session = Depends(get_db)
):
    """更新存储策略"""
    db_obj = await storage_policy.get(db, id=policy_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Storage policy not found")
    return await storage_policy.update(db, db_obj=db_obj, obj_in=policy_in)

@router.get("/storage-policies/{policy_id}/executions", response_model=List[StoragePolicyExecution])
async def list_policy_executions(
    policy_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """获取策略执行历史"""
    db_obj = await storage_policy.get(db, id=policy_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Storage policy not found")
    return db_obj.executions[skip:skip + limit] 