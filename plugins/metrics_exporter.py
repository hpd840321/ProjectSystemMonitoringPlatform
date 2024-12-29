import json
from typing import Dict, Any, Optional
from app.infrastructure.plugin.base import PluginBase, PluginMetadata, PluginHook
from app.models.agent import AgentMetrics

class MetricsExporterPlugin(PluginBase, PluginHook):
    """指标导出插件"""

    @property
    def metadata(self) -> PluginMetadata:
        return PluginMetadata(
            id="metrics_exporter",
            name="Metrics Exporter",
            version="1.0.0",
            description="Export metrics to external systems",
            author="Admin",
            settings_schema={
                "export_url": {
                    "type": "string",
                    "description": "Metrics export endpoint URL"
                },
                "export_interval": {
                    "type": "integer",
                    "description": "Export interval in seconds",
                    "default": 300
                }
            }
        )

    async def install(self) -> bool:
        """安装插件"""
        # 可以在这里进行一些初始化操作
        return True

    async def uninstall(self) -> bool:
        """卸载插件"""
        # 可以在这里进行一些清理操作
        return True

    async def enable(self) -> bool:
        """启用插件"""
        # 启动指标导出任务
        return True

    async def disable(self) -> bool:
        """禁用插件"""
        # 停止指标导出任务
        return True

    async def configure(self, settings: Dict[str, Any]) -> bool:
        """配置插件"""
        # 验证和保存配置
        try:
            # 验证必要的配置项
            if "export_url" not in settings:
                raise ValueError("export_url is required")
            
            # 保存配置
            self._settings = settings
            return True
        except Exception:
            return False

    async def get_settings(self) -> Dict[str, Any]:
        """获取插件配置"""
        return self._settings

    async def health_check(self) -> bool:
        """插件健康检查"""
        try:
            # 检查导出URL是否可访问
            url = self._settings.get("export_url")
            if not url:
                return False
            
            # 这里可以添加实际的健康检查逻辑
            return True
        except Exception:
            return False

    async def before_request(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """请求前处理"""
        # 这里可以在请求前进行一些处理
        return context

    async def after_request(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """请求后处理"""
        # 如果是指标相关的请求，进行导出
        if (
            context.get("path", "").startswith("/api/v1/metrics") and
            context.get("method") == "GET"
        ):
            await self._export_metrics(context.get("response", {}))
        return context

    async def on_error(self, context: Dict[str, Any], error: Exception) -> None:
        """错误处理"""
        # 记录错误信息
        logger.error(f"Plugin error: {str(error)}")

    async def _export_metrics(self, metrics: Dict[str, Any]) -> None:
        """导出指标数据"""
        try:
            url = self._settings.get("export_url")
            if not url:
                return

            # 转换指标格式
            export_data = {
                "timestamp": datetime.now().isoformat(),
                "metrics": metrics
            }

            # 发送数据
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    url,
                    json=export_data,
                    timeout=30
                ) as response:
                    if response.status != 200:
                        logger.error(
                            f"Failed to export metrics: {response.status}"
                        )
        except Exception as e:
            logger.error(f"Error exporting metrics: {str(e)}") 