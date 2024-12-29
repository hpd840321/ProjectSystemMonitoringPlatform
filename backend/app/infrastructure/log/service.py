import asyncio
from typing import List
from datetime import datetime
from sqlalchemy.orm import Session

from app.crud import log_source, log_parse_rule, log
from app.models.log import LogSource, LogParseRule
from app.interface.api.v1.schemas.log import LogEntry
from .collectors import CollectorFactory
from .parsers import LogParserChain

class LogService:
    """日志服务"""
    
    def __init__(self, db: Session):
        self.db = db
        self.collectors = {}
        self.parser_chains = {}
        
    async def start(self):
        """启动日志采集"""
        # 加载所有启用的日志源
        sources = log_source.get_multi(self.db)
        enabled_sources = [s for s in sources if s.enabled]
        
        # 为每个日志源创建采集器和解析器
        for source in enabled_sources:
            collector = CollectorFactory.create(source)
            parser_chain = LogParserChain(source.parse_rules)
            
            self.collectors[source.id] = collector
            self.parser_chains[source.id] = parser_chain
            
            # 启动采集任务
            asyncio.create_task(self._collect_and_parse(source.id))
            
    async def _collect_and_parse(self, source_id: int):
        """采集和解析日志"""
        collector = self.collectors[source_id]
        parser_chain = self.parser_chains[source_id]
        
        async for entry in collector.collect():
            # 解析日志
            parsed_entry = parser_chain.parse(entry)
            
            # 保存到数据库
            await log.create(self.db, obj_in=parsed_entry)
            
    def add_source(self, source: LogSource):
        """添加新的日志源"""
        if source.id in self.collectors:
            return
            
        collector = CollectorFactory.create(source)
        parser_chain = LogParserChain(source.parse_rules)
        
        self.collectors[source.id] = collector
        self.parser_chains[source.id] = parser_chain
        
        asyncio.create_task(self._collect_and_parse(source.id))
        
    def remove_source(self, source_id: int):
        """移除日志源"""
        self.collectors.pop(source_id, None)
        self.parser_chains.pop(source_id, None) 