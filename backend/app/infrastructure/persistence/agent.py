from typing import List, Optional
from datetime import datetime
from .database import Database
from ...domain.agent.repository import AgentRepository, AgentVersionRepository, UpgradeTaskRepository
from ...domain.agent.aggregate import Agent, AgentVersion, UpgradeTask, AgentStatus, UpgradeTaskStatus

class AgentRepositoryImpl(AgentRepository):
    def __init__(self, db: Database):
        self.db = db
    
    async def save(self, agent: Agent) -> None:
        query = """
            INSERT INTO agents (
                id, server_id, version, status, last_heartbeat,
                config, created_at, updated_at
            ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
            ON CONFLICT (id) DO UPDATE SET
                version = $3,
                status = $4,
                last_heartbeat = $5,
                config = $6,
                updated_at = $8
        """
        await self.db.execute(
            query,
            agent.id,
            agent.server_id,
            agent.version,
            agent.status.value,
            agent.last_heartbeat,
            agent.config,
            agent.created_at,
            agent.updated_at
        )
    
    async def get_by_id(self, agent_id: str) -> Optional[Agent]:
        query = "SELECT * FROM agents WHERE id = $1"
        row = await self.db.fetch_one(query, agent_id)
        if not row:
            return None
        return Agent(
            **{
                **row,
                "status": AgentStatus(row["status"])
            }
        )
    
    async def get_by_server(self, server_id: str) -> Optional[Agent]:
        query = "SELECT * FROM agents WHERE server_id = $1"
        row = await self.db.fetch_one(query, server_id)
        if not row:
            return None
        return Agent(
            **{
                **row,
                "status": AgentStatus(row["status"])
            }
        )
    
    async def list_by_status(self, status: str) -> List[Agent]:
        query = "SELECT * FROM agents WHERE status = $1"
        rows = await self.db.fetch_all(query, status)
        return [
            Agent(
                **{
                    **row,
                    "status": AgentStatus(row["status"])
                }
            )
            for row in rows
        ]

class AgentVersionRepositoryImpl(AgentVersionRepository):
    def __init__(self, db: Database):
        self.db = db
    
    async def save(self, version: AgentVersion) -> None:
        # 如果是最新版本,先将其他版本设置为非最新
        if version.is_latest:
            await self.db.execute(
                "UPDATE agent_versions SET is_latest = false"
            )
        
        query = """
            INSERT INTO agent_versions (
                id, version, file_path, checksum,
                description, is_latest, created_at, updated_at
            ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
            ON CONFLICT (version) DO UPDATE SET
                file_path = $3,
                checksum = $4,
                description = $5,
                is_latest = $6,
                updated_at = $8
        """
        await self.db.execute(
            query,
            version.id,
            version.version,
            version.file_path,
            version.checksum,
            version.description,
            version.is_latest,
            version.created_at,
            version.updated_at
        )
    
    async def get_by_version(self, version: str) -> Optional[AgentVersion]:
        query = "SELECT * FROM agent_versions WHERE version = $1"
        row = await self.db.fetch_one(query, version)
        if not row:
            return None
        return AgentVersion(**row)
    
    async def get_latest(self) -> Optional[AgentVersion]:
        query = "SELECT * FROM agent_versions WHERE is_latest = true"
        row = await self.db.fetch_one(query)
        if not row:
            return None
        return AgentVersion(**row)
    
    async def list_all(self) -> List[AgentVersion]:
        query = "SELECT * FROM agent_versions ORDER BY version DESC"
        rows = await self.db.fetch_all(query)
        return [AgentVersion(**row) for row in rows]

class UpgradeTaskRepositoryImpl(UpgradeTaskRepository):
    def __init__(self, db: Database):
        self.db = db
    
    async def save(self, task: UpgradeTask) -> None:
        query = """
            INSERT INTO agent_upgrade_tasks (
                id, agent_id, from_version, to_version,
                status, error, created_at, updated_at
            ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
            ON CONFLICT (id) DO UPDATE SET
                status = $5,
                error = $6,
                updated_at = $8
        """
        await self.db.execute(
            query,
            task.id,
            task.agent_id,
            task.from_version,
            task.to_version,
            task.status.value,
            task.error,
            task.created_at,
            task.updated_at
        )
    
    async def get_by_id(self, task_id: str) -> Optional[UpgradeTask]:
        query = "SELECT * FROM agent_upgrade_tasks WHERE id = $1"
        row = await self.db.fetch_one(query, task_id)
        if not row:
            return None
        return UpgradeTask(
            **{
                **row,
                "status": UpgradeTaskStatus(row["status"])
            }
        )
    
    async def list_by_agent(self, agent_id: str) -> List[UpgradeTask]:
        query = "SELECT * FROM agent_upgrade_tasks WHERE agent_id = $1 ORDER BY created_at DESC"
        rows = await self.db.fetch_all(query, agent_id)
        return [
            UpgradeTask(
                **{
                    **row,
                    "status": UpgradeTaskStatus(row["status"])
                }
            )
            for row in rows
        ] 