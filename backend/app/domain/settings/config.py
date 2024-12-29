from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Dict, Optional

class NotificationType(str, Enum):
    EMAIL = "email"
    WEBHOOK = "webhook"
    SMS = "sms"

class StorageType(str, Enum):
    LOCAL = "local"
    S3 = "s3"
    OSS = "oss"

class DataType(str, Enum):
    METRICS = "metrics"
    LOGS = "logs"
    BACKUPS = "backups"

@dataclass
class NotificationSettings:
    id: str
    type: NotificationType
    name: str
    config: Dict
    enabled: bool
    created_at: datetime
    updated_at: datetime

@dataclass
class StorageSettings:
    id: str
    type: StorageType
    name: str
    config: Dict
    is_default: bool
    created_at: datetime
    updated_at: datetime

@dataclass
class RetentionSettings:
    id: str
    data_type: DataType
    retention_days: int
    compression_enabled: bool
    compression_days: Optional[int]
    created_at: datetime
    updated_at: datetime 