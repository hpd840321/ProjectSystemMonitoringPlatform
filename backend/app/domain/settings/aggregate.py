from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional, Dict, Any

class SettingType(str, Enum):
    SYSTEM = "system"    # 系统设置
    SECURITY = "security"  # 安全设置
    MONITOR = "monitor"   # 监控设置
    BACKUP = "backup"    # 备份设置
    ALERT = "alert"     # 告警设置
    LOG = "log"         # 日志设置

@dataclass
class Setting:
    """系统设置"""
    id: str
    type: SettingType
    key: str
    value: Any
    description: Optional[str]
    created_at: datetime
    updated_at: datetime

@dataclass
class SystemConfig:
    """系统配置"""
    # 基本设置
    site_name: str
    site_url: str
    admin_email: str
    
    # 安全设置
    password_min_length: int
    password_expire_days: int
    session_timeout: int
    allowed_ips: list
    
    # 监控设置
    metric_retention_days: int
    metric_collect_interval: int
    
    # 备份设置
    backup_retention_days: int
    backup_max_size: int
    
    # 告警设置
    alert_check_interval: int
    alert_max_retry: int
    
    # 日志设置
    log_retention_days: int
    log_max_size: int
    
    @classmethod
    def from_settings(cls, settings: Dict[str, Any]):
        """从设置字典创建配置"""
        return cls(
            site_name=settings.get("site_name", "Server Monitor"),
            site_url=settings.get("site_url", "http://localhost"),
            admin_email=settings.get("admin_email", "admin@example.com"),
            password_min_length=settings.get("password_min_length", 8),
            password_expire_days=settings.get("password_expire_days", 90),
            session_timeout=settings.get("session_timeout", 30),
            allowed_ips=settings.get("allowed_ips", []),
            metric_retention_days=settings.get("metric_retention_days", 30),
            metric_collect_interval=settings.get("metric_collect_interval", 60),
            backup_retention_days=settings.get("backup_retention_days", 7),
            backup_max_size=settings.get("backup_max_size", 1024 * 1024 * 1024),
            alert_check_interval=settings.get("alert_check_interval", 60),
            alert_max_retry=settings.get("alert_max_retry", 3),
            log_retention_days=settings.get("log_retention_days", 30),
            log_max_size=settings.get("log_max_size", 100 * 1024 * 1024)
        ) 