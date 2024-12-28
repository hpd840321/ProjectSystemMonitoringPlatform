from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Dict, Optional

class LogLevel(str, Enum):
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

@dataclass
class LogConfig:
    """日志配置"""
    path: str
    pattern: str  # 日志解析正则
    level: LogLevel
    enabled: bool = True

@dataclass
class LogEntry:
    """日志条目"""
    id: str
    server_id: str
    timestamp: datetime
    level: LogLevel
    message: str
    source: str  # 日志来源
    metadata: Dict  # 解析后的结构化数据
    raw: str  # 原始日志

@dataclass
class LogFilter:
    """日志过滤器"""
    server_id: Optional[str] = None
    level: Optional[LogLevel] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    keyword: Optional[str] = None
    source: Optional[str] = None 