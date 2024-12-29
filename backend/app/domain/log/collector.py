from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional
import re

class CollectorType(str, Enum):
    FILE = "file"
    SYSLOG = "syslog"
    JOURNALD = "journald"

@dataclass
class LogCollector:
    id: str
    name: str
    type: CollectorType
    config: Dict
    enabled: bool
    created_at: datetime
    updated_at: datetime

@dataclass
class LogParser:
    id: str
    name: str
    pattern: str
    fields: Dict[str, str]
    sample: Optional[str]
    enabled: bool
    created_at: datetime
    updated_at: datetime
    
    def parse(self, line: str) -> Optional[Dict]:
        """解析日志行"""
        try:
            match = re.match(self.pattern, line)
            if not match:
                return None
            
            result = {}
            for field, group in self.fields.items():
                try:
                    result[field] = match.group(group)
                except IndexError:
                    continue
            
            return result
        except Exception:
            return None

@dataclass
class CollectorParser:
    collector_id: str
    parser_id: str
    created_at: datetime 