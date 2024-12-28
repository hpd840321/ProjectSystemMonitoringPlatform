from typing import List, Dict, Optional
from datetime import datetime
from .dto import AgentDTO, AgentRegisterDTO, AgentMetricsDTO
from app.domain.agent.service import AgentService
from app.domain.agent.aggregate import AgentStatus

class AgentApplicationService:
    """Agent应用服务"""
    
    def __init__(self, agent_service: AgentService):
        self.agent_service = agent_service
    
    async def register_agent(self, dto: AgentRegisterDTO) -> AgentDTO:
        """注册Agent"""
        agent = await self.agent_service.register_agent(
            server_id=dto.server_id,
            hostname=dto.hostname,
            ip_address=dto.ip_address,
            system_info=dto.system_info,
            version=dto.version
        )
        return self._to_dto(agent)
    
    async def get_agent(self, agent_id: str) -> Optional[AgentDTO]:
        """获取Agent信息"""
        agent = await self.agent_service.get_agent(agent_id)
        return self._to_dto(agent) if agent else None
    
    async def list_server_agents(self, server_id: str) -> List[AgentDTO]:
        """获取服务器的Agent列表"""
        agents = await self.agent_service.list_by_server(server_id)
        return [self._to_dto(agent) for agent in agents]
    
    async def update_heartbeat(
        self,
        agent_id: str,
        metrics: Optional[Dict] = None
    ) -> None:
        """更新Agent心跳"""
        await self.agent_service.update_heartbeat(agent_id, metrics)
    
    def _to_dto(self, agent) -> AgentDTO:
        """转换为DTO"""
        return AgentDTO(
            id=agent.id,
            server_id=agent.server_id,
            version=agent.version.value,
            status=agent.status.value,
            hostname=agent.hostname,
            ip_address=agent.ip_address,
            system_info=agent.system_info,
            config=agent.config,
            last_heartbeat=agent.last_heartbeat,
            created_at=agent.created_at
        ) 