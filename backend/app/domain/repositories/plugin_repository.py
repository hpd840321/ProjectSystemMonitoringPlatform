from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.models.plugin import Plugin

class IPluginRepository(ABC):
    @abstractmethod
    async def save(self, plugin: Plugin) -> str:
        """保存插件"""
        pass

    @abstractmethod
    async def get_by_id(self, plugin_id: str) -> Optional[Plugin]:
        """根据ID获取插件"""
        pass

    @abstractmethod
    async def get_by_name(self, name: str) -> Optional[Plugin]:
        """根据名称获取插件"""
        pass

    @abstractmethod
    async def list_active_plugins(self) -> List[Plugin]:
        """获取所有活动的插件"""
        pass

    @abstractmethod
    async def update_status(self, plugin_id: str, status: str) -> bool:
        """更新插件状态"""
        pass 