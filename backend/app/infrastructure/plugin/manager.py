import os
import importlib
import logging
from typing import Dict, List, Type, Optional
from sqlalchemy.orm import Session

from app.infrastructure.plugin.base import PluginBase, PluginMetadata
from app.models.plugin import Plugin as PluginModel
from app.interface.api.v1.schemas.plugin import PluginCreate, PluginUpdate

logger = logging.getLogger(__name__)

class PluginManager:
    """插件管理器"""

    def __init__(self):
        self._plugins: Dict[str, PluginBase] = {}
        self._enabled_plugins: Dict[str, PluginBase] = {}
        self._plugin_dir = "plugins"

    async def load_plugins(self, db: Session) -> None:
        """加载所有插件"""
        # 确保插件目录存在
        if not os.path.exists(self._plugin_dir):
            os.makedirs(self._plugin_dir)

        # 从数据库加载插件信息
        db_plugins = db.query(PluginModel).all()
        
        for plugin_file in os.listdir(self._plugin_dir):
            if plugin_file.endswith(".py"):
                try:
                    # 动态导入插件模块
                    module_name = plugin_file[:-3]
                    module = importlib.import_module(f"{self._plugin_dir}.{module_name}")
                    
                    # 查找插件类
                    for attr_name in dir(module):
                        attr = getattr(module, attr_name)
                        if (isinstance(attr, type) and 
                            issubclass(attr, PluginBase) and 
                            attr != PluginBase):
                            plugin = attr()
                            self._plugins[plugin.metadata.id] = plugin
                            
                            # 如果插件在数据库中且已启用，则启用插件
                            db_plugin = next(
                                (p for p in db_plugins if p.id == plugin.metadata.id),
                                None
                            )
                            if db_plugin and db_plugin.enabled:
                                await self.enable_plugin(plugin.metadata.id)
                                
                except Exception as e:
                    logger.error(f"Failed to load plugin {plugin_file}: {str(e)}")

    async def install_plugin(
        self,
        db: Session,
        plugin_id: str
    ) -> Optional[PluginModel]:
        """安装插件"""
        if plugin_id not in self._plugins:
            return None
            
        plugin = self._plugins[plugin_id]
        if await plugin.install():
            # 创建数据库记录
            db_obj = PluginModel(
                id=plugin.metadata.id,
                name=plugin.metadata.name,
                version=plugin.metadata.version,
                description=plugin.metadata.description,
                author=plugin.metadata.author,
                enabled=False
            )
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            return db_obj
        return None

    async def uninstall_plugin(
        self,
        db: Session,
        plugin_id: str
    ) -> bool:
        """卸载插件"""
        if plugin_id not in self._plugins:
            return False
            
        plugin = self._plugins[plugin_id]
        if await plugin.uninstall():
            # 删除数据库记录
            db_obj = db.query(PluginModel).get(plugin_id)
            if db_obj:
                db.delete(db_obj)
                db.commit()
            return True
        return False

    async def enable_plugin(self, plugin_id: str) -> bool:
        """启用插件"""
        if plugin_id not in self._plugins:
            return False
            
        plugin = self._plugins[plugin_id]
        if await plugin.enable():
            self._enabled_plugins[plugin_id] = plugin
            return True
        return False

    async def disable_plugin(self, plugin_id: str) -> bool:
        """禁用插件"""
        if plugin_id not in self._enabled_plugins:
            return False
            
        plugin = self._enabled_plugins[plugin_id]
        if await plugin.disable():
            del self._enabled_plugins[plugin_id]
            return True
        return False

    async def configure_plugin(
        self,
        plugin_id: str,
        settings: Dict[str, Any]
    ) -> bool:
        """配置插件"""
        if plugin_id not in self._plugins:
            return False
            
        plugin = self._plugins[plugin_id]
        return await plugin.configure(settings)

    def get_plugin(self, plugin_id: str) -> Optional[PluginBase]:
        """获取插件实例"""
        return self._plugins.get(plugin_id)

    def get_enabled_plugins(self) -> List[PluginBase]:
        """获取所有已启用的插件"""
        return list(self._enabled_plugins.values())

    def get_all_plugins(self) -> List[PluginBase]:
        """获取所有插件"""
        return list(self._plugins.values())

    async def run_plugin_hooks(
        self,
        hook_name: str,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """运行插件钩子"""
        for plugin in self._enabled_plugins.values():
            try:
                if hasattr(plugin, hook_name):
                    hook = getattr(plugin, hook_name)
                    context = await hook(context)
            except Exception as e:
                logger.error(f"Error running plugin hook {hook_name}: {str(e)}")
        return context

plugin_manager = PluginManager() 