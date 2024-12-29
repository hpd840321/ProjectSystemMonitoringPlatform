from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.interface.api.v1.dependencies import get_db, get_current_user
from app.interface.api.v1.schemas.audit import (
    AuditLogInDB,
    AuditLogFilter
)
from app.crud import audit_log
from app.models.user import User

router = APIRouter()

@router.get("/audit-logs", response_model=List[AuditLogInDB])
async def list_audit_logs(
    user_id: Optional[int] = None,
    username: Optional[str] = None,
    action: Optional[str] = None,
    resource_type: Optional[str] = None,
    resource_id: Optional[str] = None,
    status: Optional[str] = None,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取审计日志列表"""
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    filter_params = AuditLogFilter(
        user_id=user_id,
        username=username,
        action=action,
        resource_type=resource_type,
        resource_id=resource_id,
        status=status,
        start_time=start_time,
        end_time=end_time
    )
    
    return await audit_log.get_multi(
        db,
        filter_params=filter_params,
        skip=skip,
        limit=limit
    )

@router.get("/audit-logs/summary")
async def get_audit_summary(
    days: int = Query(7, ge=1, le=30),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取审计日志统计"""
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    end_time = datetime.now()
    start_time = end_time - timedelta(days=days)
    
    return await audit_log.get_actions_summary(
        db,
        start_time=start_time,
        end_time=end_time
    ) 