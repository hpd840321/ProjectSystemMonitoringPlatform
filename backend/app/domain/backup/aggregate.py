from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional, Dict

class BackupStatus(str, Enum):
    PENDING = "pending"
    SUCCESS = "success"
    FAILED = "failed"

class BackupType(str, Enum):
    FULL = "full"
    CONFIG = "config"
    DATABASE = "database"

@dataclass
class Backup:
    """备份聚合根"""
    id: str
    filename: str
    size: int
    created_at: datetime
    created_by: str
    status: BackupStatus
    error_message: Optional[str]
    backup_type: BackupType
    metadata: Dict

@dataclass
class BackupRestore:
    """备份恢复记录"""
    id: str
    backup_id: str
    restored_at: datetime
    restored_by: str
    status: BackupStatus
    error_message: Optional[str] 