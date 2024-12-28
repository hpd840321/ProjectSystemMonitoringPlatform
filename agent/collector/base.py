from abc import ABC, abstractmethod
from typing import Any, Dict

class BaseCollector(ABC):
    """采集器基类"""
    
    @abstractmethod
    async def collect(self) -> Dict[str, Any]:
        """执行数据采集"""
        pass

    @abstractmethod
    async def validate(self, data: Dict[str, Any]) -> bool:
        """验证采集数据"""
        pass 