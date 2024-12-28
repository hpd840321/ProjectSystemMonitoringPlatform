import asyncio
from typing import List
from .base import BaseCollector

class LogCollector(BaseCollector):
    def __init__(self, config: dict):
        self.log_paths = config["log_paths"]
        self.patterns = config["patterns"]
        self.last_positions = {}

    async def collect(self) -> dict:
        """增量采集日志"""
        logs = []
        for path in self.log_paths:
            position = self.last_positions.get(path, 0)
            new_logs = await self._collect_file(path, position)
            logs.extend(new_logs)
        return {"logs": logs}

    async def _collect_file(self, path: str, position: int) -> List[dict]:
        """采集单个日志文件"""
        try:
            with open(path, 'r') as f:
                f.seek(position)
                new_logs = []
                for line in f:
                    if self._match_patterns(line):
                        new_logs.append(self._parse_log(line))
                self.last_positions[path] = f.tell()
                return new_logs
        except Exception as e:
            # 处理文件访问异常
            return [] 