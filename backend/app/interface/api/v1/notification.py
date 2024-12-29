from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.interface.api.v1.dependencies import get_db, get_current_user
from app.interface.api.v1.schemas.notification import (
    NotificationChannelCreate,
    NotificationChannelUpdate,
    NotificationChannelInDB,
    NotificationTemplateCreate,
    NotificationTemplateUpdate,
    NotificationTemplateInDB,
    NotificationLogInDB
)
from app.crud import notification_channel, notification_template, notification_log
from app.models.user import User

router = APIRouter()

# 通知渠道管理接口
@router.get("/notification-channels", response_model=List[NotificationChannelInDB])
async def list_notification_channels(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取通知渠道列表"""
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return await notification_channel.get_multi(db, skip=skip, limit=limit)

@router.post("/notification-channels", response_model=NotificationChannelInDB)
async def create_notification_channel(
    channel_in: NotificationChannelCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """创建通知渠道"""
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    db_obj = await notification_channel.get_by_name(db, name=channel_in.name)
    if db_obj:
        raise HTTPException(
            status_code=400,
            detail="Channel with this name already exists"
        )
    return await notification_channel.create(db, obj_in=channel_in)

@router.put("/notification-channels/{channel_id}", response_model=NotificationChannelInDB)
async def update_notification_channel(
    channel_id: int,
    channel_in: NotificationChannelUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """更新通知渠道"""
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    db_obj = await notification_channel.get(db, id=channel_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Channel not found")
    return await notification_channel.update(db, db_obj=db_obj, obj_in=channel_in)

@router.delete("/notification-channels/{channel_id}")
async def delete_notification_channel(
    channel_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """删除通知渠道"""
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    await notification_channel.delete(db, id=channel_id)
    return {"msg": "Channel deleted successfully"}

# 通知模板管理接口
@router.get("/notification-templates", response_model=List[NotificationTemplateInDB])
async def list_notification_templates(
    type: str = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取通知模板列表"""
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    if type:
        return await notification_template.get_by_type(db, type=type)
    return await notification_template.get_multi(db, skip=skip, limit=limit)

@router.post("/notification-templates", response_model=NotificationTemplateInDB)
async def create_notification_template(
    template_in: NotificationTemplateCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """创建通知模板"""
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    db_obj = await notification_template.get_by_name(db, name=template_in.name)
    if db_obj:
        raise HTTPException(
            status_code=400,
            detail="Template with this name already exists"
        )
    return await notification_template.create(db, obj_in=template_in)

@router.put("/notification-templates/{template_id}", response_model=NotificationTemplateInDB)
async def update_notification_template(
    template_id: int,
    template_in: NotificationTemplateUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """更新通知模板"""
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    db_obj = await notification_template.get(db, id=template_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Template not found")
    return await notification_template.update(db, db_obj=db_obj, obj_in=template_in)

@router.delete("/notification-templates/{template_id}")
async def delete_notification_template(
    template_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """删除通知模板"""
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    await notification_template.delete(db, id=template_id)
    return {"msg": "Template deleted successfully"}

# 通知日志查询接口
@router.get("/notification-logs", response_model=List[NotificationLogInDB])
async def list_notification_logs(
    channel_id: int = None,
    template_id: int = None,
    event_type: str = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取通知日志列表"""
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    return await notification_log.get_multi(
        db,
        channel_id=channel_id,
        template_id=template_id,
        event_type=event_type,
        skip=skip,
        limit=limit
    ) 