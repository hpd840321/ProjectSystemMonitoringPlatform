from abc import ABC, abstractmethod
from typing import Dict, Any
import smtplib
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.infrastructure.config import settings
import aiohttp
import logging
from ...domain.alert.aggregate import NotificationType, NotificationChannel
import json

logger = logging.getLogger(__name__)

class NotificationSender(ABC):
    """通知发送器接口"""
    
    @abstractmethod
    async def send(self, channel: NotificationChannel, message: Dict[str, Any]) -> bool:
        """发送通知"""
        pass

class EmailSender(NotificationSender):
    """邮件发送器"""
    
    async def send(self, channel: NotificationChannel, message: Dict[str, Any]) -> bool:
        """发送通知"""
        try:
            if channel.type == NotificationType.EMAIL:
                return await self._send_email(channel.config, message)
            elif channel.type == NotificationType.WEBHOOK:
                return await self._send_webhook(channel.config, message)
            elif channel.type == NotificationType.SMS:
                return await self._send_sms(channel.config, message)
            elif channel.type == NotificationType.SLACK:
                return await self._send_slack(channel.config, message)
            else:
                logger.error(f"Unsupported notification type: {channel.type}")
                return False
        except Exception as e:
            logger.error(f"Failed to send notification: {str(e)}")
            return False
    
    async def _send_email(self, config: Dict, message: Dict) -> bool:
        """发送邮件"""
        try:
            msg = MIMEMultipart()
            msg['From'] = config['from_email']
            msg['To'] = config['to_email']
            msg['Subject'] = message['subject']
            
            body = MIMEText(message['content'], 'plain')
            msg.attach(body)
            
            with smtplib.SMTP(config['smtp_host'], config['smtp_port']) as server:
                if config.get('use_tls'):
                    server.starttls()
                if config.get('username') and config.get('password'):
                    server.login(config['username'], config['password'])
                server.send_message(msg)
            return True
        except Exception as e:
            logger.error(f"Failed to send email: {str(e)}")
            return False
    
    async def _send_webhook(self, config: Dict, message: Dict) -> bool:
        """发送Webhook通知"""
        try:
            async with aiohttp.ClientSession() as session:
                headers = {
                    'Content-Type': 'application/json',
                    **config.get('headers', {})
                }
                payload = {
                    **message['params'],
                    'title': message['subject'],
                    'content': message['content']
                }
                async with session.post(
                    config['url'],
                    json=payload,
                    headers=headers
                ) as resp:
                    return resp.status < 400
        except Exception as e:
            logger.error(f"Failed to send webhook: {str(e)}")
            return False
    
    async def _send_sms(self, config: Dict, message: Dict) -> bool:
        """发送短信"""
        try:
            async with aiohttp.ClientSession() as session:
                # 这里使用阿里云短信服务作为示例
                payload = {
                    'AccessKeyId': config['access_key_id'],
                    'Action': 'SendSms',
                    'SignName': config['sign_name'],
                    'TemplateCode': config['template_code'],
                    'PhoneNumbers': config['phone_numbers'],
                    'TemplateParam': json.dumps(message['params'])
                }
                async with session.post(
                    'https://dysmsapi.aliyuncs.com',
                    data=payload
                ) as resp:
                    result = await resp.json()
                    return result.get('Code') == 'OK'
        except Exception as e:
            logger.error(f"Failed to send SMS: {str(e)}")
            return False
    
    async def _send_slack(self, config: Dict, message: Dict) -> bool:
        """发送Slack通知"""
        try:
            async with aiohttp.ClientSession() as session:
                payload = {
                    'text': f"*{message['subject']}*\n{message['content']}"
                }
                async with session.post(
                    config['webhook_url'],
                    json=payload
                ) as resp:
                    return resp.status == 200
        except Exception as e:
            logger.error(f"Failed to send Slack message: {str(e)}")
            return False 