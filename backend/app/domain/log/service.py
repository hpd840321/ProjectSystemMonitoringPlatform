from datetime import datetime
from typing import List, Dict
from uuid import uuid4
from .repository import LogRepository
from .aggregate import LogEntry, LogFilter, LogLevel
from app.infrastructure.log.parser import LogParser

class LogService:
    """日志服务"""
    
    def __init__(self, log_repo: LogRepository):
        self.log_repo = log_repo
    
    async def process_logs(
        self,
        server_id: str,
        source: str,
        lines: List[str],
        parser: LogParser
    ) -> None:
        """处理日志"""
        entries = []
        
        for line in lines:
            data = parser.parse(line)
            if not data:
                continue
                
            entry = LogEntry(
                id=str(uuid4()),
                server_id=server_id,
                timestamp=data.get('timestamp', datetime.now()),
                level=self._get_log_level(data),
                message=data.get('message', line),
                source=source,
                metadata=data,
                raw=line
            )
            entries.append(entry)
        
        if entries:
            await self.log_repo.save_logs(entries)
    
    async def search_logs(
        self,
        filter: LogFilter,
        limit: int = 100,
        offset: int = 0
    ) -> List[LogEntry]:
        """搜索日志"""
        return await self.log_repo.search_logs(filter, limit, offset)
    
    def _get_log_level(self, data: Dict) -> LogLevel:
        """获取日志级别"""
        status = data.get('status')
        if status:
            if status.startswith('5'):
                return LogLevel.ERROR
            elif status.startswith('4'):
                return LogLevel.WARNING
        return LogLevel.INFO 