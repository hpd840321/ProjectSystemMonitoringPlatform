import os
import shutil
import tarfile
from typing import List
from app.infrastructure.config import settings

class ConfigBackup:
    """配置文件备份工具"""
    
    def __init__(self):
        self.config_paths = [
            ".env",
            "config/",
            "certs/"
        ]
        
    def backup(self, backup_file: str) -> None:
        """备份配置文件"""
        with tarfile.open(backup_file, "w:gz") as tar:
            for path in self.config_paths:
                if os.path.exists(path):
                    tar.add(path)
                    
    def restore(self, backup_file: str) -> None:
        """恢复配置文件"""
        with tarfile.open(backup_file, "r:gz") as tar:
            tar.extractall("./") 