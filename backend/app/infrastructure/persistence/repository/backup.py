from datetime import datetime
from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.backup.repository import BackupRepository
from app.domain.backup.aggregate import Backup, BackupRestore, BackupStatus
from ..models.backup import BackupModel, BackupRestoreModel

class SQLAlchemyBackupRepository(BackupRepository):
    """备份SQLAlchemy仓储实现"""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def save(self, backup: Backup) -> None:
        """保存备份记录"""
        model = BackupModel(
            id=backup.id,
            filename=backup.filename,
            size=backup.size,
            created_at=backup.created_at,
            created_by=backup.created_by,
            status=backup.status.value,
            error_message=backup.error_message,
            backup_type=backup.backup_type.value,
            metadata=backup.metadata
        )
        self.session.add(model)
        await self.session.commit()
    
    async def get_by_id(self, backup_id: str) -> Optional[Backup]:
        """获取备份记录"""
        result = await self.session.execute(
            select(BackupModel).where(BackupModel.id == backup_id)
        )
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None
    
    async def list_backups(
        self,
        limit: int = 100,
        offset: int = 0
    ) -> List[Backup]:
        """获取备份列表"""
        result = await self.session.execute(
            select(BackupModel)
            .order_by(BackupModel.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        return [self._to_entity(model) for model in result.scalars()]
    
    async def save_restore(self, restore: BackupRestore) -> None:
        """保存恢复记录"""
        model = BackupRestoreModel(
            id=restore.id,
            backup_id=restore.backup_id,
            restored_at=restore.restored_at,
            restored_by=restore.restored_by,
            status=restore.status.value,
            error_message=restore.error_message
        )
        self.session.add(model)
        await self.session.commit()
    
    async def list_restores(
        self,
        backup_id: str
    ) -> List[BackupRestore]:
        """获取恢复记录列表"""
        result = await self.session.execute(
            select(BackupRestoreModel)
            .where(BackupRestoreModel.backup_id == backup_id)
            .order_by(BackupRestoreModel.restored_at.desc())
        )
        return [self._to_restore_entity(model) for model in result.scalars()] 