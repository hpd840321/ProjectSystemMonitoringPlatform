from pydantic import BaseModel, Field
from typing import Dict, Optional, List
from datetime import datetime
from ....domain.monitor.aggregate import MetricType, AggregationType

class CustomMetricCreate(BaseModel):
    name: str = Field(..., description="指标名称")
    metric_type: MetricType = Field(..., description="指标类型(counter/gauge)")
    collection_script: str = Field(..., description="采集脚本")
    interval: int = Field(..., description="采集间隔(秒)")
    unit: Optional[str] = Field(None, description="单位(如:bytes/seconds)")
    labels: Optional[Dict] = Field(None, description="标签配置")
    description: Optional[str] = Field(None, description="描述")

class CustomMetricResponse(BaseModel):
    id: str
    project_id: str
    name: str
    metric_type: str
    collection_script: str
    interval: int
    unit: Optional[str]
    labels: Dict
    description: Optional[str]
    enabled: bool
    created_at: datetime
    updated_at: datetime
    
    @classmethod
    def from_domain(cls, metric):
        return cls(
            id=metric.id,
            project_id=metric.project_id,
            name=metric.name,
            metric_type=metric.metric_type.value,
            collection_script=metric.collection_script,
            interval=metric.interval,
            unit=metric.unit,
            labels=metric.labels,
            description=metric.description,
            enabled=metric.enabled,
            created_at=metric.created_at,
            updated_at=metric.updated_at
        )

class MetricValueCreate(BaseModel):
    value: float = Field(..., description="指标值")
    labels: Optional[Dict] = Field(None, description="标签值")
    timestamp: datetime = Field(..., description="时间戳")

class MetricValueResponse(BaseModel):
    id: str
    metric_id: str
    server_id: str
    value: float
    labels: Dict
    timestamp: datetime
    
    @classmethod
    def from_domain(cls, value):
        return cls(
            id=value.id,
            metric_id=value.metric_id,
            server_id=value.server_id,
            value=value.value,
            labels=value.labels,
            timestamp=value.timestamp
        )

class AggregationCreate(BaseModel):
    name: str = Field(..., description="聚合配置名称")
    aggregation_type: AggregationType = Field(..., description="聚合类型")
    interval: str = Field(..., description="聚合间隔(如:5m/1h/1d)")
    retention_days: int = Field(..., description="保留天数")
    description: Optional[str] = Field(None, description="描述")

class AggregationResponse(BaseModel):
    id: str
    metric_id: str
    name: str
    aggregation_type: str
    interval: str
    retention_days: int
    description: Optional[str]
    enabled: bool
    created_at: datetime
    updated_at: datetime
    
    @classmethod
    def from_domain(cls, agg):
        return cls(
            id=agg.id,
            metric_id=agg.metric_id,
            name=agg.name,
            aggregation_type=agg.aggregation_type.value,
            interval=agg.interval,
            retention_days=agg.retention_days,
            description=agg.description,
            enabled=agg.enabled,
            created_at=agg.created_at,
            updated_at=agg.updated_at
        )

class RetentionPolicyCreate(BaseModel):
    raw_data_retention_days: int = Field(..., description="原始数据保留天数")
    aggregated_data_retention_days: int = Field(..., description="聚合数据保留天数")

class RetentionPolicyResponse(BaseModel):
    id: str
    metric_id: str
    raw_data_retention_days: int
    aggregated_data_retention_days: int
    created_at: datetime
    updated_at: datetime
    
    @classmethod
    def from_domain(cls, policy):
        return cls(
            id=policy.id,
            metric_id=policy.metric_id,
            raw_data_retention_days=policy.raw_data_retention_days,
            aggregated_data_retention_days=policy.aggregated_data_retention_days,
            created_at=policy.created_at,
            updated_at=policy.updated_at
        ) 