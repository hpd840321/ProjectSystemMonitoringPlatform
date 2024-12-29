from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict, Any
from app.application.services.plugin_service import PluginApplicationService
from app.interfaces.api.dependencies import get_plugin_service

router = APIRouter(prefix="/api/v1/plugins")

@router.post("/install")
async def install_plugin(
    plugin_info: Dict[str, Any],
    plugin_service: PluginApplicationService = Depends(get_plugin_service)
):
    """安装插件"""
    try:
        return await plugin_service.install_plugin(plugin_info)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{plugin_name}/enable")
async def enable_plugin(
    plugin_name: str,
    plugin_service: PluginApplicationService = Depends(get_plugin_service)
):
    """启用插件"""
    try:
        return await plugin_service.enable_plugin(plugin_name)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{plugin_name}/disable")
async def disable_plugin(plugin_name: str):
    """禁用插件"""
    return await PluginService().disable_plugin(plugin_name)

@router.get("/{plugin_name}/status")
async def get_plugin_status(plugin_name: str):
    """获取插件状态"""
    return await PluginService().get_plugin_status(plugin_name) 