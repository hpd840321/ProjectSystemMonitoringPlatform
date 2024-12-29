from typing import Optional, Dict, List
import aiohttp
from app.gateway.config import GatewayConfig

class ServiceInstance:
    def __init__(self, host: str, port: int, metadata: Dict = None):
        self.host = host
        self.port = port
        self.metadata = metadata or {}
        self.healthy = True

class ServiceDiscovery:
    def __init__(self, config: GatewayConfig):
        self.config = config
        self._services: Dict[str, List[ServiceInstance]] = {}
        
    async def get_service(self, service_name: str) -> Optional[ServiceInstance]:
        """获取服务实例"""
        if service_name not in self._services:
            await self._refresh_service(service_name)
            
        instances = self._services.get(service_name, [])
        return self._select_instance(instances)
        
    async def _refresh_service(self, service_name: str):
        """刷新服务列表"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.config.service_registry_url}/services/{service_name}"
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        self._services[service_name] = [
                            ServiceInstance(**instance)
                            for instance in data["instances"]
                        ]
        except Exception as e:
            # 处理异常
            pass

    def _select_instance(self, instances: List[ServiceInstance]) -> Optional[ServiceInstance]:
        """选择服务实例(负载均衡)"""
        healthy_instances = [i for i in instances if i.healthy]
        if not healthy_instances:
            return None
            
        # 简单轮询策略
        return healthy_instances[0]  # 实际应用中应该实现proper轮询 