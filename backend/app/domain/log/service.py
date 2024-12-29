from datetime import datetime
from typing import List, Dict, Optional
from uuid import uuid4
from .repository import LogParseRuleRepository, LogCollectConfigRepository
from .aggregate import LogParseRule, LogCollectConfig

class LogService:
    def __init__(
        self,
        rule_repo: LogParseRuleRepository,
        config_repo: LogCollectConfigRepository
    ):
        self.rule_repo = rule_repo
        self.config_repo = config_repo
    
    async def create_parse_rule(
        self,
        name: str,
        pattern: str,
        fields: Dict[str, str],
        description: Optional[str] = None
    ) -> LogParseRule:
        """创建日志解析规则"""
        now = datetime.now()
        rule = LogParseRule(
            id=str(uuid4()),
            name=name,
            pattern=pattern,
            fields=fields,
            description=description,
            created_at=now,
            updated_at=now
        )
        await self.rule_repo.save(rule)
        return rule
    
    async def create_collect_config(
        self,
        server_id: str,
        name: str,
        path: str,
        rule_id: str,
        enabled: bool = True
    ) -> LogCollectConfig:
        """创建日志采集配置"""
        now = datetime.now()
        config = LogCollectConfig(
            id=str(uuid4()),
            server_id=server_id,
            name=name,
            path=path,
            rule_id=rule_id,
            enabled=enabled,
            created_at=now,
            updated_at=now
        )
        await self.config_repo.save(config)
        return config
    
    async def parse_log(self, rule_id: str, content: str) -> Optional[Dict]:
        """解析日志内容"""
        rule = await self.rule_repo.get_by_id(rule_id)
        if not rule:
            return None
            
        # 使用正则表达式解析
        import re
        match = re.match(rule.pattern, content)
        if not match:
            return None
            
        # 转换字段类型
        result = {}
        for name, value in match.groupdict().items():
            field_type = rule.fields.get(name)
            if field_type == "integer":
                result[name] = int(value)
            elif field_type == "float":
                result[name] = float(value)
            elif field_type == "datetime":
                # 根据实际日志格式调整解析方式
                result[name] = datetime.strptime(value, "%d/%b/%Y:%H:%M:%S %z")
            else:
                result[name] = value
        return result 