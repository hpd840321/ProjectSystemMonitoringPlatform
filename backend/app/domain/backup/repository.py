from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import datetime
from .aggregate import Backup, BackupRestore

class BackupRepository(ABC):
    """备份仓储接口"""
    
    @abstractmethod
    async def save(self, backup: Backup) -> None:
        """保存备份记录"""
        pass
    
    @abstractmethod
    async def get_by_id(self, backup_id: str) -> Optional[Backup]:
        """获取备份记录"""
        pass
    
    @abstractmethod
    async def list_backups(
        self,
        limit: int = 100,
        offset: int = 0
    ) -> List[Backup]:
        """获取备份列表"""
        pass
    
    @abstractmethod
    async def save_restore(self, restore: BackupRestore) -> None:
        """保存恢复记录"""
        pass
    
    @abstractmethod
    async def list_restores(
        self,
        backup_id: str
    ) -> List[BackupRestore]:
        """获取恢复记录列表"""
        pass 