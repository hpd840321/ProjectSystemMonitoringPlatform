from pydantic import BaseSettings
from typing import List, Dict

class GatewayConfig(BaseSettings):
    # 服务发现配置
    service_registry_url: str
    service_registry_token: str
    
    # 负载均衡配置
    load_balancer_strategy: str = "round_robin"
    
    # 限流配置
    rate_limit_enabled: bool = True
    rate_limit_requests: int = 100
    rate_limit_window: int = 60  # seconds
    
    # 路由配置
    service_routes: Dict[str, str] = {
        "agent": "http://agent-service:8001",
        "monitor": "http://monitor-service:8002",
        "plugin": "http://plugin-service:8003"
    }
    
    # CORS配置
    cors_origins: List[str] = ["*"]
    
    class Config:
        env_prefix = "GATEWAY_" 