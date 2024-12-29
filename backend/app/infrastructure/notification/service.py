import smtplib
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Dict, Any
from jinja2 import Template
from sqlalchemy.orm import Session

from app.crud import notification_channel, notification_template, notification_log
from app.interface.api.v1.schemas.notification import (
    NotificationLogCreate,
    EmailConfig,
    WebhookConfig,
    SMSConfig
)

class NotificationService:
    """通知服务"""

    async def send_notification(
        self,
        db: Session,
        template_name: str,
        context: Dict[str, Any],
        recipients: List[str]
    ) -> bool:
        """发送通知"""
        # 获取模板
        template = await notification_template.get_by_name(db, name=template_name)
        if not template:
            raise ValueError(f"Template {template_name} not found")

        # 渲染模板
        subject = Template(template.subject_template).render(**context)
        content = Template(template.content_template).render(**context)

        # 获取所有启用的通知渠道
        channels = await notification_channel.get_enabled(db)
        
        success = True
        for channel in channels:
            try:
                # 根据渠道类型发送通知
                if channel.type == "email":
                    await self._send_email(channel.config, recipients, subject, content)
                elif channel.type == "webhook":
                    await self._send_webhook(channel.config, subject, content)
                elif channel.type == "sms":
                    await self._send_sms(channel.config, recipients, content)

                # 记录成功日志
                await notification_log.create(
                    db,
                    obj_in=NotificationLogCreate(
                        channel_id=channel.id,
                        template_id=template.id,
                        event_type=template.type,
                        recipients=recipients,
                        subject=subject,
                        content=content,
                        status="success"
                    )
                )
            except Exception as e:
                success = False
                # 记录失败日志
                await notification_log.create(
                    db,
                    obj_in=NotificationLogCreate(
                        channel_id=channel.id,
                        template_id=template.id,
                        event_type=template.type,
                        recipients=recipients,
                        subject=subject,
                        content=content,
                        status="failed",
                        error_message=str(e)
                    )
                )

        return success

    async def _send_email(
        self,
        config: Dict[str, Any],
        recipients: List[str],
        subject: str,
        content: str
    ):
        """发送邮件"""
        email_config = EmailConfig(**config)
        
        msg = MIMEMultipart()
        msg['From'] = f"{email_config.from_name} <{email_config.from_email}>"
        msg['To'] = ", ".join(recipients)
        msg['Subject'] = subject
        
        msg.attach(MIMEText(content, 'plain'))
        
        server = smtplib.SMTP(email_config.host, email_config.port)
        if email_config.use_tls:
            server.starttls()
        server.login(email_config.username, email_config.password)
        server.send_message(msg)
        server.quit()

    async def _send_webhook(
        self,
        config: Dict[str, Any],
        subject: str,
        content: str
    ):
        """发送Webhook通知"""
        webhook_config = WebhookConfig(**config)
        
        payload = {
            "subject": subject,
            "content": content
        }
        
        response = requests.request(
            method=webhook_config.method,
            url=webhook_config.url,
            headers=webhook_config.headers,
            json=payload,
            timeout=webhook_config.timeout
        )
        
        response.raise_for_status()

    async def _send_sms(
        self,
        config: Dict[str, Any],
        recipients: List[str],
        content: str
    ):
        """发送短信"""
        sms_config = SMSConfig(**config)
        
        # TODO: 实现具体的短信发送逻辑
        # 这里需要根据实际使用的短信服务商来实现
        pass

notification_service = NotificationService() 