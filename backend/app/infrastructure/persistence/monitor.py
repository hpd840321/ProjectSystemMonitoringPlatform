from typing import List, Optional
from datetime import datetime
from sqlalchemy import select, and_, text
from .database import Database
from ...domain.monitor.repository import (
    CustomMetricRepository,
    MetricValueRepository,
    MetricAggregationRepository,
    AggregatedMetricRepository,
    RetentionPolicyRepository
)
from ...domain.monitor.aggregate import (
    CustomMetric,
    MetricValue,
    MetricAggregation,
    AggregatedMetric,
    RetentionPolicy,
    MetricType,
    AggregationType
)

class CustomMetricRepositoryImpl(CustomMetricRepository):
    def __init__(self, db: Database):
        self.db = db
    
    async def save(self, metric: CustomMetric) -> None:
        query = """
            INSERT INTO custom_metrics (
                id, project_id, name, description, metric_type,
                unit, labels, collection_script, interval,
                enabled, created_at, updated_at
            ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12)
            ON CONFLICT (id) DO UPDATE SET
                name = $3,
                description = $4,
                metric_type = $5,
                unit = $6,
                labels = $7,
                collection_script = $8,
                interval = $9,
                enabled = $10,
                updated_at = $12
        """
        await self.db.execute(
            query,
            metric.id,
            metric.project_id,
            metric.name,
            metric.description,
            metric.metric_type.value,
            metric.unit,
            metric.labels,
            metric.collection_script,
            metric.interval,
            metric.enabled,
            metric.created_at,
            metric.updated_at
        )
    
    async def get_by_id(self, metric_id: str) -> Optional[CustomMetric]:
        query = "SELECT * FROM custom_metrics WHERE id = $1"
        row = await self.db.fetch_one(query, metric_id)
        if not row:
            return None
        return CustomMetric(
            **{**row, "metric_type": MetricType(row["metric_type"])}
        )
    
    async def list_by_project(self, project_id: str) -> List[CustomMetric]:
        query = "SELECT * FROM custom_metrics WHERE project_id = $1"
        rows = await self.db.fetch_all(query, project_id)
        return [
            CustomMetric(**{**row, "metric_type": MetricType(row["metric_type"])})
            for row in rows
        ]
    
    async def delete(self, metric_id: str) -> None:
        query = "DELETE FROM custom_metrics WHERE id = $1"
        await self.db.execute(query, metric_id)

class MetricValueRepositoryImpl(MetricValueRepository):
    def __init__(self, db: Database):
        self.db = db
    
    async def save_values(self, values: List[MetricValue]) -> None:
        query = """
            INSERT INTO custom_metric_values (
                id, metric_id, server_id, value, labels, timestamp
            ) VALUES ($1, $2, $3, $4, $5, $6)
        """
        await self.db.execute_many(
            query,
            [
                (v.id, v.metric_id, v.server_id, v.value, v.labels, v.timestamp)
                for v in values
            ]
        )
    
    async def get_values(
        self,
        metric_id: str,
        server_id: str,
        start_time: datetime,
        end_time: datetime
    ) -> List[MetricValue]:
        query = """
            SELECT * FROM custom_metric_values
            WHERE metric_id = $1
            AND server_id = $2
            AND timestamp BETWEEN $3 AND $4
            ORDER BY timestamp
        """
        rows = await self.db.fetch_all(
            query,
            metric_id,
            server_id,
            start_time,
            end_time
        )
        return [MetricValue(**row) for row in rows]
    
    async def delete_before(self, metric_id: str, timestamp: datetime) -> None:
        query = """
            DELETE FROM custom_metric_values
            WHERE metric_id = $1 AND timestamp < $2
        """
        await self.db.execute(query, metric_id, timestamp)

