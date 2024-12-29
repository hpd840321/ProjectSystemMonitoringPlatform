from datetime import datetime
from typing import Dict, Optional
from uuid import uuid4
from .collector import LogParser
from .repository import LogRepository

class LogParserService:
    def __init__(self, log_repo: LogRepository):
        self.log_repo = log_repo
    
    async def create_parser(
        self,
        name: str,
        pattern: str,
        fields: Dict[str, str],
        sample: Optional[str] = None
    ) -> LogParser:
        """创建日志解析器"""
        now = datetime.now()
        parser = LogParser(
            id=str(uuid4()),
            name=name,
            pattern=pattern,
            fields=fields,
            sample=sample,
            enabled=True,
            created_at=now,
            updated_at=now
        )
        
        # 验证解析器
        if sample and not parser.parse(sample):
            raise ValueError("Invalid parser pattern")
        
        await self.log_repo.save_parser(parser)
        return parser
    
    async def test_parser(
        self,
        pattern: str,
        fields: Dict[str, str],
        sample: str
    ) -> Optional[Dict]:
        """测试解析器"""
        parser = LogParser(
            id="test",
            name="test",
            pattern=pattern,
            fields=fields,
            sample=sample,
            enabled=True,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        return parser.parse(sample) 