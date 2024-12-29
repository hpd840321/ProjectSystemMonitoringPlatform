from datetime import datetime
from typing import List, Optional
from sqlalchemy import select, and_, desc
from .database import Database
from ...domain.backup.repository import BackupConfigRepository, BackupJobRepository
from ...domain.backup.aggregate import BackupConfig, BackupJob, BackupType, BackupStatus

class BackupConfigRepositoryImpl(BackupConfigRepository):
    def __init__(self, db: Database):
        self.db = db
    
    async def save(self, config: BackupConfig) -> None:
        query = """
            INSERT INTO backup_configs (
                id, server_id, name, type, schedule,
                retention_days, target_dir, enabled,
                created_at, updated_at
            ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
            ON CONFLICT (id) DO UPDATE SET
                name = $3,
                type = $4,
                schedule = $5,
                retention_days = $6,
                target_dir = $7,
                enabled = $8,
                updated_at = $10
        """
        await self.db.execute(
            query,
            config.id,
            config.server_id,
            config.name,
            config.type.value,
            config.schedule,
            config.retention_days,
            config.target_dir,
            config.enabled,
            config.created_at,
            config.updated_at
        )
    
    async def get_by_id(self, config_id: str) -> Optional[BackupConfig]:
        query = "SELECT * FROM backup_configs WHERE id = $1"
        row = await self.db.fetch_one(query, config_id)
        if not row:
            return None
        return BackupConfig(
            **{
                **row,
                "type": BackupType(row["type"])
            }
        )
    
    async def list_by_server(self, server_id: str) -> List[BackupConfig]:
        query = "SELECT * FROM backup_configs WHERE server_id = $1"
        rows = await self.db.fetch_all(query, server_id)
        return [
            BackupConfig(
                **{
                    **row,
                    "type": BackupType(row["type"])
                }
            )
            for row in rows
        ]
    
    async def list_all(self) -> List[BackupConfig]:
        query = "SELECT * FROM backup_configs"
        rows = await self.db.fetch_all(query)
        return [
            BackupConfig(
                **{
                    **row,
                    "type": BackupType(row["type"])
                }
            )
            for row in rows
        ]
    
    async def delete(self, config_id: str) -> None:
        query = "DELETE FROM backup_configs WHERE id = $1"
        await self.db.execute(query, config_id)

class BackupJobRepositoryImpl(BackupJobRepository):
    def __init__(self, db: Database):
        self.db = db
    
    async def save(self, job: BackupJob) -> None:
        query = """
            INSERT INTO backup_jobs (
                id, config_id, server_id, type, status,
                start_time, end_time, size, file_path,
                error, created_at
            ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
            ON CONFLICT (id) DO UPDATE SET
                status = $5,
                end_time = $7,
                size = $8,
                file_path = $9,
                error = $10
        """
        await self.db.execute(
            query,
            job.id,
            job.config_id,
            job.server_id,
            job.type.value,
            job.status.value,
            job.start_time,
            job.end_time,
            job.size,
            job.file_path,
            job.error,
            job.created_at
        )
    
    async def get_by_id(self, job_id: str) -> Optional[BackupJob]:
        query = "SELECT * FROM backup_jobs WHERE id = $1"
        row = await self.db.fetch_one(query, job_id)
        if not row:
            return None
        return BackupJob(
            **{
                **row,
                "type": BackupType(row["type"]),
                "status": BackupStatus(row["status"])
            }
        )
    
    async def list_by_config(
        self,
        config_id: str,
        limit: int = 100,
        offset: int = 0
    ) -> List[BackupJob]:
        query = """
            SELECT * FROM backup_jobs
            WHERE config_id = $1
            ORDER BY start_time DESC
            LIMIT $2 OFFSET $3
        """
        rows = await self.db.fetch_all(query, config_id, limit, offset)
        return [
            BackupJob(
                **{
                    **row,
                    "type": BackupType(row["type"]),
                    "status": BackupStatus(row["status"])
                }
            )
            for row in rows
        ]
    
    async def list_by_server(
        self,
        server_id: str,
        limit: int = 100,
        offset: int = 0
    ) -> List[BackupJob]:
        query = """
            SELECT * FROM backup_jobs
            WHERE server_id = $1
            ORDER BY start_time DESC
            LIMIT $2 OFFSET $3
        """
        rows = await self.db.fetch_all(query, server_id, limit, offset)
        return [
            BackupJob(
                **{
                    **row,
                    "type": BackupType(row["type"]),
                    "status": BackupStatus(row["status"])
                }
            )
            for row in rows
        ]
    
    async def delete_before(self, config_id: str, timestamp: datetime) -> None:
        query = """
            DELETE FROM backup_jobs
            WHERE config_id = $1 AND start_time < $2
        """
        await self.db.execute(query, config_id, timestamp) 