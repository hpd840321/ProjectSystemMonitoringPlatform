class AgentMetricsError(Exception):
    """Agent指标异常基类"""
    pass

class MetricsNotFoundError(AgentMetricsError):
    """指标数据不存在"""
    pass

class InvalidTimeRangeError(AgentMetricsError):
    """无效的时间范围"""
    pass

class MetricsAggregationError(AgentMetricsError):
    """指标聚合错误"""
    pass 