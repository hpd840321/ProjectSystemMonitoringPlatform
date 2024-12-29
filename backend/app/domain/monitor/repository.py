from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import datetime
from .aggregate import (
    CustomMetric,
    MetricValue,
    MetricAggregation,
    AggregatedMetric,
    RetentionPolicy
)

class CustomMetricRepository(ABC):
    @abstractmethod
    async def save(self, metric: CustomMetric) -> None:
        pass
    
    @abstractmethod
    async def get_by_id(self, metric_id: str) -> Optional[CustomMetric]:
        pass
    
    @abstractmethod
    async def list_by_project(self, project_id: str) -> List[CustomMetric]:
        pass
    
    @abstractmethod
    async def delete(self, metric_id: str) -> None:
        pass

class MetricValueRepository(ABC):
    @abstractmethod
    async def save_values(self, values: List[MetricValue]) -> None:
        pass
    
    @abstractmethod
    async def get_values(
        self,
        metric_id: str,
        server_id: str,
        start_time: datetime,
        end_time: datetime
    ) -> List[MetricValue]:
        pass
    
    @abstractmethod
    async def delete_before(self, metric_id: str, timestamp: datetime) -> None:
        pass

class MetricAggregationRepository(ABC):
    @abstractmethod
    async def save(self, aggregation: MetricAggregation) -> None:
        pass
    
    @abstractmethod
    async def list_by_metric(self, metric_id: str) -> List[MetricAggregation]:
        pass
    
    @abstractmethod
    async def delete(self, aggregation_id: str) -> None:
        pass

class AggregatedMetricRepository(ABC):
    @abstractmethod
    async def save_values(self, values: List[AggregatedMetric]) -> None:
        pass
    
    @abstractmethod
    async def get_values(
        self,
        aggregation_id: str,
        server_id: str,
        start_time: datetime,
        end_time: datetime
    ) -> List[AggregatedMetric]:
        pass
    
    @abstractmethod
    async def delete_before(self, aggregation_id: str, timestamp: datetime) -> None:
        pass

class RetentionPolicyRepository(ABC):
    @abstractmethod
    async def save(self, policy: RetentionPolicy) -> None:
        pass
    
    @abstractmethod
    async def get_by_metric(self, metric_id: str) -> Optional[RetentionPolicy]:
        pass
    
    @abstractmethod
    async def delete(self, policy_id: str) -> None:
        pass 