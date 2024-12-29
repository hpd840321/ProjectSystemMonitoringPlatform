import logging
from datetime import datetime, timedelta
from typing import List
from app.domain.agent.service import AgentService
from app.domain.agent.aggregate import AgentStatus
from app.infrastructure.config import settings
import asyncio

logger = logging.getLogger(__name__)

class AgentStatusChecker:
    def __init__(self, service: AgentService):
        self.service = service
    
    async def check_agent_status(self):
        """检查Agent状态"""
        try:
            # 获取所有在线Agent
            agents = await self.service.agent_repo.list_by_status(AgentStatus.ONLINE)
            
            # 检查心跳时间
            threshold = datetime.now() - timedelta(seconds=settings.AGENT_OFFLINE_THRESHOLD)
            for agent in agents:
                if agent.last_heartbeat < threshold:
                    # 更新为离线状态
                    agent.status = AgentStatus.OFFLINE
                    agent.updated_at = datetime.now()
                    await self.service.agent_repo.save(agent)
                    logger.warning(f"Agent {agent.id} is offline")
        except Exception as e:
            logger.error(f"Failed to check agent status: {str(e)}")
    
    async def run(self):
        """运行状态检查"""
        while True:
            await self.check_agent_status()
            await asyncio.sleep(settings.AGENT_CHECK_INTERVAL) 