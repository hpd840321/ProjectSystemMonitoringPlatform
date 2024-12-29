from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import datetime
from .aggregate import BackupConfig, BackupJob

class BackupConfigRepository(ABC):
    """备份配置仓储接口"""
    
    @abstractmethod
    async def save(self, config: BackupConfig) -> None:
        """保存备份配置"""
        pass
    
    @abstractmethod
    async def get_by_id(self, config_id: str) -> Optional[BackupConfig]:
        """获取备份配置"""
        pass
    
    @abstractmethod
    async def list_by_server(self, server_id: str) -> List[BackupConfig]:
        """获取服务器的备份配置列表"""
        pass
    
    @abstractmethod
    async def list_all(self) -> List[BackupConfig]:
        """获取所有备份配置"""
        pass
    
    @abstractmethod
    async def delete(self, config_id: str) -> None:
        """删除备份配置"""
        pass

class BackupJobRepository(ABC):
    """备份任务仓储接口"""
    
    @abstractmethod
    async def save(self, job: BackupJob) -> None:
        """保存备份任务"""
        pass
    
    @abstractmethod
    async def get_by_id(self, job_id: str) -> Optional[BackupJob]:
        """获取备份任务"""
        pass
    
    @abstractmethod
    async def list_by_config(
        self,
        config_id: str,
        limit: int = 100,
        offset: int = 0
    ) -> List[BackupJob]:
        """获取备份配置的任务列表"""
        pass
    
    @abstractmethod
    async def list_by_server(
        self,
        server_id: str,
        limit: int = 100,
        offset: int = 0
    ) -> List[BackupJob]:
        """获取服务器的任务列表"""
        pass
    
    @abstractmethod
    async def delete_before(self, config_id: str, timestamp: datetime) -> None:
        """删除指定时间之前的任务"""
        pass 