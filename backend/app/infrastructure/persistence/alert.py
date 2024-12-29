from typing import List, Optional
from datetime import datetime
from sqlalchemy import select, and_
from .database import Database
from ...domain.alert.repository import AlertLevelRepository, NotificationChannelRepository
from ...domain.alert.aggregate import AlertLevel, NotificationChannel, NotificationType

class AlertLevelRepositoryImpl(AlertLevelRepository):
    def __init__(self, db: Database):
        self.db = db
    
    async def save(self, level: AlertLevel) -> None:
        query = """
            INSERT INTO alert_levels (id, name, description, color, priority, created_at, updated_at)
            VALUES ($1, $2, $3, $4, $5, $6, $7)
            ON CONFLICT (id) DO UPDATE
            SET name = $2, description = $3, color = $4, priority = $5, updated_at = $7
        """
        await self.db.execute(
            query,
            level.id,
            level.name,
            level.description,
            level.color,
            level.priority,
            level.created_at,
            level.updated_at
        )
    
    async def get_by_id(self, level_id: str) -> AlertLevel:
        query = "SELECT * FROM alert_levels WHERE id = $1"
        row = await self.db.fetch_one(query, level_id)
        if not row:
            return None
        return AlertLevel(**row)
    
    async def list_all(self) -> List[AlertLevel]:
        query = "SELECT * FROM alert_levels ORDER BY priority"
        rows = await self.db.fetch_all(query)
        return [AlertLevel(**row) for row in rows]
    
    async def delete(self, level_id: str) -> None:
        query = "DELETE FROM alert_levels WHERE id = $1"
        await self.db.execute(query, level_id)

class NotificationChannelRepositoryImpl(NotificationChannelRepository):
    def __init__(self, db: Database):
        self.db = db
    
    async def save(self, channel: NotificationChannel) -> None:
        query = """
            INSERT INTO notification_channels (
                id, name, type, config, enabled,
                created_at, updated_at
            ) VALUES ($1, $2, $3, $4, $5, $6, $7)
            ON CONFLICT (id) DO UPDATE SET
                name = $2,
                type = $3,
                config = $4,
                enabled = $5,
                updated_at = $7
        """
        await self.db.execute(
            query,
            channel.id,
            channel.name,
            channel.type.value,
            channel.config,
            channel.enabled,
            channel.created_at,
            channel.updated_at
        )
    
    async def get_by_id(self, channel_id: str) -> Optional[NotificationChannel]:
        query = "SELECT * FROM notification_channels WHERE id = $1"
        row = await self.db.fetch_one(query, channel_id)
        if not row:
            return None
        return NotificationChannel(
            **{
                **row,
                "type": NotificationType(row["type"])
            }
        )
    
    async def list_all(self) -> List[NotificationChannel]:
        query = "SELECT * FROM notification_channels"
        rows = await self.db.fetch_all(query)
        return [
            NotificationChannel(
                **{
                    **row,
                    "type": NotificationType(row["type"])
                }
            )
            for row in rows
        ]
    
    async def delete(self, channel_id: str) -> None:
        query = "DELETE FROM notification_channels WHERE id = $1"
        await self.db.execute(query, channel_id)
    
    async def get_channels_by_level(self, level_id: str) -> List[NotificationChannel]:
        query = """
            SELECT c.* FROM notification_channels c
            JOIN alert_level_channels lc ON c.id = lc.channel_id
            WHERE lc.level_id = $1 AND c.enabled = true
        """
        rows = await self.db.fetch_all(query, level_id)
        return [
            NotificationChannel(
                **{
                    **row,
                    "type": NotificationType(row["type"])
                }
            )
            for row in rows
        ] 