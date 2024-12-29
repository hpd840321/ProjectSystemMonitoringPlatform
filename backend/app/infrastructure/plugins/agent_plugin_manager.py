from typing import List, Dict, Any
import importlib
import logging

class AgentPluginManager:
    def __init__(self):
        self._plugins = {}
        self._logger = logging.getLogger(__name__)

    async def load_plugin(self, plugin_name: str, config: Dict[str, Any]) -> bool:
        """加载插件"""
        try:
            module = importlib.import_module(f"app.plugins.agent.{plugin_name}")
            plugin_class = getattr(module, "AgentPlugin")
            plugin_instance = plugin_class(config)
            self._plugins[plugin_name] = plugin_instance
            return True
        except Exception as e:
            self._logger.error(f"Failed to load plugin {plugin_name}: {str(e)}")
            return False

    async def process_data(self, plugin_name: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """处理插件数据"""
        if plugin_name not in self._plugins:
            raise KeyError(f"Plugin {plugin_name} not found")
        return await self._plugins[plugin_name].process_data(data)

    def get_active_plugins(self) -> List[str]:
        """获取所有活动的插件"""
        return list(self._plugins.keys()) 