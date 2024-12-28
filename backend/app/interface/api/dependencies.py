from fastapi import Depends
from app.infrastructure.persistence.database import get_session
from app.domain.agent.service import AgentService
from app.domain.agent.repository import AgentRepository, AgentMetricsRepository
from app.application.agent.service import AgentApplicationService
from app.infrastructure.persistence.repository.agent import (
    SQLAlchemyAgentRepository,
    SQLAlchemyAgentMetricsRepository
)

async def get_agent_service(
    session = Depends(get_session)
) -> AgentApplicationService:
    """获取Agent应用服务"""
    agent_repo = SQLAlchemyAgentRepository(session)
    metrics_repo = SQLAlchemyAgentMetricsRepository(session)
    agent_service = AgentService(agent_repo, metrics_repo)
    return AgentApplicationService(agent_service) 