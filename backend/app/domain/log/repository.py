from abc import ABC, abstractmethod
from typing import List, Optional
from .aggregate import LogParseRule, LogCollectConfig

class LogParseRuleRepository(ABC):
    """日志解析规则仓储接口"""
    
    @abstractmethod
    async def save(self, rule: LogParseRule) -> None:
        """保存解析规则"""
        pass
    
    @abstractmethod
    async def get_by_id(self, rule_id: str) -> Optional[LogParseRule]:
        """获取解析规则"""
        pass
    
    @abstractmethod
    async def list_all(self) -> List[LogParseRule]:
        """获取所有解析规则"""
        pass
    
    @abstractmethod
    async def delete(self, rule_id: str) -> None:
        """删除解析规则"""
        pass

class LogCollectConfigRepository(ABC):
    """日志采集配置仓储接口"""
    
    @abstractmethod
    async def save(self, config: LogCollectConfig) -> None:
        """保存采集配置"""
        pass
    
    @abstractmethod
    async def get_by_id(self, config_id: str) -> Optional[LogCollectConfig]:
        """获取采集配置"""
        pass
    
    @abstractmethod
    async def list_by_server(self, server_id: str) -> List[LogCollectConfig]:
        """获取服务器的采集配置"""
        pass
    
    @abstractmethod
    async def delete(self, config_id: str) -> None:
        """删除采集配置"""
        pass 