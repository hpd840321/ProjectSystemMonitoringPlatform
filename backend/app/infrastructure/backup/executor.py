import os
import shutil
import asyncio
import logging
from datetime import datetime
from typing import Optional
from croniter import croniter
import tarfile
import subprocess

from sqlalchemy.orm import Session
from app.crud import backup_config
from app.models.backup import BackupConfig
from app.interface.api.v1.schemas.backup import BackupRecordCreate
from app.infrastructure.persistence.database import SessionLocal

logger = logging.getLogger(__name__)

class BackupExecutor:
    """备份执行器"""
    
    def __init__(self):
        self.running = False
        self.tasks = {}
    
    async def start(self):
        """启动执行器"""
        self.running = True
        db = SessionLocal()
        try:
            # 加载所有启用的备份配置
            configs = backup_config.get_multi(db)
            enabled_configs = [c for c in configs if c.enabled]
            
            # 为每个配置创建调度任务
            for config in enabled_configs:
                self._schedule_backup(config)
        finally:
            db.close()
            
        # 启动调度循环
        while self.running:
            await asyncio.sleep(60)  # 每分钟检查一次
            await self._check_schedules()
    
    def stop(self):
        """停止执行器"""
        self.running = False
        for task in self.tasks.values():
            task.cancel()
    
    def _schedule_backup(self, config: BackupConfig):
        """调度备份任务"""
        self.tasks[config.id] = {
            "config": config,
            "next_run": self._get_next_run(config.schedule)
        }
    
    async def _check_schedules(self):
        """检查调度"""
        now = datetime.now()
        for config_id, task in list(self.tasks.items()):
            if now >= task["next_run"]:
                config = task["config"]
                # 更新下次执行时间
                self.tasks[config_id]["next_run"] = self._get_next_run(config.schedule)
                # 执行备份
                asyncio.create_task(self._execute_backup(config))
    
    async def _execute_backup(self, config: BackupConfig):
        """执行备份"""
        db = SessionLocal()
        try:
            # 创建备份记录
            record = await backup_config.create_record(
                db,
                obj_in=BackupRecordCreate(
                    config_id=config.id,
                    file_path="",  # 临时路径
                    file_size=0,
                    status="running",
                    started_at=datetime.now()
                )
            )
            
            try:
                # 执行具体的备份操作
                backup_path = await self._perform_backup(config)
                file_size = os.path.getsize(backup_path)
                
                # 更新记录
                record.file_path = backup_path
                record.file_size = file_size
                record.status = "success"
                record.completed_at = datetime.now()
                
                # 清理旧备份
                await self._cleanup_old_backups(config)
                
            except Exception as e:
                logger.exception(f"Failed to execute backup {config.id}")
                record.status = "failed"
                record.error_message = str(e)
                record.completed_at = datetime.now()
            
            db.add(record)
            db.commit()
            
        finally:
            db.close()
    
    async def _perform_backup(self, config: BackupConfig) -> str:
        """执行具体的备份操作"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{config.name}_{timestamp}.tar.gz"
        backup_path = os.path.join(config.target_path, backup_name)
        
        # 确保目标目录存在
        os.makedirs(config.target_path, exist_ok=True)
        
        if config.type == "system":
            # 系统备份
            await self._backup_system(backup_path)
        elif config.type == "database":
            # 数据库备份
            await self._backup_database(backup_path)
        elif config.type == "files":
            # 文件备份
            await self._backup_files(backup_path)
        
        return backup_path
    
    async def _backup_system(self, backup_path: str):
        """系统备份"""
        # 使用tar打包系统关键目录
        cmd = [
            "tar", "czf", backup_path,
            "/etc",
            "/var/log",
            "--exclude=/var/log/journal"
        ]
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        await process.communicate()
        if process.returncode != 0:
            raise Exception("System backup failed")
    
    async def _backup_database(self, backup_path: str):
        """数据库备份"""
        # 使用pg_dump备份PostgreSQL数据库
        dump_file = backup_path.replace(".tar.gz", ".sql")
        cmd = [
            "pg_dump",
            "-h", "localhost",
            "-U", "postgres",
            "-f", dump_file,
            "monitor"
        ]
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        await process.communicate()
        if process.returncode != 0:
            raise Exception("Database backup failed")
        
        # 压缩dump文件
        with tarfile.open(backup_path, "w:gz") as tar:
            tar.add(dump_file, arcname=os.path.basename(dump_file))
        os.remove(dump_file)
    
    async def _backup_files(self, backup_path: str):
        """文件备份"""
        # 这里需要根据实际需求指定要备份的文件路径
        paths_to_backup = [
            "/data/uploads",
            "/data/configs"
        ]
        
        with tarfile.open(backup_path, "w:gz") as tar:
            for path in paths_to_backup:
                if os.path.exists(path):
                    tar.add(path, arcname=os.path.basename(path))
    
    async def _cleanup_old_backups(self, config: BackupConfig):
        """清理旧备份"""
        backup_dir = config.target_path
        if not os.path.exists(backup_dir):
            return
            
        # 获取所有备份文件并按时间排序
        backups = []
        for f in os.listdir(backup_dir):
            if f.startswith(f"{config.name}_") and f.endswith(".tar.gz"):
                path = os.path.join(backup_dir, f)
                backups.append((path, os.path.getctime(path)))
        
        backups.sort(key=lambda x: x[1], reverse=True)
        
        # 删除超出保留数量的旧备份
        for path, _ in backups[config.retention_count:]:
            try:
                os.remove(path)
            except Exception as e:
                logger.error(f"Failed to remove old backup {path}: {e}")
    
    def _get_next_run(self, schedule: str) -> datetime:
        """获取下次执行时间"""
        cron = croniter(schedule, datetime.now())
        return cron.get_next(datetime) 