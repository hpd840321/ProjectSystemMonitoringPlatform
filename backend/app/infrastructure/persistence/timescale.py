from datetime import datetime
from typing import List, Dict
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.monitor.repository import MetricRepository
from app.domain.monitor.aggregate import MetricPoint, MetricType

class TimescaleMetricRepository(MetricRepository):
    """TimescaleDB监控数据仓储实现"""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def save_metrics(self, points: List[MetricPoint]) -> None:
        """保存监控数据点"""
        values = [
            {
                "server_id": p.server_id,
                "metric_type": p.metric_type,
                "value": p.value,
                "timestamp": p.timestamp,
                "labels": p.labels
            }
            for p in points
        ]
        
        query = text("""
            INSERT INTO metrics (
                server_id, metric_type, value, timestamp, labels
            ) VALUES (
                :server_id, :metric_type, :value, :timestamp, :labels
            )
        """)
        
        await self.session.execute(query, values)
        await self.session.commit()
    
    async def query_metrics(
        self,
        server_id: str,
        metric_type: MetricType,
        start_time: datetime,
        end_time: datetime,
        interval: str = "1m"
    ) -> List[Dict]:
        """查询监控数据"""
        query = text("""
            SELECT time_bucket(:interval, timestamp) AS time,
                   avg(value) as value,
                   min(value) as min,
                   max(value) as max
            FROM metrics
            WHERE server_id = :server_id
              AND metric_type = :metric_type
              AND timestamp BETWEEN :start_time AND :end_time
            GROUP BY time
            ORDER BY time
        """)
        
        result = await self.session.execute(
            query,
            {
                "server_id": server_id,
                "metric_type": metric_type,
                "start_time": start_time,
                "end_time": end_time,
                "interval": interval
            }
        )
        
        return [dict(row) for row in result] 