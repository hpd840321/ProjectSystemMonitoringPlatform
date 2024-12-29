from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from pydantic import BaseModel

class PluginMetadata(BaseModel):
    """插件元数据"""
    id: str
    name: str
    version: str
    description: str
    author: str
    dependencies: List[str] = []
    settings_schema: Optional[Dict[str, Any]] = None

class PluginBase(ABC):
    """插件基类"""

    @property
    @abstractmethod
    def metadata(self) -> PluginMetadata:
        """获取插件元数据"""
        pass

    @abstractmethod
    async def install(self) -> bool:
        """安装插件"""
        pass

    @abstractmethod
    async def uninstall(self) -> bool:
        """卸载插件"""
        pass

    @abstractmethod
    async def enable(self) -> bool:
        """启用插件"""
        pass

    @abstractmethod
    async def disable(self) -> bool:
        """禁用插件"""
        pass

    @abstractmethod
    async def configure(self, settings: Dict[str, Any]) -> bool:
        """配置插件"""
        pass

    @abstractmethod
    async def get_settings(self) -> Dict[str, Any]:
        """获取插件配置"""
        pass

    @abstractmethod
    async def health_check(self) -> bool:
        """插件健康检查"""
        pass

class PluginHook(ABC):
    """插件钩子基类"""

    @abstractmethod
    async def before_request(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """请求前处理"""
        pass

    @abstractmethod
    async def after_request(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """请求后处理"""
        pass

    @abstractmethod
    async def on_error(self, context: Dict[str, Any], error: Exception) -> None:
        """错误处理"""
        pass 