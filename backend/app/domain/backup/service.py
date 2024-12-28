from datetime import datetime
from typing import List, Optional
from uuid import uuid4
from .repository import BackupRepository
from .aggregate import Backup, BackupRestore, BackupStatus, BackupType
from app.infrastructure.backup.service import BackupService as BackupInfraService

class BackupService:
    """备份领域服务"""
    
    def __init__(
        self,
        backup_repo: BackupRepository,
        backup_infra: BackupInfraService
    ):
        self.backup_repo = backup_repo
        self.backup_infra = backup_infra
    
    async def create_backup(
        self,
        user_id: str,
        backup_type: BackupType = BackupType.FULL
    ) -> Backup:
        """创建备份"""
        # 创建备份记录
        backup = Backup(
            id=str(uuid4()),
            filename="",  # 临时文件名
            size=0,  # 临时大小
            created_at=datetime.now(),
            created_by=user_id,
            status=BackupStatus.PENDING,
            error_message=None,
            backup_type=backup_type,
            metadata={}
        )
        await self.backup_repo.save(backup)
        
        try:
            # 执行备份
            filename = await self.backup_infra.create_backup()
            
            # 更新备份记录
            backup.filename = filename
            backup.size = self._get_file_size(filename)
            backup.status = BackupStatus.SUCCESS
            await self.backup_repo.save(backup)
            
            return backup
            
        except Exception as e:
            # 更新失败状态
            backup.status = BackupStatus.FAILED
            backup.error_message = str(e)
            await self.backup_repo.save(backup)
            raise
    
    async def restore_backup(
        self,
        backup_id: str,
        user_id: str
    ) -> BackupRestore:
        """恢复备份"""
        backup = await self.backup_repo.get_by_id(backup_id)
        if not backup:
            raise ValueError("Backup not found")
            
        # 创建恢复记录
        restore = BackupRestore(
            id=str(uuid4()),
            backup_id=backup_id,
            restored_at=datetime.now(),
            restored_by=user_id,
            status=BackupStatus.PENDING,
            error_message=None
        )
        await self.backup_repo.save_restore(restore)
        
        try:
            # 执行恢复
            await self.backup_infra.restore_backup(backup.filename)
            
            # 更新恢复记录
            restore.status = BackupStatus.SUCCESS
            await self.backup_repo.save_restore(restore)
            
            return restore
            
        except Exception as e:
            # 更新失败状态
            restore.status = BackupStatus.FAILED
            restore.error_message = str(e)
            await self.backup_repo.save_restore(restore)
            raise
    
    async def list_backups(
        self,
        limit: int = 100,
        offset: int = 0
    ) -> List[Backup]:
        """获取备份列表"""
        return await self.backup_repo.list_backups(limit, offset)
    
    async def get_backup(self, backup_id: str) -> Optional[Backup]:
        """获取备份详情"""
        return await self.backup_repo.get_by_id(backup_id)
    
    async def list_restores(self, backup_id: str) -> List[BackupRestore]:
        """获取恢复记录列表"""
        return await self.backup_repo.list_restores(backup_id)
    
    def _get_file_size(self, filename: str) -> int:
        """获取文件大小"""
        import os
        return os.path.getsize(os.path.join(self.backup_infra.backup_dir, filename)) 