class MetricAggregationRepositoryImpl(MetricAggregationRepository):
    def __init__(self, db: Database):
        self.db = db
    
    async def save(self, aggregation: MetricAggregation) -> None:
        query = """
            INSERT INTO metric_aggregations (
                id, metric_id, name, description,
                aggregation_type, interval, retention_days,
                enabled, created_at, updated_at
            ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
            ON CONFLICT (id) DO UPDATE SET
                name = $3,
                description = $4,
                aggregation_type = $5,
                interval = $6,
                retention_days = $7,
                enabled = $8,
                updated_at = $10
        """
        await self.db.execute(
            query,
            aggregation.id,
            aggregation.metric_id,
            aggregation.name,
            aggregation.description,
            aggregation.aggregation_type.value,
            aggregation.interval,
            aggregation.retention_days,
            aggregation.enabled,
            aggregation.created_at,
            aggregation.updated_at
        )
    
    async def list_by_metric(self, metric_id: str) -> List[MetricAggregation]:
        query = "SELECT * FROM metric_aggregations WHERE metric_id = $1"
        rows = await self.db.fetch_all(query, metric_id)
        return [
            MetricAggregation(
                **{**row, "aggregation_type": AggregationType(row["aggregation_type"])}
            )
            for row in rows
        ]
    
    async def delete(self, aggregation_id: str) -> None:
        query = "DELETE FROM metric_aggregations WHERE id = $1"
        await self.db.execute(query, aggregation_id)

class AggregatedMetricRepositoryImpl(AggregatedMetricRepository):
    def __init__(self, db: Database):
        self.db = db
    
    async def save_values(self, values: List[AggregatedMetric]) -> None:
        query = """
            INSERT INTO aggregated_metrics (
                id, aggregation_id, server_id,
                value, start_time, end_time
            ) VALUES ($1, $2, $3, $4, $5, $6)
        """
        await self.db.execute_many(
            query,
            [
                (
                    v.id, v.aggregation_id, v.server_id,
                    v.value, v.start_time, v.end_time
                )
                for v in values
            ]
        )
    
    async def get_values(
        self,
        aggregation_id: str,
        server_id: str,
        start_time: datetime,
        end_time: datetime
    ) -> List[AggregatedMetric]:
        query = """
            SELECT * FROM aggregated_metrics
            WHERE aggregation_id = $1
            AND server_id = $2
            AND start_time >= $3
            AND end_time <= $4
            ORDER BY start_time
        """
        rows = await self.db.fetch_all(
            query,
            aggregation_id,
            server_id,
            start_time,
            end_time
        )
        return [AggregatedMetric(**row) for row in rows]
    
    async def delete_before(self, aggregation_id: str, timestamp: datetime) -> None:
        query = """
            DELETE FROM aggregated_metrics
            WHERE aggregation_id = $1 AND end_time < $2
        """
        await self.db.execute(query, aggregation_id, timestamp)

class RetentionPolicyRepositoryImpl(RetentionPolicyRepository):
    def __init__(self, db: Database):
        self.db = db
    
    async def save(self, policy: RetentionPolicy) -> None:
        query = """
            INSERT INTO metric_retention_policies (
                id, metric_id,
                raw_data_retention_days,
                aggregated_data_retention_days,
                created_at, updated_at
            ) VALUES ($1, $2, $3, $4, $5, $6)
            ON CONFLICT (id) DO UPDATE SET
                raw_data_retention_days = $3,
                aggregated_data_retention_days = $4,
                updated_at = $6
        """
        await self.db.execute(
            query,
            policy.id,
            policy.metric_id,
            policy.raw_data_retention_days,
            policy.aggregated_data_retention_days,
            policy.created_at,
            policy.updated_at
        )
    
    async def get_by_metric(self, metric_id: str) -> Optional[RetentionPolicy]:
        query = "SELECT * FROM metric_retention_policies WHERE metric_id = $1"
        row = await self.db.fetch_one(query, metric_id)
        if not row:
            return None
        return RetentionPolicy(**row)
    
    async def delete(self, policy_id: str) -> None:
        query = "DELETE FROM metric_retention_policies WHERE id = $1"
        await self.db.execute(query, policy_id) 