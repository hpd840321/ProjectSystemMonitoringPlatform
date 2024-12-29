from datetime import datetime
from typing import List
import aiohttp
import smtplib
from email.mime.text import MIMEText
from .notification import NotificationChannel, AlertNotification
from .repository import AlertRepository
from app.infrastructure.config import Settings

class NotificationService:
    def __init__(
        self,
        alert_repo: AlertRepository,
        settings: Settings
    ):
        self.alert_repo = alert_repo
        self.settings = settings
    
    async def send_notifications(
        self,
        alert_id: str,
        channels: List[NotificationChannel]
    ) -> List[AlertNotification]:
        """发送告警通知"""
        notifications = []
        
        for channel in channels:
            if not channel.enabled:
                continue
                
            try:
                if channel.type == "email":
                    await self._send_email(alert_id, channel)
                elif channel.type == "webhook":
                    await self._send_webhook(alert_id, channel)
                elif channel.type == "sms":
                    await self._send_sms(alert_id, channel)
                
                notification = AlertNotification(
                    alert_id=alert_id,
                    channel_id=channel.id,
                    sent_at=datetime.now(),
                    status="success",
                    error=None
                )
            except Exception as e:
                notification = AlertNotification(
                    alert_id=alert_id,
                    channel_id=channel.id,
                    sent_at=datetime.now(),
                    status="failed",
                    error=str(e)
                )
            
            notifications.append(notification)
            await self.alert_repo.save_notification(notification)
        
        return notifications
    
    async def _send_email(
        self,
        alert_id: str,
        channel: NotificationChannel
    ) -> None:
        """发送邮件通知"""
        alert = await self.alert_repo.get_alert(alert_id)
        if not alert:
            raise ValueError(f"Alert not found: {alert_id}")
        
        config = channel.config
        msg = MIMEText(alert.message)
        msg['Subject'] = f"[告警] {alert.rule.name}"
        msg['From'] = config['from_email']
        msg['To'] = config['to_email']
        
        with smtplib.SMTP(config['smtp_host'], config['smtp_port']) as smtp:
            if config.get('smtp_tls'):
                smtp.starttls()
            if config.get('smtp_user'):
                smtp.login(config['smtp_user'], config['smtp_password'])
            smtp.send_message(msg)
    
    async def _send_webhook(
        self,
        alert_id: str,
        channel: NotificationChannel
    ) -> None:
        """发送Webhook通知"""
        alert = await self.alert_repo.get_alert(alert_id)
        if not alert:
            raise ValueError(f"Alert not found: {alert_id}")
        
        config = channel.config
        payload = {
            "alert_id": alert.id,
            "rule_name": alert.rule.name,
            "message": alert.message,
            "level": alert.level,
            "status": alert.status,
            "created_at": alert.created_at.isoformat()
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                config['url'],
                json=payload,
                headers=config.get('headers', {})
            ) as response:
                if response.status >= 400:
                    raise ValueError(
                        f"Webhook request failed: {response.status}"
                    )
    
    async def _send_sms(
        self,
        alert_id: str,
        channel: NotificationChannel
    ) -> None:
        """发送短信通知"""
        # TODO: 实现短信发送
        raise NotImplementedError("SMS notification not implemented") 