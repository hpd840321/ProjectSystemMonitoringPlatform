from typing import List, Dict, Optional
from datetime import datetime
from uuid import uuid4
from .repository import (
    AlertRuleRepository,
    AlertEventRepository,
    NotificationChannelRepository,
    AlertLevelRepository
)
from .aggregate import (
    AlertRule,
    AlertEvent,
    AlertStatus,
    AlertSeverity,
    NotificationChannel,
    AlertLevel,
    NotificationType
)
from ..monitor.service import MonitorService
from ...interface.api.v1.ws import broadcast_alert
from ...infrastructure.notification.sender import NotificationSender
from ...interface.ws.messages import broadcast_alert
import json
import logging

logger = logging.getLogger(__name__)

class AlertService:
    """告警服务"""
    
    def __init__(
        self,
        rule_repo: AlertRuleRepository,
        event_repo: AlertEventRepository,
        channel_repo: NotificationChannelRepository,
        monitor_service: MonitorService,
        level_repo: AlertLevelRepository,
        notification_sender: NotificationSender
    ):
        self.rule_repo = rule_repo
        self.event_repo = event_repo
        self.channel_repo = channel_repo
        self.monitor_service = monitor_service
        self.level_repo = level_repo
        self.notification_sender = notification_sender
    
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
    
    async def create_alert(
        self,
        rule_id: str,
        target: str,
        message: str,
        level_id: str,
        labels: Optional[Dict] = None
    ) -> Alert:
        """创建告警"""
        # 获取告警规则
        rule = await self.alert_repo.get_rule(rule_id)
        if not rule:
            raise ValueError(f"Alert rule not found: {rule_id}")
        
        # 获取告警级别
        level = await self.alert_repo.get_level(level_id)
        if not level:
            raise ValueError(f"Alert level not found: {level_id}")
        
        # 创建告警
        alert = Alert(
            id=str(uuid4()),
            rule=rule,
            target=target,
            message=message,
            level=level,
            status="active",
            labels=labels or {},
            created_at=datetime.now()
        )
        
        await self.alert_repo.save_alert(alert)
        
        # 获取通知渠道
        channels = await self.alert_repo.get_rule_channels(rule_id)
        
        # 发送通知
        await self.notification_service.send_notifications(
            alert.id,
            channels
        )
        
        # 广播告警
        await broadcast_alert(alert.to_dict())
        
        return alert 

    async def _send_notifications(self, alert: AlertEvent) -> None:
        """发送告警通知"""
        # 获取告警级别对应的通知渠道
        channels = await self.channel_repo.get_channels_by_level(alert.severity)
        
        # 准备通知内容
        message = {
            "subject": f"[{alert.severity}] {alert.summary}",
            "content": self._format_alert_message(alert),
            "params": {
                "severity": alert.severity,
                "summary": alert.summary,
                "details": alert.details
            }
        }
        
        # 发送通知
        for channel in channels:
            success = await self.notification_sender.send(channel, message)
            if success:
                logger.info(f"Sent alert notification via {channel.type}")
            else:
                logger.error(f"Failed to send alert notification via {channel.type}")
    
    def _format_alert_message(self, alert: AlertEvent) -> str:
        """格式化告警消息"""
        return f"""
告警级别: {alert.severity}
告警概要: {alert.summary}
服务器ID: {alert.server_id}
首次发生: {alert.first_occurred_at}
最近发生: {alert.last_occurred_at}

详细信息:
{json.dumps(alert.details, indent=2, ensure_ascii=False)}
"""

class AlertLevelService:
    def __init__(self, repo: AlertLevelRepository):
        self.repo = repo
    
    async def create_level(
        self,
        name: str,
        color: str,
        priority: int,
        description: Optional[str] = None
    ) -> AlertLevel:
        """创建告警级别"""
        now = datetime.now()
        level = AlertLevel(
            id=str(uuid4()),
            name=name,
            description=description,
            color=color,
            priority=priority,
            created_at=now,
            updated_at=now
        )
        await self.repo.save(level)
        return level
    
    async def get_level(self, level_id: str) -> AlertLevel:
        """获取告警级别"""
        return await self.repo.get_by_id(level_id)
    
    async def list_levels(self) -> List[AlertLevel]:
        """获取所有告警级别"""
        return await self.repo.list_all()

class NotificationService:
    def __init__(self, repo: NotificationChannelRepository):
        self.repo = repo
    
    async def create_channel(
        self,
        name: str,
        type: str,
        config: Dict,
        enabled: bool = True
    ) -> NotificationChannel:
        """创建通知渠道"""
        now = datetime.now()
        channel = NotificationChannel(
            id=str(uuid4()),
            name=name,
            type=NotificationType(type),
            config=config,
            enabled=enabled,
            created_at=now,
            updated_at=now
        )
        await self.repo.save(channel)
        return channel
    
    async def send_notification(
        self,
        channel_id: str,
        title: str,
        content: str
    ) -> None:
        """发送通知"""
        channel = await self.repo.get_by_id(channel_id)
        if not channel or not channel.enabled:
            return
        
        # 根据渠道类型发送通知
        if channel.type == NotificationType.EMAIL:
            await self._send_email(channel.config, title, content)
        elif channel.type == NotificationType.SMS:
            await self._send_sms(channel.config, content)
        elif channel.type == NotificationType.WEBHOOK:
            await self._send_webhook(channel.config, title, content)
        elif channel.type == NotificationType.SLACK:
            await self._send_slack(channel.config, title, content)
    
    def _validate_channel_config(self, channel: NotificationChannel) -> None:
        """验证通知渠道配置"""
        config = channel.config
        
        if channel.type == NotificationType.EMAIL:
            required = ['smtp_host', 'smtp_port', 'from_email']
        elif channel.type == NotificationType.WEBHOOK:
            required = ['url']
        elif channel.type == NotificationType.SMS:
            required = ['api_key', 'template_id']
        
        missing = [key for key in required if key not in config]
        if missing:
            raise ValueError(f"Missing required config: {', '.join(missing)}")
    
    async def get_channel(self, channel_id: str) -> NotificationChannel:
        """获取通知渠道"""
        return await self.repo.get_by_id(channel_id)
    
    async def list_channels(self) -> List[NotificationChannel]:
        """获取所有通知渠道"""
        return await self.repo.list_all()
    
    async def get_channels_by_level(self, level_id: str) -> List[NotificationChannel]:
        """获取告警级别对应的通知渠道"""
        return await self.repo.get_channels_by_level(level_id) 