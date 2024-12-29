from typing import List, Optional
from app.domain.models.plugin import Plugin, PluginStatus
from app.domain.repositories.plugin_repository import IPluginRepository
from app.infrastructure.persistence.database import Database

class PostgresPluginRepository(IPluginRepository):
    def __init__(self, db: Database):
        self.db = db

    async def save(self, plugin: Plugin) -> str:
        query = """
            INSERT INTO agent_plugins 
            (name, version, description, entry_point, config_schema, status)
            VALUES ($1, $2, $3, $4, $5, $6)
            RETURNING id
        """
        plugin_id = await self.db.fetch_val(
            query,
            plugin.name,
            plugin.version,
            plugin.description,
            plugin.entry_point,
            plugin.config_schema,
            plugin.status.value
        )
        return plugin_id

    async def get_by_id(self, plugin_id: str) -> Optional[Plugin]:
        query = "SELECT * FROM agent_plugins WHERE id = $1"
        row = await self.db.fetch_one(query, plugin_id)
        return self._row_to_plugin(row) if row else None

    def _row_to_plugin(self, row) -> Plugin:
        return Plugin(
            id=row['id'],
            name=row['name'],
            version=row['version'],
            description=row['description'],
            entry_point=row['entry_point'],
            config_schema=row['config_schema'],
            status=PluginStatus(row['status']),
            created_at=row['created_at'],
            updated_at=row['updated_at']
        ) 