from abc import ABC, abstractmethod
from typing import List, Optional
from .aggregate import AlertRule, AlertEvent, NotificationChannel

class AlertRuleRepository(ABC):
    """告警规则仓储接口"""
    
    @abstractmethod
    async def save(self, rule: AlertRule) -> None:
        """保存告警规则"""
        pass
    
    @abstractmethod
    async def get_by_id(self, rule_id: str) -> Optional[AlertRule]:
        """获取告警规则"""
        pass
    
    @abstractmethod
    async def list_by_project(self, project_id: str) -> List[AlertRule]:
        """获取项目告警规则"""
        pass

class AlertEventRepository(ABC):
    """告警事件仓储接口"""
    
    @abstractmethod
    async def save(self, event: AlertEvent) -> None:
        """保存告警事件"""
        pass
    
    @abstractmethod
    async def get_active_by_rule(self, rule_id: str) -> List[AlertEvent]:
        """获取规则的活动告警"""
        pass
    
    @abstractmethod
    async def list_by_server(
        self,
        server_id: str,
        limit: int = 100
    ) -> List[AlertEvent]:
        """获取服务器告警历史"""
        pass

class NotificationChannelRepository(ABC):
    """通知渠道仓储接口"""
    
    @abstractmethod
    async def save(self, channel: NotificationChannel) -> None:
        """保存通知渠道"""
        pass
    
    @abstractmethod
    async def list_by_project(self, project_id: str) -> List[NotificationChannel]:
        """获取项目通知渠道"""
        pass 