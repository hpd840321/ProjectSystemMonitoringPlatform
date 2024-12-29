from fastapi import APIRouter, Depends, HTTPException
from typing import List
from .dependencies import get_current_user, get_alert_level_service, get_notification_service
from .schemas.alert import (
    AlertLevelCreate,
    AlertLevelResponse,
    NotificationChannelCreate,
    NotificationChannelResponse,
    ChannelTestRequest
)

router = APIRouter()

# 告警级别管理
@router.post("/alert-levels", response_model=AlertLevelResponse)
async def create_alert_level(
    data: AlertLevelCreate,
    service = Depends(get_alert_level_service),
    user = Depends(get_current_user)
):
    """创建告警级别"""
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="需要管理员权限")
    
    level = await service.create_level(
        name=data.name,
        color=data.color,
        priority=data.priority,
        description=data.description
    )
    return AlertLevelResponse.from_domain(level)

@router.get("/alert-levels", response_model=List[AlertLevelResponse])
async def list_alert_levels(
    service = Depends(get_alert_level_service)
):
    """获取告警级别列表"""
    levels = await service.list_levels()
    return [AlertLevelResponse.from_domain(l) for l in levels]

# 通知渠道管理
@router.post("/notification-channels", response_model=NotificationChannelResponse)
async def create_notification_channel(
    data: NotificationChannelCreate,
    service = Depends(get_notification_service),
    user = Depends(get_current_user)
):
    """创建通知渠道"""
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="需要管理员权限")
    
    channel = await service.create_channel(
        name=data.name,
        type=data.type,
        config=data.config,
        enabled=data.enabled
    )
    return NotificationChannelResponse.from_domain(channel)

@router.get("/notification-channels", response_model=List[NotificationChannelResponse])
async def list_notification_channels(
    service = Depends(get_notification_service)
):
    """获取通知渠道列表"""
    channels = await service.list_channels()
    return [NotificationChannelResponse.from_domain(c) for c in channels]

@router.post("/notification-channels/{channel_id}/test")
async def test_notification_channel(
    channel_id: str,
    data: ChannelTestRequest,
    service = Depends(get_notification_service),
    user = Depends(get_current_user)
):
    """测试通知渠道"""
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="需要管理员权限")
    
    success = await service.send_notification(
        channel_id=channel_id,
        title=data.title,
        content=data.content
    )
    
    if not success:
        raise HTTPException(status_code=500, detail="发送测试消息失败")
    return {"message": "测试消息发送成功"} 