from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.interface.api.v1.dependencies import get_db
from app.interface.api.v1.schemas.alert_level import (
    AlertLevelCreate, AlertLevelUpdate, AlertLevelInDB
)
from app.crud import alert_level

router = APIRouter()

@router.post("/alert-levels", response_model=AlertLevelInDB)
async def create_alert_level(
    level_in: AlertLevelCreate,
    db: Session = Depends(get_db)
):
    """创建告警级别"""
    # 检查名称是否已存在
    db_obj = await alert_level.get_by_name(db, name=level_in.name)
    if db_obj:
        raise HTTPException(
            status_code=400,
            detail="Alert level with this name already exists"
        )
    return await alert_level.create(db, obj_in=level_in)

@router.get("/alert-levels", response_model=List[AlertLevelInDB])
async def list_alert_levels(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """获取告警级别列表"""
    return await alert_level.get_multi(db, skip=skip, limit=limit)

@router.get("/alert-levels/{level_id}", response_model=AlertLevelInDB)
async def get_alert_level(
    level_id: int,
    db: Session = Depends(get_db)
):
    """获取告警级别详情"""
    db_obj = await alert_level.get(db, id=level_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Alert level not found")
    return db_obj

@router.put("/alert-levels/{level_id}", response_model=AlertLevelInDB)
async def update_alert_level(
    level_id: int,
    level_in: AlertLevelUpdate,
    db: Session = Depends(get_db)
):
    """更新告警级别"""
    db_obj = await alert_level.get(db, id=level_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Alert level not found")
    
    # 检查新名称是否与其他级别冲突
    if level_in.name != db_obj.name:
        existing = await alert_level.get_by_name(db, name=level_in.name)
        if existing:
            raise HTTPException(
                status_code=400,
                detail="Alert level with this name already exists"
            )
    
    return await alert_level.update(db, db_obj=db_obj, obj_in=level_in)

@router.delete("/alert-levels/{level_id}")
async def delete_alert_level(
    level_id: int,
    db: Session = Depends(get_db)
):
    """删除告警级别"""
    db_obj = await alert_level.get(db, id=level_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Alert level not found")
    
    # 检查是否有告警使用此级别
    if db_obj.alerts:
        raise HTTPException(
            status_code=400,
            detail="Cannot delete alert level that is in use"
        )
    
    await alert_level.delete(db, id=level_id)
    return {"msg": "Alert level deleted successfully"} 