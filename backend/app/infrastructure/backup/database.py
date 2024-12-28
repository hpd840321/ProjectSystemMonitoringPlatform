import asyncio
import os
import subprocess
from datetime import datetime
from app.infrastructure.config import settings

class DatabaseBackup:
    """数据库备份工具"""
    
    def __init__(self):
        self.db_url = settings.BACKUP_DATABASE_URL
        self.db_name = self.db_url.split("/")[-1]
        
    async def backup(self, backup_file: str) -> None:
        """备份数据库"""
        # 使用pg_dump备份
        cmd = [
            "pg_dump",
            "-h", self.db_url.split("@")[1].split("/")[0],
            "-U", self.db_url.split("://")[1].split(":")[0],
            "-d", self.db_name,
            "-F", "c",  # 自定义格式
            "-f", backup_file
        ]
        
        process = await asyncio.create_subprocess_exec(
            *cmd,
            env={"PGPASSWORD": self.db_url.split(":")[2].split("@")[0]}
        )
        await process.wait()
        
        if process.returncode != 0:
            raise RuntimeError("Database backup failed")
            
    async def restore(self, backup_file: str) -> None:
        """恢复数据库"""
        # 使用pg_restore恢复
        cmd = [
            "pg_restore",
            "-h", self.db_url.split("@")[1].split("/")[0],
            "-U", self.db_url.split("://")[1].split(":")[0],
            "-d", self.db_name,
            "-c",  # 清理现有数据
            backup_file
        ]
        
        process = await asyncio.create_subprocess_exec(
            *cmd,
            env={"PGPASSWORD": self.db_url.split(":")[2].split("@")[0]}
        )
        await process.wait()
        
        if process.returncode != 0:
            raise RuntimeError("Database restore failed") 