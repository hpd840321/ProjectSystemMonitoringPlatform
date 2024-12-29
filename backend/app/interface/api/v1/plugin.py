from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.interface.api.v1.dependencies import get_db, get_current_user
from app.interface.api.v1.schemas.plugin import (
    PluginCreate,
    PluginUpdate,
    PluginInDB,
    PluginStatus
)
from app.infrastructure.plugin.manager import plugin_manager
from app.models.user import User

router = APIRouter()

@router.get("/plugins", response_model=List[PluginInDB])
async def list_plugins(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取插件列表"""
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return plugin_manager.get_all_plugins()

@router.post("/plugins/{plugin_id}/install", response_model=PluginInDB)
async def install_plugin(
    plugin_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """安装插件"""
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    result = await plugin_manager.install_plugin(db, plugin_id)
    if not result:
        raise HTTPException(status_code=400, detail="Failed to install plugin")
    return result

@router.post("/plugins/{plugin_id}/uninstall")
async def uninstall_plugin(
    plugin_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """卸载插件"""
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    success = await plugin_manager.uninstall_plugin(db, plugin_id)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to uninstall plugin")
    return {"msg": "Plugin uninstalled successfully"}

@router.post("/plugins/{plugin_id}/enable")
async def enable_plugin(
    plugin_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """启用插件"""
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    success = await plugin_manager.enable_plugin(plugin_id)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to enable plugin")
    return {"msg": "Plugin enabled successfully"}

@router.post("/plugins/{plugin_id}/disable")
async def disable_plugin(
    plugin_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """禁用插件"""
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    success = await plugin_manager.disable_plugin(plugin_id)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to disable plugin")
    return {"msg": "Plugin disabled successfully"}

@router.put("/plugins/{plugin_id}/configure")
async def configure_plugin(
    plugin_id: str,
    settings: Dict[str, Any],
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """配置插件"""
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    success = await plugin_manager.configure_plugin(plugin_id, settings)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to configure plugin")
    return {"msg": "Plugin configured successfully"}

@router.get("/plugins/{plugin_id}/status", response_model=PluginStatus)
async def get_plugin_status(
    plugin_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取插件状态"""
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    plugin = plugin_manager.get_plugin(plugin_id)
    if not plugin:
        raise HTTPException(status_code=404, detail="Plugin not found")
    
    try:
        health = await plugin.health_check()
        return {
            "id": plugin_id,
            "enabled": plugin_id in plugin_manager._enabled_plugins,
            "health": health,
            "error": None
        }
    except Exception as e:
        return {
            "id": plugin_id,
            "enabled": plugin_id in plugin_manager._enabled_plugins,
            "health": False,
            "error": str(e)
        } 