from typing import List, Optional
import json
from datetime import datetime, timedelta
from ...domain.agent.metrics import AgentMetrics, AgentMetricsHourly

class AgentMetricsCache:
    """Agent指标缓存"""
    
    def __init__(self, redis):
        self.redis = redis
        self.raw_prefix = "agent:metrics:raw:"
        self.hourly_prefix = "agent:metrics:hourly:"
        self.ttl = 3600  # 缓存1小时
    
    async def get_raw_metrics(
        self,
        agent_id: str,
        start_time: datetime,
        end_time: datetime
    ) -> Optional[List[AgentMetrics]]:
        """获取原始指标缓存"""
        key = f"{self.raw_prefix}{agent_id}:{start_time.isoformat()}:{end_time.isoformat()}"
        data = await self.redis.get(key)
        if not data:
            return None
        
        metrics_data = json.loads(data)
        return [
            AgentMetrics(
                **{
                    **m,
                    "timestamp": datetime.fromisoformat(m["timestamp"]),
                    "created_at": datetime.fromisoformat(m["created_at"])
                }
            )
            for m in metrics_data
        ]
    
    async def set_raw_metrics(
        self,
        agent_id: str,
        start_time: datetime,
        end_time: datetime,
        metrics: List[AgentMetrics]
    ) -> None:
        """设置原始指标缓存"""
        key = f"{self.raw_prefix}{agent_id}:{start_time.isoformat()}:{end_time.isoformat()}"
        data = [
            {
                **m.__dict__,
                "timestamp": m.timestamp.isoformat(),
                "created_at": m.created_at.isoformat()
            }
            for m in metrics
        ]
        await self.redis.setex(key, self.ttl, json.dumps(data))
    
    async def get_hourly_metrics(
        self,
        agent_id: str,
        start_time: datetime,
        end_time: datetime
    ) -> Optional[List[AgentMetricsHourly]]:
        """获取小时聚合指标缓存"""
        key = f"{self.hourly_prefix}{agent_id}:{start_time.isoformat()}:{end_time.isoformat()}"
        data = await self.redis.get(key)
        if not data:
            return None
        
        metrics_data = json.loads(data)
        return [
            AgentMetricsHourly(
                **{
                    **m,
                    "hour": datetime.fromisoformat(m["hour"]),
                    "created_at": datetime.fromisoformat(m["created_at"])
                }
            )
            for m in metrics_data
        ]
    
    async def set_hourly_metrics(
        self,
        agent_id: str,
        start_time: datetime,
        end_time: datetime,
        metrics: List[AgentMetricsHourly]
    ) -> None:
        """设置小时聚合指标缓存"""
        key = f"{self.hourly_prefix}{agent_id}:{start_time.isoformat()}:{end_time.isoformat()}"
        data = [
            {
                **m.__dict__,
                "hour": m.hour.isoformat(),
                "created_at": m.created_at.isoformat()
            }
            for m in metrics
        ]
        await self.redis.setex(key, self.ttl, json.dumps(data)) 