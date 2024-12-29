from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import io

from app.interface.api.v1.dependencies import get_db, get_current_user
from app.interface.api.v1.schemas.report import (
    TimeRange,
    ResourceUsageReport,
    AlertReport,
    PerformanceReport,
    ReportExportFormat
)
from app.infrastructure.report.generator import report_generator
from app.models.user import User

router = APIRouter()

@router.get("/reports/resource-usage", response_model=ResourceUsageReport)
async def get_resource_usage_report(
    start_time: datetime,
    end_time: datetime = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取资源使用报表"""
    if not end_time:
        end_time = datetime.now()
    
    time_range = TimeRange(start_time=start_time, end_time=end_time)
    return await report_generator.generate_resource_usage_report(db, time_range)

@router.get("/reports/alerts", response_model=AlertReport)
async def get_alert_report(
    start_time: datetime,
    end_time: datetime = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取告警报表"""
    if not end_time:
        end_time = datetime.now()
    
    time_range = TimeRange(start_time=start_time, end_time=end_time)
    return await report_generator.generate_alert_report(db, time_range)

@router.get("/reports/performance", response_model=PerformanceReport)
async def get_performance_report(
    start_time: datetime,
    end_time: datetime = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取性能报表"""
    if not end_time:
        end_time = datetime.now()
    
    time_range = TimeRange(start_time=start_time, end_time=end_time)
    return await report_generator.generate_performance_report(db, time_range)

@router.post("/reports/export")
async def export_report(
    report_type: str = Query(..., regex="^(resource-usage|alerts|performance)$"),
    start_time: datetime = None,
    end_time: datetime = None,
    export_format: ReportExportFormat = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """导出报表"""
    if not start_time:
        start_time = datetime.now() - timedelta(days=7)
    if not end_time:
        end_time = datetime.now()
    if not export_format:
        export_format = ReportExportFormat(format="pdf", include_charts=True)
    
    time_range = TimeRange(start_time=start_time, end_time=end_time)
    
    # 生成报表数据
    if report_type == "resource-usage":
        report = await report_generator.generate_resource_usage_report(db, time_range)
    elif report_type == "alerts":
        report = await report_generator.generate_alert_report(db, time_range)
    else:  # performance
        report = await report_generator.generate_performance_report(db, time_range)
    
    # 导出报表
    report_data = await report_generator.export_report(
        report.dict(),
        export_format.format,
        export_format.include_charts
    )
    
    # 返回文件
    return StreamingResponse(
        io.BytesIO(report_data),
        media_type={
            'csv': 'text/csv',
            'pdf': 'application/pdf',
            'excel': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        }[export_format.format],
        headers={
            'Content-Disposition': f'attachment; filename="report_{report_type}_{start_time.date()}_{end_time.date()}.{export_format.format}"'
        }
    ) 