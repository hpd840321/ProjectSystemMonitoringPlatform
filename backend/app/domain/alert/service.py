from typing import List, Dict
from datetime import datetime
from uuid import uuid4
from .repository import (
    AlertRuleRepository,
    AlertEventRepository,
    NotificationChannelRepository
)
from .aggregate import (
    AlertRule,
    AlertEvent,
    AlertStatus,
    AlertSeverity,
    NotificationChannel
)
from ..monitor.service import MonitorService

class AlertService:
    """告警服务"""
    
    def __init__(
        self,
        rule_repo: AlertRuleRepository,
        event_repo: AlertEventRepository,
        channel_repo: NotificationChannelRepository,
        monitor_service: MonitorService
    ):
        self.rule_repo = rule_repo
        self.event_repo = event_repo
        self.channel_repo = channel_repo
        self.monitor_service = monitor_service
    
    async def create_rule(
        self,
        project_id: str,
        name: str,
        description: str,
        metric_type: str,
        condition: str,
        severity: AlertSeverity,
        interval: int = 60
    ) -> AlertRule:
        """创建告警规则"""
        now = datetime.now()
        rule = AlertRule(
            id=str(uuid4()),
            project_id=project_id,
            name=name,
            description=description,
            metric_type=metric_type,
            condition=condition,
            severity=severity,
            interval=interval,
            enabled=True,
            created_at=now,
            updated_at=now
        )
        await self.rule_repo.save(rule)
        return rule
    
    async def check_alerts(self, server_id: str) -> None:
        """检查服务器告警"""
        # 获取最新指标
        metrics = await self.monitor_service.get_server_metrics(
            server_id=server_id,
            hours=1
        )
        
        # 获取告警规则
        rules = await self.rule_repo.list_by_project(server_id)
        
        for rule in rules:
            if not rule.enabled:
                continue
                
            # 评估告警条件
            if self._evaluate_condition(rule.condition, metrics):
                await self._create_or_update_alert(rule, server_id, metrics)
            else:
                await self._resolve_alerts(rule.id, server_id)
    
    async def _create_or_update_alert(
        self,
        rule: AlertRule,
        server_id: str,
        metrics: Dict
    ) -> None:
        """创建或更新告警"""
        now = datetime.now()
        
        # 检查是否存在活动告警
        active_alerts = await self.event_repo.get_active_by_rule(rule.id)
        existing = next(
            (a for a in active_alerts if a.server_id == server_id),
            None
        )
        
        if existing:
            # 更新现有告警
            existing.last_occurred_at = now
            await self.event_repo.save(existing)
        else:
            # 创建新告警
            event = AlertEvent(
                id=str(uuid4()),
                rule_id=rule.id,
                server_id=server_id,
                status=AlertStatus.FIRING,
                severity=rule.severity,
                summary=f"Alert: {rule.name}",
                details=metrics,
                first_occurred_at=now,
                last_occurred_at=now,
                resolved_at=None,
                notification_sent=False
            )
            await self.event_repo.save(event)
            
            # 发送通知
            await self._send_notifications(event)
    
    async def _resolve_alerts(self, rule_id: str, server_id: str) -> None:
        """解决告警"""
        active_alerts = await self.event_repo.get_active_by_rule(rule_id)
        for alert in active_alerts:
            if alert.server_id == server_id:
                alert.status = AlertStatus.RESOLVED
                alert.resolved_at = datetime.now()
                await self.event_repo.save(alert) 