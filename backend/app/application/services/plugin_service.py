from typing import Dict, Any, List
from app.domain.models.plugin import Plugin, PluginStatus
from app.domain.services.plugin_service import PluginDomainService
from app.domain.repositories.plugin_repository import IPluginRepository
from app.infrastructure.plugins.agent_plugin_manager import AgentPluginManager

class PluginApplicationService:
    def __init__(
        self,
        plugin_repository: IPluginRepository,
        plugin_manager: AgentPluginManager,
        plugin_domain_service: PluginDomainService
    ):
        self.plugin_repository = plugin_repository
        self.plugin_manager = plugin_manager
        self.plugin_domain_service = plugin_domain_service

    async def install_plugin(self, plugin_info: Dict[str, Any]) -> bool:
        """安装插件"""
        try:
            # 创建插件领域模型
            plugin = Plugin(
                id=None,
                name=plugin_info["name"],
                version=plugin_info["version"],
                description=plugin_info.get("description"),
                entry_point=plugin_info["entry_point"],
                config_schema=plugin_info["config_schema"],
                status=PluginStatus.INACTIVE,
                created_at=None,
                updated_at=None
            )

            # 验证插件
            self.plugin_domain_service.validate_plugin_installation(
                plugin, 
                plugin_info.get("config", {})
            )

            # 保存到数据库
            plugin_id = await self.plugin_repository.save(plugin)

            # 加载插件
            return await self.plugin_manager.load_plugin(
                plugin.name,
                plugin_info.get("config", {})
            )

        except Exception as e:
            # 处理异常
            raise

    async def enable_plugin(self, plugin_name: str) -> bool:
        """启用插件"""
        plugin = await self.plugin_repository.get_by_name(plugin_name)
        if not plugin:
            raise ValueError(f"Plugin {plugin_name} not found")

        # 更新状态
        await self.plugin_repository.update_status(
            plugin.id, 
            PluginStatus.ACTIVE.value
        )
        return True 