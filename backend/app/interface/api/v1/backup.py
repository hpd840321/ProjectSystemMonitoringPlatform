from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.domain.backup.service import BackupService
from app.domain.backup.aggregate import Backup, BackupRestore, BackupType
from app.interface.api.dependencies import get_current_admin_user
from app.interface.api.schemas.backup import (
    BackupResponse,
    BackupRestoreResponse,
    CreateBackupRequest
)

router = APIRouter()

@router.post("/backups", response_model=BackupResponse)
async def create_backup(
    request: CreateBackupRequest,
    backup_service: BackupService = Depends(),
    current_user = Depends(get_current_admin_user)
) -> BackupResponse:
    """创建备份"""
    try:
        backup = await backup_service.create_backup(
            current_user.id,
            request.backup_type
        )
        return BackupResponse.from_entity(backup)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/backups/{backup_id}/restore", response_model=BackupRestoreResponse)
async def restore_backup(
    backup_id: str,
    backup_service: BackupService = Depends(),
    current_user = Depends(get_current_admin_user)
) -> BackupRestoreResponse:
    """恢复备份"""
    try:
        restore = await backup_service.restore_backup(
            backup_id,
            current_user.id
        )
        return BackupRestoreResponse.from_entity(restore)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/backups", response_model=List[BackupResponse])
async def list_backups(
    limit: int = 100,
    offset: int = 0,
    backup_service: BackupService = Depends(),
    _=Depends(get_current_admin_user)
) -> List[BackupResponse]:
    """获取备份列表"""
    backups = await backup_service.list_backups(limit, offset)
    return [BackupResponse.from_entity(b) for b in backups] 