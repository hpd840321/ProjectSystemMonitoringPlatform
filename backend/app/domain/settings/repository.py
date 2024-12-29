from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from .aggregate import Setting, SettingType

class SettingRepository(ABC):
    """系统设置仓储接口"""
    
    @abstractmethod
    async def save(self, setting: Setting) -> None:
        """保存设置"""
        pass
    
    @abstractmethod
    async def get_by_key(self, key: str) -> Optional[Setting]:
        """获取设置"""
        pass
    
    @abstractmethod
    async def list_by_type(self, type: SettingType) -> List[Setting]:
        """获取指定类型的设置列表"""
        pass
    
    @abstractmethod
    async def get_all_settings(self) -> Dict[str, Any]:
        """获取所有设置"""
        pass
    
    @abstractmethod
    async def update_settings(self, settings: Dict[str, Any]) -> None:
        """批量更新设置"""
        pass 