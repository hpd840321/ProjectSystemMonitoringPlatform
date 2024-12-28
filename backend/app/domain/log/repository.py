from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import datetime
from .aggregate import LogEntry, LogFilter

class LogRepository(ABC):
    """日志仓储接口"""
    
    @abstractmethod
    async def save_logs(self, entries: List[LogEntry]) -> None:
        """保存日志"""
        pass
    
    @abstractmethod
    async def search_logs(
        self,
        filter: LogFilter,
        limit: int = 100,
        offset: int = 0
    ) -> List[LogEntry]:
        """搜索日志"""
        pass
    
    @abstractmethod
    async def get_log_stats(
        self,
        server_id: str,
        start_time: datetime,
        end_time: datetime
    ) -> Dict:
        """获取日志统计"""
        pass 