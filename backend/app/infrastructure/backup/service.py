from datetime import datetime, timedelta
import os
import tarfile
from typing import List
from .database import DatabaseBackup
from .config import ConfigBackup
from app.infrastructure.config import settings

class BackupService:
    """数据备份服务"""
    
    def __init__(self):
        self.backup_dir = settings.BACKUP_DIR
        self.db_backup = DatabaseBackup()
        self.config_backup = ConfigBackup()
        os.makedirs(self.backup_dir, exist_ok=True)
        
    async def create_backup(self) -> str:
        """创建备份"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = f"backup_{timestamp}.tar.gz"
        backup_path = os.path.join(self.backup_dir, backup_file)
        
        try:
            # 备份数据库
            db_file = f"{backup_path}.db"
            await self.db_backup.backup(db_file)
            
            # 备份配置
            config_file = f"{backup_path}.config"
            self.config_backup.backup(config_file)
            
            # 打包所有备份文件
            with tarfile.open(backup_path, "w:gz") as tar:
                tar.add(db_file)
                tar.add(config_file)
                
            # 清理临时文件
            os.unlink(db_file)
            os.unlink(config_file)
            
            # 清理过期备份
            await self._cleanup_old_backups()
            
            return backup_file
            
        except Exception as e:
            # 清理失败的备份文件
            if os.path.exists(backup_path):
                os.unlink(backup_path)
            raise RuntimeError(f"Backup failed: {str(e)}")
            
    async def restore_backup(self, backup_file: str) -> None:
        """恢复备份"""
        backup_path = os.path.join(self.backup_dir, backup_file)
        if not os.path.exists(backup_path):
            raise ValueError("Backup file not found")
            
        # 解压备份文件
        with tarfile.open(backup_path, "r:gz") as tar:
            tar.extractall(self.backup_dir)
            
        try:
            # 恢复数据库
            db_file = f"{backup_path}.db"
            await self.db_backup.restore(db_file)
            
            # 恢复配置
            config_file = f"{backup_path}.config"
            self.config_backup.restore(config_file)
            
        finally:
            # 清理临时文件
            if os.path.exists(db_file):
                os.unlink(db_file)
            if os.path.exists(config_file):
                os.unlink(config_file)
                
    async def _cleanup_old_backups(self):
        """清理过期备份"""
        retention_days = settings.BACKUP_KEEP_DAYS
        threshold = datetime.now() - timedelta(days=retention_days)
        
        for backup in self.list_backups():
            try:
                # 从文件名解析备份时间
                timestamp = backup.split("_")[1].split(".")[0]
                backup_time = datetime.strptime(timestamp, "%Y%m%d_%H%M%S")
                
                if backup_time < threshold:
                    backup_path = os.path.join(self.backup_dir, backup)
                    os.unlink(backup_path)
            except:
                continue
    
    def list_backups(self) -> List[str]:
        """获取备份列表"""
        backups = []
        for file in os.listdir(self.backup_dir):
            if file.startswith("backup_") and file.endswith(".tar.gz"):
                backups.append(file)
        return sorted(backups, reverse=True) 