from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional

class BackupType(str, Enum):
    FULL = "full"      # 全量备份
    INCREMENTAL = "incremental"  # 增量备份

class BackupStatus(str, Enum):
    PENDING = "pending"    # 等待执行
    RUNNING = "running"    # 执行中
    COMPLETED = "completed"  # 完成
    FAILED = "failed"     # 失败

@dataclass
class BackupConfig:
    """备份配置"""
    id: str
    server_id: str
    name: str
    type: BackupType
    schedule: str  # cron表达式
    retention_days: int  # 保留天数
    target_dir: str  # 备份目标目录
    enabled: bool
    created_at: datetime
    updated_at: datetime

@dataclass
class BackupJob:
    """备份任务"""
    id: str
    config_id: str
    server_id: str
    type: BackupType
    status: BackupStatus
    start_time: datetime
    end_time: Optional[datetime]
    size: Optional[int]  # 备份大小(字节)
    file_path: Optional[str]  # 备份文件路径
    error: Optional[str]  # 错误信息
    created_at: datetime 