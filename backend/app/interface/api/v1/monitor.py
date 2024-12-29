from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List
from datetime import datetime
from .dependencies import get_current_user, get_monitor_service
from .schemas.monitor import (
    CustomMetricCreate,
    CustomMetricResponse,
    MetricValueCreate,
    MetricValueResponse,
    AggregationCreate,
    AggregationResponse,
    RetentionPolicyCreate,
    RetentionPolicyResponse
)
from ....domain.monitor.aggregate import MetricType, AggregationType

router = APIRouter()

# 自定义指标管理
@router.post("/projects/{project_id}/metrics", response_model=CustomMetricResponse)
async def create_custom_metric(
    project_id: str,
    data: CustomMetricCreate,
    service = Depends(get_monitor_service),
    user = Depends(get_current_user)
):
    """创建自定义监控指标"""
    try:
        metric = await service.create_custom_metric(
            project_id=project_id,
            name=data.name,
            metric_type=data.metric_type,
            collection_script=data.collection_script,
            interval=data.interval,
            unit=data.unit,
            labels=data.labels,
            description=data.description
        )
        return CustomMetricResponse.from_domain(metric)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/projects/{project_id}/metrics", response_model=List[CustomMetricResponse])
async def list_custom_metrics(
    project_id: str,
    service = Depends(get_monitor_service)
):
    """获取项目的自定义指标列表"""
    metrics = await service.custom_metric_repo.list_by_project(project_id)
    return [CustomMetricResponse.from_domain(m) for m in metrics]

# 指标数据管理
@router.post("/metrics/{metric_id}/values")
async def record_metric_values(
    metric_id: str,
    server_id: str,
    values: List[MetricValueCreate],
    service = Depends(get_monitor_service)
):
    """记录指标数据"""
    try:
        await service.record_metric_values(
            metric_id=metric_id,
            server_id=server_id,
            values=[v.dict() for v in values]
        )
        return {"message": "success"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/metrics/{metric_id}/values", response_model=List[MetricValueResponse])
async def get_metric_values(
    metric_id: str,
    server_id: str,
    start_time: datetime,
    end_time: datetime,
    service = Depends(get_monitor_service)
):
    """查询指标数据"""
    values = await service.metric_value_repo.get_values(
        metric_id=metric_id,
        server_id=server_id,
        start_time=start_time,
        end_time=end_time
    )
    return [MetricValueResponse.from_domain(v) for v in values]

# 指标聚合管理
@router.post("/metrics/{metric_id}/aggregations", response_model=AggregationResponse)
async def create_aggregation(
    metric_id: str,
    data: AggregationCreate,
    service = Depends(get_monitor_service),
    user = Depends(get_current_user)
):
    """创建指标聚合配置"""
    try:
        aggregation = await service.create_aggregation(
            metric_id=metric_id,
            name=data.name,
            aggregation_type=data.aggregation_type,
            interval=data.interval,
            retention_days=data.retention_days,
            description=data.description
        )
        return AggregationResponse.from_domain(aggregation)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/metrics/{metric_id}/aggregations", response_model=List[AggregationResponse])
async def list_aggregations(
    metric_id: str,
    service = Depends(get_monitor_service)
):
    """获取指标的聚合配置��表"""
    aggregations = await service.aggregation_repo.list_by_metric(metric_id)
    return [AggregationResponse.from_domain(a) for a in aggregations]

# 数据保留策略管理
@router.post("/metrics/{metric_id}/retention", response_model=RetentionPolicyResponse)
async def set_retention_policy(
    metric_id: str,
    data: RetentionPolicyCreate,
    service = Depends(get_monitor_service),
    user = Depends(get_current_user)
):
    """设置数据保留策略"""
    try:
        policy = await service.set_retention_policy(
            metric_id=metric_id,
            raw_days=data.raw_data_retention_days,
            aggregated_days=data.aggregated_data_retention_days
        )
        return RetentionPolicyResponse.from_domain(policy)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/metrics/{metric_id}/retention", response_model=RetentionPolicyResponse)
async def get_retention_policy(
    metric_id: str,
    service = Depends(get_monitor_service)
):
    """获取数据保留策略"""
    policy = await service.retention_policy_repo.get_by_metric(metric_id)
    if not policy:
        raise HTTPException(status_code=404, detail="保留策略不存在")
    return RetentionPolicyResponse.from_domain(policy) 