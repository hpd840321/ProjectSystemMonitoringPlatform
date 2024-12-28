from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.application.alert.service import AlertApplicationService
from app.application.alert.dto import (
    AlertRuleCreateDTO,
    AlertRuleDTO,
    AlertEventDTO,
    NotificationChannelCreateDTO,
    NotificationChannelDTO
)
from .dependencies import get_alert_service, get_current_user
from app.interface.api.decorators import require_roles
from app.domain.user.aggregate import UserRole

router = APIRouter()

@router.post(
    "/projects/{project_id}/alert-rules",
    response_model=AlertRuleDTO,
    dependencies=[Depends(require_roles([UserRole.ADMIN, UserRole.PROJECT_ADMIN]))]
)
async def create_alert_rule(
    project_id: str,
    dto: AlertRuleCreateDTO,
    service: AlertApplicationService = Depends(get_alert_service),
    current_user = Depends(get_current_user)
) -> AlertRuleDTO:
    """创建告警规则"""
    return await service.create_alert_rule(project_id, dto)

@router.get(
    "/projects/{project_id}/alert-rules",
    response_model=List[AlertRuleDTO]
)
async def list_alert_rules(
    project_id: str,
    service: AlertApplicationService = Depends(get_alert_service),
    current_user = Depends(get_current_user)
) -> List[AlertRuleDTO]:
    """获取告警规则列表"""
    return await service.list_alert_rules(project_id)

@router.get(
    "/servers/{server_id}/alerts",
    response_model=List[AlertEventDTO]
)
async def list_server_alerts(
    server_id: str,
    service: AlertApplicationService = Depends(get_alert_service),
    current_user = Depends(get_current_user)
) -> List[AlertEventDTO]:
    """获取服务器告警历史"""
    return await service.list_server_alerts(server_id)

@router.post(
    "/projects/{project_id}/notification-channels",
    response_model=NotificationChannelDTO,
    dependencies=[Depends(require_roles([UserRole.ADMIN, UserRole.PROJECT_ADMIN]))]
)
async def create_notification_channel(
    project_id: str,
    dto: NotificationChannelCreateDTO,
    service: AlertApplicationService = Depends(get_alert_service),
    current_user = Depends(get_current_user)
) -> NotificationChannelDTO:
    """创建通知渠道"""
    return await service.create_notification_channel(project_id, dto) 