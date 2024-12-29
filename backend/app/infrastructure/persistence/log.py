from typing import List, Optional
from datetime import datetime
from .database import Database
from ...domain.log.repository import LogParseRuleRepository, LogCollectConfigRepository
from ...domain.log.aggregate import LogParseRule, LogCollectConfig

class LogParseRuleRepositoryImpl(LogParseRuleRepository):
    def __init__(self, db: Database):
        self.db = db
    
    async def save(self, rule: LogParseRule) -> None:
        query = """
            INSERT INTO log_parse_rules (
                id, name, pattern, fields, description,
                created_at, updated_at
            ) VALUES ($1, $2, $3, $4, $5, $6, $7)
            ON CONFLICT (id) DO UPDATE SET
                name = $2,
                pattern = $3,
                fields = $4,
                description = $5,
                updated_at = $7
        """
        await self.db.execute(
            query,
            rule.id,
            rule.name,
            rule.pattern,
            rule.fields,
            rule.description,
            rule.created_at,
            rule.updated_at
        )
    
    async def get_by_id(self, rule_id: str) -> Optional[LogParseRule]:
        query = "SELECT * FROM log_parse_rules WHERE id = $1"
        row = await self.db.fetch_one(query, rule_id)
        if not row:
            return None
        return LogParseRule(**row)
    
    async def list_all(self) -> List[LogParseRule]:
        query = "SELECT * FROM log_parse_rules"
        rows = await self.db.fetch_all(query)
        return [LogParseRule(**row) for row in rows]
    
    async def delete(self, rule_id: str) -> None:
        query = "DELETE FROM log_parse_rules WHERE id = $1"
        await self.db.execute(query, rule_id)

class LogCollectConfigRepositoryImpl(LogCollectConfigRepository):
    def __init__(self, db: Database):
        self.db = db
    
    async def save(self, config: LogCollectConfig) -> None:
        query = """
            INSERT INTO log_collect_configs (
                id, server_id, name, path, rule_id,
                enabled, created_at, updated_at
            ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
            ON CONFLICT (id) DO UPDATE SET
                server_id = $2,
                name = $3,
                path = $4,
                rule_id = $5,
                enabled = $6,
                updated_at = $8
        """
        await self.db.execute(
            query,
            config.id,
            config.server_id,
            config.name,
            config.path,
            config.rule_id,
            config.enabled,
            config.created_at,
            config.updated_at
        )
    
    async def get_by_id(self, config_id: str) -> Optional[LogCollectConfig]:
        query = "SELECT * FROM log_collect_configs WHERE id = $1"
        row = await self.db.fetch_one(query, config_id)
        if not row:
            return None
        return LogCollectConfig(**row)
    
    async def list_by_server(self, server_id: str) -> List[LogCollectConfig]:
        query = "SELECT * FROM log_collect_configs WHERE server_id = $1"
        rows = await self.db.fetch_all(query, server_id)
        return [LogCollectConfig(**row) for row in rows]
    
    async def delete(self, config_id: str) -> None:
        query = "DELETE FROM log_collect_configs WHERE id = $1"
        await self.db.execute(query, config_id) 