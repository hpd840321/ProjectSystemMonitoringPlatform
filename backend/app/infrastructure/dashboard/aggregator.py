from typing import List, Dict, Any
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.agent import Agent, AgentMetrics
from app.models.project import Project
from app.models.alert import Alert
from app.models.audit import AuditLog
from app.interface.api.v1.schemas.dashboard import (
    SystemStatus,
    ResourceUsage,
    ResourceTrend,
    AlertSummary,
    RecentEvent
)

class DashboardAggregator:
    """仪表盘数据聚合器"""

    def get_system_status(self, db: Session) -> SystemStatus:
        """获取系统状态"""
        total_servers = db.query(func.count(Agent.id)).scalar()
        online_servers = db.query(func.count(Agent.id))\
                          .filter(Agent.status == "online")\
                          .scalar()
        
        total_projects = db.query(func.count(Project.id)).scalar()
        active_projects = db.query(func.count(Project.id))\
                           .filter(Project.status == "active")\
                           .scalar()
        
        return SystemStatus(
            total_servers=total_servers,
            online_servers=online_servers,
            total_projects=total_projects,
            active_projects=active_projects
        )

    def get_resource_usage(self, db: Session) -> ResourceUsage:
        """获取当前资源使用情况"""
        # 获取最近的指标数据
        latest_metrics = db.query(AgentMetrics)\
                         .order_by(AgentMetrics.timestamp.desc())\
                         .limit(1)\
                         .first()
        
        if not latest_metrics:
            return ResourceUsage(
                cpu_usage=0,
                memory_usage=0,
                disk_usage=0,
                network_in=0,
                network_out=0,
                timestamp=datetime.now()
            )
        
        return ResourceUsage(
            cpu_usage=latest_metrics.cpu_usage,
            memory_usage=latest_metrics.memory_usage,
            disk_usage=latest_metrics.disk_usage,
            network_in=latest_metrics.network_in,
            network_out=latest_metrics.network_out,
            timestamp=latest_metrics.timestamp
        )

    def get_resource_trends(
        self, db: Session, *, hours: int = 24
    ) -> ResourceTrend:
        """获取资源使用趋势"""
        start_time = datetime.now() - timedelta(hours=hours)
        
        # 获取时间段内的指标数据
        metrics = db.query(AgentMetrics)\
                   .filter(AgentMetrics.timestamp >= start_time)\
                   .order_by(AgentMetrics.timestamp.asc())\
                   .all()
        
        return ResourceTrend(
            timestamps=[m.timestamp for m in metrics],
            cpu_usage=[m.cpu_usage for m in metrics],
            memory_usage=[m.memory_usage for m in metrics],
            disk_usage=[m.disk_usage for m in metrics],
            network_in=[m.network_in for m in metrics],
            network_out=[m.network_out for m in metrics]
        )

    def get_alert_summary(self, db: Session) -> AlertSummary:
        """获取告警统计"""
        # 获取总数
        total = db.query(func.count(Alert.id)).scalar()
        
        # 按严重程度统计
        by_severity = dict(
            db.query(
                Alert.severity,
                func.count(Alert.id)
            ).group_by(Alert.severity).all()
        )
        
        # 按状态统计
        by_status = dict(
            db.query(
                Alert.status,
                func.count(Alert.id)
            ).group_by(Alert.status).all()
        )
        
        # 获取最近的告警
        recent_alerts = db.query(Alert)\
                        .order_by(Alert.created_at.desc())\
                        .limit(5)\
                        .all()
        
        return AlertSummary(
            total=total,
            by_severity=by_severity,
            by_status=by_status,
            recent_alerts=[alert.to_dict() for alert in recent_alerts]
        )

    def get_recent_events(
        self, db: Session, *, limit: int = 10
    ) -> List[RecentEvent]:
        """获取最近事件"""
        events = db.query(AuditLog)\
                  .order_by(AuditLog.created_at.desc())\
                  .limit(limit)\
                  .all()
        
        return [
            RecentEvent(
                id=event.id,
                event_type=event.action,
                resource_type=event.resource_type,
                resource_name=event.details.get("resource_name", ""),
                message=event.details.get("message", ""),
                severity=event.details.get("severity", "info"),
                timestamp=event.created_at
            )
            for event in events
        ]

    def get_alert_trends(
        self, db: Session, *, days: int = 7
    ) -> Dict[str, List[int]]:
        """获取告警趋势"""
        start_time = datetime.now() - timedelta(days=days)
        
        # 按天和严重程度统计告警数量
        stats = db.query(
            func.date_trunc('day', Alert.created_at).label('day'),
            Alert.severity,
            func.count(Alert.id).label('count')
        ).filter(
            Alert.created_at >= start_time
        ).group_by(
            'day',
            Alert.severity
        ).all()
        
        # 整理数据格式
        trends = {}
        for day, severity, count in stats:
            if severity not in trends:
                trends[severity] = [0] * days
            day_index = (day.date() - start_time.date()).days
            if 0 <= day_index < days:
                trends[severity][day_index] = count
        
        return trends

dashboard = DashboardAggregator()