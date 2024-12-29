from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.interface.api.v1.dependencies import get_db
from app.interface.api.v1.schemas.backup import (
    BackupConfigCreate,
    BackupConfigUpdate,
    BackupConfigInDB,
    BackupRecordInDB
)
from app.crud import backup_config

router = APIRouter()

@router.post("/backup-configs", response_model=BackupConfigInDB)
async def create_backup_config(
    config_in: BackupConfigCreate,
    db: Session = Depends(get_db)
):
    """创建备份配置"""
    db_obj = await backup_config.get_by_name(db, name=config_in.name)
    if db_obj:
        raise HTTPException(
            status_code=400,
            detail="Backup config with this name already exists"
        )
    return await backup_config.create(db, obj_in=config_in)

@router.get("/backup-configs", response_model=List[BackupConfigInDB])
async def list_backup_configs(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """获取备份配置列表"""
    return await backup_config.get_multi(db, skip=skip, limit=limit)

@router.get("/backup-configs/{config_id}", response_model=BackupConfigInDB)
async def get_backup_config(
    config_id: int,
    db: Session = Depends(get_db)
):
    """获取备份配置详情"""
    db_obj = await backup_config.get(db, id=config_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Backup config not found")
    return db_obj

@router.put("/backup-configs/{config_id}", response_model=BackupConfigInDB)
async def update_backup_config(
    config_id: int,
    config_in: BackupConfigUpdate,
    db: Session = Depends(get_db)
):
    """更新备份配置"""
    db_obj = await backup_config.get(db, id=config_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Backup config not found")
    return await backup_config.update(db, db_obj=db_obj, obj_in=config_in)

@router.delete("/backup-configs/{config_id}")
async def delete_backup_config(
    config_id: int,
    db: Session = Depends(get_db)
):
    """删除备份配置"""
    db_obj = await backup_config.get(db, id=config_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Backup config not found")
    await backup_config.delete(db, id=config_id)
    return {"msg": "Backup config deleted successfully"}

@router.get("/backup-configs/{config_id}/records", response_model=List[BackupRecordInDB])
async def list_backup_records(
    config_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """获取备份记录列表"""
    db_obj = await backup_config.get(db, id=config_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Backup config not found")
    return await backup_config.get_records(db, config_id=config_id, skip=skip, limit=limit) 