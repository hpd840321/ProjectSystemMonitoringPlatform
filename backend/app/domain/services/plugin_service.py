from typing import Dict, Any, List
from app.domain.models.plugin import Plugin, PluginStatus
from app.domain.exceptions import PluginValidationError

class PluginDomainService:
    @staticmethod
    def validate_plugin_installation(plugin: Plugin, config: Dict[str, Any]) -> bool:
        """验证插件安装的业务规则"""
        if not plugin.validate_config(config):
            raise PluginValidationError("Invalid plugin configuration")
        return True

    @staticmethod
    def validate_plugin_dependencies(plugin: Plugin, installed_plugins: List[Plugin]) -> bool:
        """验证插件依赖关系"""
        # 实现依赖检查逻辑
        pass 