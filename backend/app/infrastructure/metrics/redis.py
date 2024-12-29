from prometheus_client import Counter, Histogram

class RedisMetrics:
    """Redis监控指标"""
    
    def __init__(self):
        self.operations = Counter(
            'redis_operations_total',
            'Total number of Redis operations',
            ['operation']
        )
        self.latency = Histogram(
            'redis_operation_latency_seconds',
            'Redis operation latency in seconds',
            ['operation']
        )
        
redis_metrics = RedisMetrics() 