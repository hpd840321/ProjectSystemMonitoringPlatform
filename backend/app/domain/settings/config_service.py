from datetime import datetime
from typing import List, Optional
from uuid import uuid4
from .config import (
    NotificationSettings,
    StorageSettings,
    RetentionSettings,
    NotificationType,
    StorageType,
    DataType
)
from .repository import SettingsRepository

class ConfigService:
    def __init__(self, settings_repo: SettingsRepository):
        self.settings_repo = settings_repo
    
    async def create_notification_channel(
        self,
        type: NotificationType,
        name: str,
        config: dict,
        enabled: bool = True
    ) -> NotificationSettings:
        """创建通知渠道"""
        now = datetime.now()
        settings = NotificationSettings(
            id=str(uuid4()),
            type=type,
            name=name,
            config=config,
            enabled=enabled,
            created_at=now,
            updated_at=now
        )
        
        # 验证配置
        await self._validate_notification_config(settings)
        
        await self.settings_repo.save_notification_settings(settings)
        return settings
    
    async def create_storage_settings(
        self,
        type: StorageType,
        name: str,
        config: dict,
        is_default: bool = False
    ) -> StorageSettings:
        """创建存储配置"""
        now = datetime.now()
        settings = StorageSettings(
            id=str(uuid4()),
            type=type,
            name=name,
            config=config,
            is_default=is_default,
            created_at=now,
            updated_at=now
        )
        
        # 验证配置
        await self._validate_storage_config(settings)
        
        if is_default:
            # 清除其他默认配置
            await self.settings_repo.clear_default_storage()
        
        await self.settings_repo.save_storage_settings(settings)
        return settings
    
    async def create_retention_settings(
        self,
        data_type: DataType,
        retention_days: int,
        compression_enabled: bool = True,
        compression_days: Optional[int] = None
    ) -> RetentionSettings:
        """创建数据保留策略"""
        now = datetime.now()
        settings = RetentionSettings(
            id=str(uuid4()),
            data_type=data_type,
            retention_days=retention_days,
            compression_enabled=compression_enabled,
            compression_days=compression_days,
            created_at=now,
            updated_at=now
        )
        
        # 验证配置
        if settings.compression_enabled and not settings.compression_days:
            settings.compression_days = retention_days // 2
        
        if settings.compression_days and settings.compression_days >= settings.retention_days:
            raise ValueError("Compression days must be less than retention days")
        
        await self.settings_repo.save_retention_settings(settings)
        return settings
    
    async def _validate_notification_config(
        self,
        settings: NotificationSettings
    ) -> None:
        """验证通知配置"""
        config = settings.config
        
        if settings.type == NotificationType.EMAIL:
            required = ['smtp_host', 'smtp_port', 'from_email']
        elif settings.type == NotificationType.WEBHOOK:
            required = ['url']
        elif settings.type == NotificationType.SMS:
            required = ['api_key', 'template_id']
        
        missing = [key for key in required if key not in config]
        if missing:
            raise ValueError(f"Missing required config: {', '.join(missing)}")
    
    async def _validate_storage_config(
        self,
        settings: StorageSettings
    ) -> None:
        """验证存储配置"""
        config = settings.config
        
        if settings.type == StorageType.LOCAL:
            required = ['path']
        elif settings.type == StorageType.S3:
            required = ['endpoint', 'bucket', 'access_key', 'secret_key']
        elif settings.type == StorageType.OSS:
            required = ['endpoint', 'bucket', 'access_key', 'secret_key']
        
        missing = [key for key in required if key not in config]
        if missing:
            raise ValueError(f"Missing required config: {', '.join(missing)}") 