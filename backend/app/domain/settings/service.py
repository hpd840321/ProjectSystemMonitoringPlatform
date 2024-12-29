from datetime import datetime
from typing import Dict, Any, Optional
from uuid import uuid4
from .repository import SettingRepository
from .aggregate import Setting, SettingType, SystemConfig

class SettingService:
    def __init__(self, repo: SettingRepository):
        self.repo = repo
    
    async def get_system_config(self) -> SystemConfig:
        """获取系统配置"""
        settings = await self.repo.get_all_settings()
        return SystemConfig.from_settings(settings)
    
    async def update_system_config(self, config: Dict[str, Any]) -> SystemConfig:
        """更新系统配置"""
        await self.repo.update_settings(config)
        return await self.get_system_config()
    
    async def get_setting(self, key: str) -> Optional[Setting]:
        """获取设置"""
        return await self.repo.get_by_key(key)
    
    async def update_setting(
        self,
        type: str,
        key: str,
        value: Any,
        description: Optional[str] = None
    ) -> Setting:
        """更新设置"""
        now = datetime.now()
        setting = await self.repo.get_by_key(key)
        
        if setting:
            setting.value = value
            setting.description = description
            setting.updated_at = now
        else:
            setting = Setting(
                id=str(uuid4()),
                type=SettingType(type),
                key=key,
                value=value,
                description=description,
                created_at=now,
                updated_at=now
            )
        
        await self.repo.save(setting)
        return setting 