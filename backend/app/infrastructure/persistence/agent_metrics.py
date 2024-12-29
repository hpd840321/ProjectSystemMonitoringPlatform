from typing import List
from datetime import datetime
from uuid import uuid4
from .database import Database
from ...domain.agent.metrics import (
    AgentMetrics,
    AgentMetricsHourly,
    AgentMetricsRepository
)

class AgentMetricsRepositoryImpl(AgentMetricsRepository):
    def __init__(self, db: Database):
        self.db = db
    
    async def save_metrics(self, metrics: AgentMetrics) -> None:
        query = """
            INSERT INTO agent_metrics (
                id, agent_id, timestamp,
                cpu_percent, memory_percent, disk_usage,
                network_in, network_out, created_at
            ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
        """
        await self.db.execute(
            query,
            metrics.id,
            metrics.agent_id,
            metrics.timestamp,
            metrics.cpu_percent,
            metrics.memory_percent,
            metrics.disk_usage,
            metrics.network_in,
            metrics.network_out,
            metrics.created_at
        )
    
    async def save_hourly_metrics(self, metrics: AgentMetricsHourly) -> None:
        query = """
            INSERT INTO agent_metrics_hourly (
                id, agent_id, hour,
                cpu_percent_avg, cpu_percent_max,
                memory_percent_avg, memory_percent_max,
                disk_usage_avg, disk_usage_max,
                network_in_total, network_out_total,
                created_at
            ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12)
        """
        await self.db.execute(
            query,
            metrics.id,
            metrics.agent_id,
            metrics.hour,
            metrics.cpu_percent_avg,
            metrics.cpu_percent_max,
            metrics.memory_percent_avg,
            metrics.memory_percent_max,
            metrics.disk_usage_avg,
            metrics.disk_usage_max,
            metrics.network_in_total,
            metrics.network_out_total,
            metrics.created_at
        )
    
    async def get_metrics(
        self,
        agent_id: str,
        start_time: datetime,
        end_time: datetime
    ) -> List[AgentMetrics]:
        query = """
            SELECT * FROM agent_metrics
            WHERE agent_id = $1
            AND timestamp BETWEEN $2 AND $3
            ORDER BY timestamp
        """
        rows = await self.db.fetch_all(query, agent_id, start_time, end_time)
        return [AgentMetrics(**row) for row in rows]
    
    async def get_hourly_metrics(
        self,
        agent_id: str,
        start_time: datetime,
        end_time: datetime
    ) -> List[AgentMetricsHourly]:
        query = """
            SELECT * FROM agent_metrics_hourly
            WHERE agent_id = $1
            AND hour BETWEEN $2 AND $3
            ORDER BY hour
        """
        rows = await self.db.fetch_all(query, agent_id, start_time, end_time)
        return [AgentMetricsHourly(**row) for row in rows]
    
    async def cleanup_metrics(self, before: datetime) -> None:
        """清理指标数据"""
        await self.db.execute(
            "DELETE FROM agent_metrics WHERE timestamp < $1",
            before
        ) 