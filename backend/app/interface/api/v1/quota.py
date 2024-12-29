from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.interface.api.v1.dependencies import get_db
from app.interface.api.v1.schemas.quota import (
    QuotaCreate, QuotaUpdate, QuotaInDB, ResourceUsageCreate
)
from app.crud import quota

router = APIRouter()

@router.post("/projects/{project_id}/quotas", response_model=QuotaInDB)
async def create_quota(
    project_id: int,
    quota_in: QuotaCreate,
    db: Session = Depends(get_db)
):
    """创建项目资源配额"""
    quota_in.project_id = project_id
    return await quota.create(db, obj_in=quota_in)

@router.get("/projects/{project_id}/quotas", response_model=List[QuotaInDB])
async def list_quotas(
    project_id: int,
    db: Session = Depends(get_db)
):
    """获取项目的所有资源配额"""
    return await quota.get_multi_by_project(db, project_id=project_id)

@router.put("/quotas/{quota_id}", response_model=QuotaInDB)
async def update_quota(
    quota_id: int,
    quota_in: QuotaUpdate,
    db: Session = Depends(get_db)
):
    """更新资源配额"""
    db_obj = await quota.get(db, id=quota_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Quota not found")
    return await quota.update(db, db_obj=db_obj, obj_in=quota_in)

@router.post("/projects/{project_id}/resource-usage")
async def record_resource_usage(
    project_id: int,
    usage: ResourceUsageCreate,
    db: Session = Depends(get_db)
):
    """记录资源使用情况"""
    if usage.operation == "increase":
        # 检查是否超出配额
        if not await quota.check_quota(
            db,
            project_id=project_id,
            resource_type=usage.resource_type,
            amount=usage.amount
        ):
            raise HTTPException(
                status_code=400,
                detail="Resource quota exceeded"
            )
    
    await quota.record_usage(
        db,
        project_id=project_id,
        resource_type=usage.resource_type,
        amount=usage.amount,
        operation=usage.operation
    )
    return {"msg": "Resource usage recorded successfully"} 