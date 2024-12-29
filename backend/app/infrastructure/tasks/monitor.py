import asyncio
from datetime import datetime, timedelta
from typing import List
from ...domain.monitor.service import MonitorService
from ...domain.monitor.aggregate import CustomMetric, MetricAggregation
from ..persistence.monitor import (
    CustomMetricRepositoryImpl,
    MetricValueRepositoryImpl,
    MetricAggregationRepositoryImpl,
    AggregatedMetricRepositoryImpl,
    RetentionPolicyRepositoryImpl
)
from ..database import get_database
import logging

logger = logging.getLogger(__name__)

class MonitorTasks:
    def __init__(self):
        self.db = get_database()
        self.service = MonitorService(
            custom_metric_repo=CustomMetricRepositoryImpl(self.db),
            metric_value_repo=MetricValueRepositoryImpl(self.db),
            aggregation_repo=MetricAggregationRepositoryImpl(self.db),
            aggregated_metric_repo=AggregatedMetricRepositoryImpl(self.db),
            retention_policy_repo=RetentionPolicyRepositoryImpl(self.db)
        )
    
    async def start(self):
        """启动监控任务"""
        await asyncio.gather(
            self._run_cleanup_task(),
            self._run_aggregation_task()
        )
    
    async def _run_cleanup_task(self):
        """运行数据清理任务"""
        while True:
            try:
                await self._cleanup_expired_data()
            except Exception as e:
                logger.error(f"Failed to cleanup data: {e}")
            
            # 每天执行一次
            await asyncio.sleep(24 * 60 * 60)
    
    async def _run_aggregation_task(self):
        """运行数据聚合任务"""
        while True:
            try:
                await self._aggregate_metrics()
            except Exception as e:
                logger.error(f"Failed to aggregate metrics: {e}")
            
            # 每分钟执行一次
            await asyncio.sleep(60)
    
    async def _cleanup_expired_data(self):
        """清理过期数据"""
        # 获取所有自定义指标
        metrics = await self.service.custom_metric_repo.list_all()
        
        for metric in metrics:
            # 获取保留策略
            policy = await self.service.retention_policy_repo.get_by_metric(metric.id)
            if not policy:
                continue
            
            # 清理原始数据
            raw_expire_time = datetime.now() - timedelta(days=policy.raw_data_retention_days)
            await self.service.metric_value_repo.delete_before(
                metric.id,
                raw_expire_time
            )
            
            # 清理聚合数据
            agg_expire_time = datetime.now() - timedelta(days=policy.aggregated_data_retention_days)
            aggregations = await self.service.aggregation_repo.list_by_metric(metric.id)
            for agg in aggregations:
                await self.service.aggregated_metric_repo.delete_before(
                    agg.id,
                    agg_expire_time
                )
            
            logger.info(f"Cleaned up expired data for metric {metric.id}")
    
    async def _aggregate_metrics(self):
        """聚合监控数据"""
        # 获取所有自定义指标
        metrics = await self.service.custom_metric_repo.list_all()
        
        for metric in metrics:
            # 获取聚合配置
            aggregations = await self.service.aggregation_repo.list_by_metric(metric.id)
            if not aggregations:
                continue
            
            # 获取需要聚合的服务器列表
            servers = await self._get_metric_servers(metric.id)
            
            # 对每个服务器执行聚合
            for server_id in servers:
                await self.service._aggregate_metrics(metric.id, server_id)
            
            logger.info(f"Aggregated metrics for {metric.id}")
    
    async def _get_metric_servers(self, metric_id: str) -> List[str]:
        """获取指标相关的服务器列表"""
        # TODO: 实现获取服务器列表的逻辑
        return [] 