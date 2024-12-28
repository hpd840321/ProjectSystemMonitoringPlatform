from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseSender(ABC):
    """发送器基类"""
    
    @abstractmethod
    async def send(self, data: Dict[str, Any]) -> bool:
        """发送数据"""
        pass 