from typing import List, Dict, Optional
from datetime import datetime, timedelta
from .repository import (
    CustomMetricRepository,
    MetricValueRepository,
    MetricAggregationRepository,
    AggregatedMetricRepository,
    RetentionPolicyRepository
)
from .aggregate import (
    CustomMetric,
    MetricValue,
    MetricAggregation,
    AggregatedMetric,
    RetentionPolicy,
    MetricType,
    AggregationType
)

class MonitorService:
    def __init__(
        self,
        custom_metric_repo: CustomMetricRepository,
        metric_value_repo: MetricValueRepository,
        aggregation_repo: MetricAggregationRepository,
        aggregated_metric_repo: AggregatedMetricRepository,
        retention_policy_repo: RetentionPolicyRepository
    ):
        self.custom_metric_repo = custom_metric_repo
        self.metric_value_repo = metric_value_repo
        self.aggregation_repo = aggregation_repo
        self.aggregated_metric_repo = aggregated_metric_repo
        self.retention_policy_repo = retention_policy_repo
    
    # 自定义指标管理
    async def create_custom_metric(
        self,
        project_id: str,
        name: str,
        metric_type: MetricType,
        collection_script: str,
        interval: int,
        unit: Optional[str] = None,
        labels: Optional[Dict] = None,
        description: Optional[str] = None
    ) -> CustomMetric:
        """创建自定义监控指标"""
        now = datetime.now()
        metric = CustomMetric(
            id=str(uuid4()),
            project_id=project_id,
            name=name,
            description=description,
            metric_type=metric_type,
            unit=unit,
            labels=labels or {},
            collection_script=collection_script,
            interval=interval,
            enabled=True,
            created_at=now,
            updated_at=now
        )
        await self.custom_metric_repo.save(metric)
        return metric
    
    # 指标数据管理
    async def record_metric_values(
        self,
        metric_id: str,
        server_id: str,
        values: List[Dict]
    ) -> None:
        """记录指标数据"""
        metric_values = []
        for value_data in values:
            value = MetricValue(
                id=str(uuid4()),
                metric_id=metric_id,
                server_id=server_id,
                value=value_data["value"],
                labels=value_data.get("labels", {}),
                timestamp=value_data["timestamp"]
            )
            metric_values.append(value)
        
        await self.metric_value_repo.save_values(metric_values)
        
        # 触发数据聚合
        await self._aggregate_metrics(metric_id, server_id)
    
    # 指标聚合管理
    async def create_aggregation(
        self,
        metric_id: str,
        name: str,
        aggregation_type: AggregationType,
        interval: str,
        retention_days: int,
        description: Optional[str] = None
    ) -> MetricAggregation:
        """创建指标聚合配置"""
        now = datetime.now()
        aggregation = MetricAggregation(
            id=str(uuid4()),
            metric_id=metric_id,
            name=name,
            description=description,
            aggregation_type=aggregation_type,
            interval=interval,
            retention_days=retention_days,
            enabled=True,
            created_at=now,
            updated_at=now
        )
        await self.aggregation_repo.save(aggregation)
        return aggregation
    
    async def _aggregate_metrics(self, metric_id: str, server_id: str) -> None:
        """执行指标聚合"""
        # 获取聚合配置
        aggregations = await self.aggregation_repo.list_by_metric(metric_id)
        
        for agg in aggregations:
            if not agg.enabled:
                continue
            
            # 计算时间窗口
            end_time = datetime.now()
            interval = self._parse_interval(agg.interval)
            start_time = end_time - interval
            
            # 获取原始数据
            values = await self.metric_value_repo.get_values(
                metric_id,
                server_id,
                start_time,
                end_time
            )
            
            if not values:
                continue
            
            # 计算聚合值
            agg_value = self._calculate_aggregation(
                [v.value for v in values],
                agg.aggregation_type
            )
            
            # 保存聚合结果
            aggregated = AggregatedMetric(
                id=str(uuid4()),
                aggregation_id=agg.id,
                server_id=server_id,
                value=agg_value,
                start_time=start_time,
                end_time=end_time
            )
            await self.aggregated_metric_repo.save_values([aggregated])
    
    def _parse_interval(self, interval: str) -> timedelta:
        """解析时间间隔"""
        value = int(interval[:-1])
        unit = interval[-1]
        
        if unit == 'm':
            return timedelta(minutes=value)
        elif unit == 'h':
            return timedelta(hours=value)
        elif unit == 'd':
            return timedelta(days=value)
        else:
            raise ValueError(f"Invalid interval: {interval}")
    
    def _calculate_aggregation(
        self,
        values: List[float],
        agg_type: AggregationType
    ) -> float:
        """计算聚合值"""
        if agg_type == AggregationType.AVG:
            return sum(values) / len(values)
        elif agg_type == AggregationType.MAX:
            return max(values)
        elif agg_type == AggregationType.MIN:
            return min(values)
        elif agg_type == AggregationType.SUM:
            return sum(values)
        else:
            raise ValueError(f"Invalid aggregation type: {agg_type}")
    
    # 数据保留策略管理
    async def set_retention_policy(
        self,
        metric_id: str,
        raw_days: int,
        aggregated_days: int
    ) -> RetentionPolicy:
        """设置数据保留策略"""
        now = datetime.now()
        policy = RetentionPolicy(
            id=str(uuid4()),
            metric_id=metric_id,
            raw_data_retention_days=raw_days,
            aggregated_data_retention_days=aggregated_days,
            created_at=now,
            updated_at=now
        )
        await self.retention_policy_repo.save(policy)
        return policy
    
    async def cleanup_expired_data(self) -> None:
        """清理过期数据"""
        # TODO: 实现数据清理逻辑
        pass 