from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Dict, Optional, List

class LogLevel(str, Enum):
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

class LogFormat(str, Enum):
    SYSLOG = "syslog"
    JSON = "json"
    NGINX = "nginx"
    APACHE = "apache"
    CUSTOM = "custom"

@dataclass
class LogConfig:
    """日志采集配置"""
    id: str
    server_id: str
    name: str
    description: Optional[str]
    file_path: str
    format: LogFormat
    pattern: Optional[str]  # 自定义格式的正则表达式
    fields: Dict[str, str]  # 字段映射
    enabled: bool
    created_at: datetime
    updated_at: datetime

@dataclass
class LogEntry:
    """日志条目"""
    id: str
    config_id: str
    server_id: str
    level: LogLevel
    message: str
    timestamp: datetime
    fields: Dict[str, str]  # 解析后的字段
    raw: str  # 原始日志行
    created_at: datetime

@dataclass
class LogFilter:
    """日志过滤器"""
    server_id: Optional[str] = None
    level: Optional[LogLevel] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    keyword: Optional[str] = None
    source: Optional[str] = None 

@dataclass
class LogParseRule:
    """日志解析规则"""
    id: str
    name: str
    pattern: str
    fields: Dict[str, str]  # 字段名 -> 字段类型
    description: Optional[str]
    created_at: datetime
    updated_at: datetime

@dataclass
class LogCollectConfig:
    """日志采集配置"""
    id: str
    server_id: str
    name: str
    path: str
    rule_id: str
    enabled: bool
    created_at: datetime
    updated_at: datetime 