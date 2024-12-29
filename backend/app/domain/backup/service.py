from datetime import datetime, timedelta
from typing import List, Optional
from uuid import uuid4
from .repository import BackupConfigRepository, BackupJobRepository
from .aggregate import BackupConfig, BackupJob, BackupType, BackupStatus
from ...interface.ws.messages import broadcast_backup_status

class BackupService:
    def __init__(
        self,
        config_repo: BackupConfigRepository,
        job_repo: BackupJobRepository
    ):
        self.config_repo = config_repo
        self.job_repo = job_repo
    
    async def create_config(
        self,
        server_id: str,
        name: str,
        type: str,
        schedule: str,
        retention_days: int,
        target_dir: str
    ) -> BackupConfig:
        """创建备份配置"""
        now = datetime.now()
        config = BackupConfig(
            id=str(uuid4()),
            server_id=server_id,
            name=name,
            type=BackupType(type),
            schedule=schedule,
            retention_days=retention_days,
            target_dir=target_dir,
            enabled=True,
            created_at=now,
            updated_at=now
        )
        await self.config_repo.save(config)
        return config
    
    async def create_job(
        self,
        config_id: str
    ) -> BackupJob:
        """创建备份任务"""
        config = await self.config_repo.get_by_id(config_id)
        if not config:
            raise ValueError("Backup config not found")
        
        now = datetime.now()
        job = BackupJob(
            id=str(uuid4()),
            config_id=config_id,
            server_id=config.server_id,
            type=config.type,
            status=BackupStatus.PENDING,
            start_time=now,
            end_time=None,
            size=None,
            file_path=None,
            error=None,
            created_at=now
        )
        await self.job_repo.save(job)
        
        # 广播任务状态
        await broadcast_backup_status(job.server_id, job.to_dict())
        return job
    
    async def update_job_status(
        self,
        job_id: str,
        status: str,
        **kwargs
    ) -> BackupJob:
        """更新任务状态"""
        job = await self.job_repo.get_by_id(job_id)
        if not job:
            raise ValueError("Backup job not found")
        
        # 更新状态
        job.status = BackupStatus(status)
        job.end_time = kwargs.get("end_time", job.end_time)
        job.size = kwargs.get("size", job.size)
        job.file_path = kwargs.get("file_path", job.file_path)
        job.error = kwargs.get("error", job.error)
        
        await self.job_repo.save(job)
        
        # 广播状态更新
        await broadcast_backup_status(job.server_id, job.to_dict())
        return job
    
    async def cleanup_old_backups(self) -> None:
        """清理过期备份"""
        configs = await self.config_repo.list_all()
        for config in configs:
            if not config.enabled:
                continue
            
            expire_time = datetime.now() - timedelta(days=config.retention_days)
            await self.job_repo.delete_before(
                config.id,
                expire_time
            ) 