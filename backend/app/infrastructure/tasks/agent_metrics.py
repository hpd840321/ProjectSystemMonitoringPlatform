import logging
from datetime import datetime, timedelta
import asyncio
from uuid import uuid4
from ...domain.agent.metrics import AgentMetricsHourly
from ...domain.agent.service import AgentService
from ...infrastructure.config import settings
from ...domain.agent.exceptions import MetricsAggregationError
from typing import List

logger = logging.getLogger(__name__)

class AgentMetricsAggregator:
    """Agent指标聚合器"""
    
    def __init__(self, service: AgentService):
        self.service = service
    
    async def aggregate_hourly_metrics(self):
        """聚合小时指标"""
        try:
            # 获取所有Agent
            agents = await self.service.agent_repo.list_all()
            now = datetime.now()
            hour_start = now.replace(minute=0, second=0, microsecond=0) - timedelta(hours=1)
            hour_end = hour_start + timedelta(hours=1)
            
            logger.info(f"Starting hourly metrics aggregation for {len(agents)} agents")
            
            for agent in agents:
                try:
                    # 获取原始指标
                    metrics = await self.service.metrics_repo.get_metrics(
                        agent_id=agent.id,
                        start_time=hour_start,
                        end_time=hour_end
                    )
                    
                    if not metrics:
                        logger.warning(f"No metrics found for agent {agent.id}")
                        continue
                    
                    # 计算聚合值
                    hourly = self._calculate_hourly_metrics(agent.id, hour_start, metrics)
                    await self.service.metrics_repo.save_hourly_metrics(hourly)
                    
                    logger.info(f"Aggregated hourly metrics for agent {agent.id}")
                    
                except Exception as e:
                    logger.error(
                        f"Failed to aggregate metrics for agent {agent.id}: {str(e)}",
                        exc_info=True
                    )
                    continue
            
            logger.info("Completed hourly metrics aggregation")
            
        except Exception as e:
            logger.error(f"Metrics aggregation failed: {str(e)}", exc_info=True)
            raise MetricsAggregationError(f"指标聚合失败: {str(e)}")
    
    def _calculate_hourly_metrics(
        self,
        agent_id: str,
        hour: datetime,
        metrics: List[AgentMetrics]
    ) -> AgentMetricsHourly:
        """计算小时聚合指标"""
        cpu_values = [m.cpu_percent for m in metrics]
        memory_values = [m.memory_percent for m in metrics]
        disk_values = [m.disk_usage for m in metrics]
        
        return AgentMetricsHourly(
            id=str(uuid4()),
            agent_id=agent_id,
            hour=hour,
            cpu_percent_avg=sum(cpu_values) / len(cpu_values),
            cpu_percent_max=max(cpu_values),
            memory_percent_avg=sum(memory_values) / len(memory_values),
            memory_percent_max=max(memory_values),
            disk_usage_avg=sum(disk_values) / len(disk_values),
            disk_usage_max=max(disk_values),
            network_in_total=sum(m.network_in for m in metrics),
            network_out_total=sum(m.network_out for m in metrics),
            created_at=datetime.now()
        )
    
    async def cleanup_old_metrics(self):
        """清理过期指标"""
        try:
            # 清理原始指标(保留7天)
            raw_threshold = datetime.now() - timedelta(days=settings.AGENT_METRICS_RETENTION_DAYS)
            await self.service.metrics_repo.cleanup_metrics(raw_threshold)
            
            # 清理聚合指标(保留30天)
            agg_threshold = datetime.now() - timedelta(days=settings.AGENT_METRICS_AGG_RETENTION_DAYS)
            await self.service.metrics_repo.cleanup_hourly_metrics(agg_threshold)
            
            logger.info("Cleaned up old metrics")
        except Exception as e:
            logger.error(f"Failed to cleanup metrics: {str(e)}")
    
    async def run(self):
        """运行聚合和清理任务"""
        while True:
            try:
                # 执行小时聚合
                await self.aggregate_hourly_metrics()
                
                # 每天执行一次清理(在UTC 0点)
                now = datetime.utcnow()
                if now.hour == 0 and now.minute < 5:  # 在0点到0点5分之间执行
                    await self.cleanup_old_metrics()
                
                # 等待到下一个小时
                await asyncio.sleep(3600)
            except Exception as e:
                logger.error(f"Metrics task error: {str(e)}")
                await asyncio.sleep(60)  # 出错时等待1分钟后重试 