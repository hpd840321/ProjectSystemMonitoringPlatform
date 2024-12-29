from typing import List, Optional, Dict, Any
from sqlalchemy import select
from .database import Database
from ...domain.settings.repository import SettingRepository
from ...domain.settings.aggregate import Setting, SettingType

class SettingRepositoryImpl(SettingRepository):
    def __init__(self, db: Database):
        self.db = db
    
    async def save(self, setting: Setting) -> None:
        query = """
            INSERT INTO settings (
                id, type, key, value, description,
                created_at, updated_at
            ) VALUES ($1, $2, $3, $4, $5, $6, $7)
            ON CONFLICT (key) DO UPDATE SET
                value = $4,
                description = $5,
                updated_at = $7
        """
        await self.db.execute(
            query,
            setting.id,
            setting.type.value,
            setting.key,
            setting.value,
            setting.description,
            setting.created_at,
            setting.updated_at
        )
    
    async def get_by_key(self, key: str) -> Optional[Setting]:
        query = "SELECT * FROM settings WHERE key = $1"
        row = await self.db.fetch_one(query, key)
        if not row:
            return None
        return Setting(
            **{
                **row,
                "type": SettingType(row["type"]),
                "value": row["value"]
            }
        )
    
    async def list_by_type(self, type: SettingType) -> List[Setting]:
        query = "SELECT * FROM settings WHERE type = $1"
        rows = await self.db.fetch_all(query, type.value)
        return [
            Setting(
                **{
                    **row,
                    "type": SettingType(row["type"]),
                    "value": row["value"]
                }
            )
            for row in rows
        ]
    
    async def get_all_settings(self) -> Dict[str, Any]:
        query = "SELECT key, value FROM settings"
        rows = await self.db.fetch_all(query)
        return {
            row["key"]: row["value"]
            for row in rows
        }
    
    async def update_settings(self, settings: Dict[str, Any]) -> None:
        """批量更新设置"""
        for key, value in settings.items():
            setting = await self.get_by_key(key)
            if setting:
                await self.save(Setting(
                    id=setting.id,
                    type=setting.type,
                    key=key,
                    value=value,
                    description=setting.description,
                    created_at=setting.created_at,
                    updated_at=datetime.now()
                )) 