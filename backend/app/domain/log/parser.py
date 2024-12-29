import re
from datetime import datetime
from typing import Dict, Optional
from .aggregate import LogFormat, LogLevel, LogEntry

class LogParser:
    """日志解析器"""
    
    def __init__(self, config):
        self.config = config
        self.format = LogFormat(config.format)
        self.pattern = config.pattern
        self.fields = config.fields
        
        if self.format == LogFormat.CUSTOM and not self.pattern:
            raise ValueError("Custom format requires pattern")
    
    def parse(self, line: str) -> Optional[Dict]:
        """解析日志行"""
        if self.format == LogFormat.SYSLOG:
            return self._parse_syslog(line)
        elif self.format == LogFormat.JSON:
            return self._parse_json(line)
        elif self.format == LogFormat.NGINX:
            return self._parse_nginx(line)
        elif self.format == LogFormat.APACHE:
            return self._parse_apache(line)
        elif self.format == LogFormat.CUSTOM:
            return self._parse_custom(line)
        return None
    
    def _parse_syslog(self, line: str) -> Optional[Dict]:
        # 标准syslog格式解析
        pattern = r"^(\w{3}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2})\s+(\w+)\s+([^:]+):\s+(.*)$"
        match = re.match(pattern, line)
        if not match:
            return None
        
        timestamp, host, program, message = match.groups()
        return {
            "timestamp": self._parse_syslog_timestamp(timestamp),
            "host": host,
            "program": program,
            "message": message,
            "level": self._guess_level(message)
        }
    
    def _parse_json(self, line: str) -> Optional[Dict]:
        try:
            data = json.loads(line)
            return {
                "timestamp": self._parse_timestamp(data.get("timestamp", "")),
                "level": data.get("level", "info").lower(),
                "message": data.get("message", ""),
                **{k: v for k, v in data.items() if k not in ["timestamp", "level", "message"]}
            }
        except json.JSONDecodeError:
            return None
    
    def _parse_nginx(self, line: str) -> Optional[Dict]:
        # nginx访问日志格式解析
        pattern = r'(?P<remote_addr>[\d\.]+)\s+-\s+(?P<remote_user>[^\s]*)\s+\[(?P<time_local>[\w:/]+\s[+\-]\d{4})\]\s+"(?P<request>[^"]*?)"\s+(?P<status>\d{3})\s+(?P<body_bytes_sent>\d+)\s+"(?P<http_referer>[^"]*?)"\s+"(?P<http_user_agent>[^"]*?)"'
        match = re.match(pattern, line)
        if not match:
            return None
        
        data = match.groupdict()
        data["timestamp"] = self._parse_nginx_timestamp(data["time_local"])
        data["level"] = "info"
        return data
    
    def _parse_custom(self, line: str) -> Optional[Dict]:
        match = re.match(self.pattern, line)
        if not match:
            return None
        
        data = match.groupdict()
        # 应用字段映射
        return {
            self.fields.get(k, k): v
            for k, v in data.items()
        }
    
    def _guess_level(self, message: str) -> str:
        """根据消息内容猜测日志级别"""
        message = message.lower()
        if any(x in message for x in ["error", "fail", "exception"]):
            return "error"
        elif any(x in message for x in ["warn", "warning"]):
            return "warning"
        elif any(x in message for x in ["debug"]):
            return "debug"
        return "info"
    
    def _parse_timestamp(self, ts_str: str) -> datetime:
        """解析时间戳"""
        # 实现各种时间格式的解析
        pass 