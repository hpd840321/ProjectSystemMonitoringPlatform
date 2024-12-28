from abc import ABC, abstractmethod
from typing import Dict
import smtplib
import requests
from email.mime.text import MIMEText
from app.infrastructure.config import settings

class NotificationSender(ABC):
    """通知发送器接口"""
    
    @abstractmethod
    async def send(self, config: Dict, message: str) -> bool:
        """发送通知"""
        pass

class EmailSender(NotificationSender):
    """邮件发送器"""
    
    async def send(self, config: Dict, message: str) -> bool:
        try:
            msg = MIMEText(message)
            msg['Subject'] = config.get('subject', 'Alert Notification')
            msg['From'] = settings.SMTP_FROM
            msg['To'] = config['to_address']
            
            with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
                if settings.SMTP_USE_TLS:
                    server.starttls()
                if settings.SMTP_USERNAME:
                    server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
                server.send_message(msg)
            return True
        except Exception as e:
            # TODO: 添加日志记录
            return False

class WebhookSender(NotificationSender):
    """Webhook发送器"""
    
    async def send(self, config: Dict, message: str) -> bool:
        try:
            response = requests.post(
                config['url'],
                json={'message': message},
                headers=config.get('headers', {})
            )
            return response.status_code == 200
        except Exception as e:
            # TODO: 添加日志记录
            return False 