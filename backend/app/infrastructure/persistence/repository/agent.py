from datetime import datetime
from typing import List, Optional
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.agent.repository import AgentRepository, AgentMetricsRepository
from app.domain.agent.aggregate import Agent, AgentMetrics, AgentStatus, AgentVersion
from ..models.agent import AgentModel, AgentMetricsModel

class SQLAlchemyAgentRepository(AgentRepository):
    """Agent SQLAlchemy仓储实现"""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def save(self, agent: Agent) -> None:
        """保存Agent"""
        model = AgentModel(
            id=agent.id,
            server_id=agent.server_id,
            version=agent.version.value,
            status=agent.status.value,
            hostname=agent.hostname,
            ip_address=agent.ip_address,
            system_info=agent.system_info,
            config=agent.config,
            last_heartbeat=agent.last_heartbeat,
            created_at=agent.created_at,
            updated_at=agent.updated_at
        )
        self.session.add(model)
        await self.session.commit()
    
    async def get_by_id(self, agent_id: str) -> Optional[Agent]:
        """获取Agent"""
        result = await self.session.execute(
            select(AgentModel).where(AgentModel.id == agent_id)
        )
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None
    
    async def list_by_server(self, server_id: str) -> List[Agent]:
        """获取服务器的Agent列表"""
        result = await self.session.execute(
            select(AgentModel).where(AgentModel.server_id == server_id)
        )
        return [self._to_entity(model) for model in result.scalars()]
    
    async def update_status(
        self,
        agent_id: str,
        status: str,
        heartbeat: datetime
    ) -> None:
        """更新Agent状态"""
        await self.session.execute(
            update(AgentModel)
            .where(AgentModel.id == agent_id)
            .values(
                status=status,
                last_heartbeat=heartbeat,
                updated_at=datetime.now()
            )
        )
        await self.session.commit()
    
    async def list_offline_agents(self, threshold: datetime) -> List[Agent]:
        """获取离线Agent列表"""
        result = await self.session.execute(
            select(AgentModel).where(
                AgentModel.last_heartbeat < threshold,
                AgentModel.status == AgentStatus.ONLINE.value
            )
        )
        return [self._to_entity(model) for model in result.scalars()]
    
    def _to_entity(self, model: AgentModel) -> Agent:
        """转换为实体"""
        return Agent(
            id=model.id,
            server_id=model.server_id,
            version=AgentVersion(model.version),
            status=AgentStatus(model.status),
            hostname=model.hostname,
            ip_address=model.ip_address,
            system_info=model.system_info,
            config=model.config,
            last_heartbeat=model.last_heartbeat,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

class SQLAlchemyAgentMetricsRepository(AgentMetricsRepository):
    """Agent指标SQLAlchemy仓储实现"""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def save_metrics(self, metrics: AgentMetrics) -> None:
        """保存Agent指标"""
        model = AgentMetricsModel(
            agent_id=metrics.agent_id,
            cpu_usage=metrics.cpu_usage,
            memory_usage=metrics.memory_usage,
            disk_usage=metrics.disk_usage,
            network_io=metrics.network_io,
            timestamp=metrics.timestamp
        )
        self.session.add(model)
        await self.session.commit()
    
    async def get_latest_metrics(self, agent_id: str) -> Optional[AgentMetrics]:
        """获取最新指标"""
        result = await self.session.execute(
            select(AgentMetricsModel)
            .where(AgentMetricsModel.agent_id == agent_id)
            .order_by(AgentMetricsModel.timestamp.desc())
            .limit(1)
        )
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None
    
    def _to_entity(self, model: AgentMetricsModel) -> AgentMetrics:
        """转换为实体"""
        return AgentMetrics(
            agent_id=model.agent_id,
            cpu_usage=model.cpu_usage,
            memory_usage=model.memory_usage,
            disk_usage=model.disk_usage,
            network_io=model.network_io,
            timestamp=model.timestamp
        ) 