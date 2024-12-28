import logging
from datetime import datetime, timedelta
from typing import List
from app.domain.agent.service import AgentService
from app.domain.agent.aggregate import AgentStatus
from app.infrastructure.config import settings

logger = logging.getLogger(__name__)

class AgentTasks:
    """Agent相关后台任务"""
    
    def __init__(self, agent_service: AgentService):
        self.agent_service = agent_service
    
    async def check_agent_status(self):
        """检查Agent状态任务"""
        try:
            logger.info("开始检查Agent状态")
            await self.agent_service.check_agent_status()
            logger.info("Agent状态检查完成")
        except Exception as e:
            logger.error(f"Agent状态检查失败: {str(e)}", exc_info=True)
    
    async def cleanup_old_metrics(self):
        """清理过期指标数据任务"""
        try:
            logger.info("开始清理过期指标数据")
            retention_days = settings.AGENT_METRICS_RETENTION_DAYS
            threshold = datetime.now() - timedelta(days=retention_days)
            await self.agent_service.cleanup_metrics(threshold)
            logger.info("过期指标数据清理完成")
        except Exception as e:
            logger.error(f"指标数据清理失败: {str(e)}", exc_info=True) 