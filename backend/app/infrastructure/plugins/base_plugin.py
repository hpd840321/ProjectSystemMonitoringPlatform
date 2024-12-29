from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseAgentPlugin(ABC):
    def __init__(self, config: Dict[str, Any]):
        self.config = config

    @abstractmethod
    async def process_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """处理数据的抽象方法"""
        pass

    @abstractmethod
    async def validate_config(self) -> bool:
        """验证配置的抽象方法"""
        pass 