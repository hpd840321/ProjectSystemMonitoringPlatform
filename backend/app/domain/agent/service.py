from datetime import datetime, timedelta
from typing import Dict, List, Optional
from uuid import uuid4
from .repository import AgentRepository, AgentMetricsRepository
from .aggregate import Agent, AgentMetrics, AgentStatus, AgentVersion

class AgentService:
    """Agent服务"""
    
    def __init__(
        self,
        agent_repo: AgentRepository,
        metrics_repo: AgentMetricsRepository
    ):
        self.agent_repo = agent_repo
        self.metrics_repo = metrics_repo
    
    async def register_agent(
        self,
        server_id: str,
        hostname: str,
        ip_address: str,
        system_info: Dict,
        version: str = AgentVersion.V1_0
    ) -> Agent:
        """注册Agent"""
        now = datetime.now()
        agent = Agent(
            id=str(uuid4()),
            server_id=server_id,
            version=AgentVersion(version),
            status=AgentStatus.ONLINE,
            hostname=hostname,
            ip_address=ip_address,
            system_info=system_info,
            config={},
            last_heartbeat=now,
            created_at=now,
            updated_at=now
        )
        await self.agent_repo.save(agent)
        return agent
    
    async def update_heartbeat(
        self,
        agent_id: str,
        metrics: Optional[Dict] = None
    ) -> None:
        """更新Agent心跳"""
        now = datetime.now()
        await self.agent_repo.update_status(
            agent_id,
            AgentStatus.ONLINE,
            now
        )
        
        if metrics:
            agent_metrics = AgentMetrics(
                agent_id=agent_id,
                cpu_usage=metrics.get('cpu', 0),
                memory_usage=metrics.get('memory', 0),
                disk_usage=metrics.get('disk', {}),
                network_io=metrics.get('network', {}),
                timestamp=now
            )
            await self.metrics_repo.save_metrics(agent_metrics)
    
    async def check_agent_status(self) -> None:
        """检查Agent状态"""
        threshold = datetime.now() - timedelta(minutes=5)
        agents = await self.agent_repo.list_offline_agents(threshold)
        
        for agent in agents:
            await self.agent_repo.update_status(
                agent.id,
                AgentStatus.OFFLINE,
                agent.last_heartbeat
            ) 