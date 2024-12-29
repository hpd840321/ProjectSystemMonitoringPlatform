import os
import re
import json
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Generator
from datetime import datetime
import asyncio
import aiofiles
import asyncssh
from systemd import journal

from app.models.log import LogSource, LogParseRule
from app.interface.api.v1.schemas.log import LogEntry

class LogCollector(ABC):
    """日志采集器基类"""
    
    def __init__(self, source: LogSource):
        self.source = source
        self.config = source.config
        
    @abstractmethod
    async def collect(self) -> Generator[LogEntry, None, None]:
        """采集日志"""
        pass

class FileLogCollector(LogCollector):
    """文件日志采集器"""
    
    async def collect(self) -> Generator[LogEntry, None, None]:
        path = self.config["path"]
        if not os.path.exists(path):
            return
            
        async with aiofiles.open(path, mode='r') as f:
            # 从文件末尾开始读取
            await f.seek(0, 2)
            while True:
                line = await f.readline()
                if not line:
                    await asyncio.sleep(1)
                    continue
                    
                yield LogEntry(
                    source_id=self.source.id,
                    timestamp=datetime.now(),
                    message=line.strip(),
                    level=None,  # 需要通过解析规则提取
                    parsed_fields=None,  # 需要通过解析规则提取
                    metadata={"path": path}
                )

class SyslogCollector(LogCollector):
    """Syslog采集器"""
    
    async def collect(self) -> Generator[LogEntry, None, None]:
        port = self.config["port"]
        protocol = self.config["protocol"]
        
        # 实现syslog服务器监听
        server = await asyncio.start_server(
            self._handle_connection, '0.0.0.0', port
        )
        
        async with server:
            await server.serve_forever()
    
    async def _handle_connection(
        self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter
    ):
        while True:
            data = await reader.readline()
            if not data:
                break
                
            message = data.decode().strip()
            yield LogEntry(
                source_id=self.source.id,
                timestamp=datetime.now(),
                message=message,
                level=None,
                parsed_fields=None,
                metadata={"protocol": self.config["protocol"]}
            )

class JournaldCollector(LogCollector):
    """Systemd Journal采集器"""
    
    async def collect(self) -> Generator[LogEntry, None, None]:
        unit = self.config["unit"]
        j = journal.Reader()
        j.add_match(_SYSTEMD_UNIT=unit)
        
        # 从最新的日志开始读取
        j.seek_tail()
        j.get_previous()
        
        while True:
            entry = j.get_next()
            if not entry:
                await asyncio.sleep(1)
                continue
                
            yield LogEntry(
                source_id=self.source.id,
                timestamp=datetime.fromtimestamp(entry["__REALTIME_TIMESTAMP"].timestamp()),
                message=entry.get("MESSAGE", ""),
                level=entry.get("PRIORITY"),
                parsed_fields=None,
                metadata={"unit": unit}
            )

class CollectorFactory:
    """日志采集器工厂"""
    
    @staticmethod
    def create(source: LogSource) -> LogCollector:
        collectors = {
            "file": FileLogCollector,
            "syslog": SyslogCollector,
            "journald": JournaldCollector
        }
        collector_class = collectors.get(source.type)
        if not collector_class:
            raise ValueError(f"Unsupported log source type: {source.type}")
        return collector_class(source) 