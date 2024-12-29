from datetime import datetime
from typing import List, Dict, Optional
import asyncio
import aiofiles
from pathlib import Path
from .collector import LogCollector, LogParser, CollectorType
from .repository import LogRepository

class LogCollectorService:
    def __init__(self, log_repo: LogRepository):
        self.log_repo = log_repo
        self._collectors: Dict[str, asyncio.Task] = {}
    
    async def start_collector(self, collector: LogCollector) -> None:
        """启动日志采集器"""
        if not collector.enabled:
            return
            
        if collector.id in self._collectors:
            return
        
        task = asyncio.create_task(self._collect_logs(collector))
        self._collectors[collector.id] = task
    
    async def stop_collector(self, collector_id: str) -> None:
        """停止日志采集器"""
        task = self._collectors.get(collector_id)
        if task:
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass
            del self._collectors[collector_id]
    
    async def _collect_logs(self, collector: LogCollector) -> None:
        """采集日志"""
        try:
            if collector.type == CollectorType.FILE:
                await self._collect_file_logs(collector)
            elif collector.type == CollectorType.SYSLOG:
                await self._collect_syslog(collector)
            elif collector.type == CollectorType.JOURNALD:
                await self._collect_journald(collector)
        except asyncio.CancelledError:
            raise
        except Exception as e:
            # TODO: 记录错误日志
            print(f"Collector error: {e}")
    
    async def _collect_file_logs(self, collector: LogCollector) -> None:
        """采集文件日志"""
        config = collector.config
        path = Path(config['path'])
        if not path.exists():
            return
        
        # 获取解析器
        parsers = await self.log_repo.get_collector_parsers(collector.id)
        
        # 读取文件
        async with aiofiles.open(path, mode='r') as f:
            # 移动到文件末尾
            await f.seek(0, 2)
            
            while True:
                line = await f.readline()
                if not line:
                    await asyncio.sleep(1)
                    continue
                
                # 解析日志
                log_entry = None
                for parser in parsers:
                    if not parser.enabled:
                        continue
                    
                    log_entry = parser.parse(line)
                    if log_entry:
                        break
                
                if log_entry:
                    # 保存解析结果
                    await self.log_repo.save_log(
                        collector_id=collector.id,
                        content=line,
                        parsed=log_entry,
                        timestamp=datetime.now()
                    )
    
    async def _collect_syslog(self, collector: LogCollector) -> None:
        """采集系统日志"""
        # TODO: 实现系统日志采集
        raise NotImplementedError()
    
    async def _collect_journald(self, collector: LogCollector) -> None:
        """采集journald日志"""
        # TODO: 实现journald日志采集
        raise NotImplementedError() 