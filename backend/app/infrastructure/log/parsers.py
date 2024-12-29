import re
from typing import Dict, Any, Optional
from datetime import datetime

from app.models.log import LogParseRule
from app.interface.api.v1.schemas.log import LogEntry

class LogParser:
    """日志解析器"""
    
    def __init__(self, rule: LogParseRule):
        self.rule = rule
        self.pattern = re.compile(rule.pattern)
        
    def parse(self, entry: LogEntry) -> LogEntry:
        """解析日志"""
        match = self.pattern.match(entry.message)
        if not match:
            return entry
            
        parsed_fields = {}
        for field_name, group_name in self.rule.fields.items():
            try:
                value = match.group(group_name)
                parsed_fields[field_name] = value
                
                # 特殊字段处理
                if field_name == "level":
                    entry.level = value
                elif field_name == "timestamp":
                    try:
                        entry.timestamp = datetime.strptime(
                            value, self.rule.fields.get("timestamp_format", "%Y-%m-%d %H:%M:%S")
                        )
                    except ValueError:
                        pass
                        
            except IndexError:
                continue
                
        entry.parsed_fields = parsed_fields
        return entry

class LogParserChain:
    """日志解析器链"""
    
    def __init__(self, rules: list[LogParseRule]):
        self.parsers = [
            LogParser(rule) for rule in sorted(rules, key=lambda r: r.priority)
        ]
        
    def parse(self, entry: LogEntry) -> LogEntry:
        """按优先级依次尝试解析"""
        for parser in self.parsers:
            result = parser.parse(entry)
            if result.parsed_fields:
                return result
        return entry 