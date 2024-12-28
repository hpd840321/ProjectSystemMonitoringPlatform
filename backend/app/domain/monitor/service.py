from typing import List, Dict
from datetime import datetime, timedelta
from .repository import MetricRepository
from .aggregate import MetricPoint, MetricType, ServerMetrics

class MonitorService:
    """监控服务"""
    
    def __init__(self, metric_repo: MetricRepository):
        self.metric_repo = metric_repo
    
    async def record_metrics(self, points: List[MetricPoint]) -> None:
        """记录监控数据"""
        await self.metric_repo.save_metrics(points)
    
    async def get_server_metrics(
        self,
        server_id: str,
        metric_type: MetricType,
        hours: int = 24
    ) -> List[Dict]:
        """获取服务器监控数据"""
        end_time = datetime.now()
        start_time = end_time - timedelta(hours=hours)
        
        return await self.metric_repo.query_metrics(
            server_id=server_id,
            metric_type=metric_type,
            start_time=start_time,
            end_time=end_time,
            interval="5m"  # 5分钟聚合
        )
    
    async def get_project_metrics(
        self,
        project_id: str,
        server_ids: List[str],
        metric_type: MetricType,
        days: int = 7
    ) -> Dict:
        """获取项目监控数据"""
        end_time = datetime.now()
        start_time = end_time - timedelta(days=days)
        
        return await self.metric_repo.aggregate_metrics(
            server_ids=server_ids,
            metric_type=metric_type,
            start_time=start_time,
            end_time=end_time,
            group_by="1h"  # 1小时聚合
        ) 