import re
from typing import Dict, Optional
from datetime import datetime
from app.domain.log.aggregate import LogLevel, LogEntry

class LogParser:
    """日志解析器"""
    
    def __init__(self, pattern: str):
        self.pattern = re.compile(pattern)
    
    def parse(self, line: str) -> Optional[Dict]:
        """解析日志行"""
        match = self.pattern.match(line)
        if not match:
            return None
            
        return match.groupdict()

class NginxAccessLogParser(LogParser):
    """Nginx访问日志解析器"""
    
    def __init__(self):
        pattern = r'(?P<remote_addr>[\d\.]+) - (?P<remote_user>[^ ]*) \[(?P<time_local>.*?)\] "(?P<request>.*?)" (?P<status>\d+) (?P<body_bytes_sent>\d+) "(?P<http_referer>.*?)" "(?P<http_user_agent>.*?)"'
        super().__init__(pattern)
    
    def parse(self, line: str) -> Optional[Dict]:
        data = super().parse(line)
        if not data:
            return None
            
        # 解析请求
        request_parts = data['request'].split()
        if len(request_parts) >= 2:
            data['method'] = request_parts[0]
            data['path'] = request_parts[1]
            
        # 转换时间格式
        try:
            data['timestamp'] = datetime.strptime(
                data['time_local'],
                '%d/%b/%Y:%H:%M:%S %z'
            )
        except ValueError:
            return None
            
        return data 