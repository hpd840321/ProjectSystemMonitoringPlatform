from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.interface.api.v1.dependencies import get_db, get_current_user
from app.interface.api.v1.schemas.dashboard import (
    DashboardOverview,
    DashboardTrends,
    ResourceTrend,
    AlertSummary
)
from app.infrastructure.dashboard.aggregator import dashboard
from app.models.user import User

router = APIRouter()

@router.get("/dashboard/overview", response_model=DashboardOverview)
async def get_dashboard_overview(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取仪表盘概览"""
    return DashboardOverview(
        system_status=await dashboard.get_system_status(db),
        resource_usage=await dashboard.get_resource_usage(db),
        alert_summary=await dashboard.get_alert_summary(db),
        recent_events=await dashboard.get_recent_events(db)
    )

@router.get("/dashboard/trends", response_model=DashboardTrends)
async def get_dashboard_trends(
    hours: int = Query(24, ge=1, le=168),  # 最多7天
    days: int = Query(7, ge=1, le=30),     # 最多30天
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取仪表盘趋势数据"""
    return DashboardTrends(
        resource_trends=await dashboard.get_resource_trends(db, hours=hours),
        alert_trends=await dashboard.get_alert_trends(db, days=days)
    )

@router.get("/dashboard/resource-trends", response_model=ResourceTrend)
async def get_resource_trends(
    hours: int = Query(24, ge=1, le=168),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取资源使用趋势"""
    return await dashboard.get_resource_trends(db, hours=hours)

@router.get("/dashboard/alert-summary", response_model=AlertSummary)
async def get_alert_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取告警统计"""
    return await dashboard.get_alert_summary(db) 