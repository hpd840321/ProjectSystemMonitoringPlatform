from abc import ABC, abstractmethod
from typing import List
from .aggregate import AlertLevel, NotificationChannel

class AlertLevelRepository(ABC):
    @abstractmethod
    async def save(self, level: AlertLevel) -> None:
        pass
    
    @abstractmethod
    async def get_by_id(self, level_id: str) -> AlertLevel:
        pass
    
    @abstractmethod
    async def list_all(self) -> List[AlertLevel]:
        pass
    
    @abstractmethod
    async def delete(self, level_id: str) -> None:
        pass

class NotificationChannelRepository(ABC):
    @abstractmethod
    async def save(self, channel: NotificationChannel) -> None:
        pass
    
    @abstractmethod
    async def get_by_id(self, channel_id: str) -> NotificationChannel:
        pass
    
    @abstractmethod
    async def list_all(self) -> List[NotificationChannel]:
        pass
    
    @abstractmethod
    async def delete(self, channel_id: str) -> None:
        pass
    
    @abstractmethod
    async def get_channels_by_level(self, level_id: str) -> List[NotificationChannel]:
        pass 