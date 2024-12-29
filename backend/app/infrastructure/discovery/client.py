import logging
from typing import List, Optional
import random
from datetime import datetime, timedelta

from app.infrastructure.discovery.base import ServiceInstance
from app.infrastructure.discovery.redis_registry import registry

logger = logging.getLogger(__name__)

class ServiceDiscoveryClient:
    """服务发现客户端"""

    def __init__(self):
        self._cache = {}  # 本地缓存
        self._cache_ttl = 30  # 缓存TTL（秒）
        self._max_cache_items = 100

    async def get_service(
        self,
        service_name: str,
        use_cache: bool = True
    ) -> Optional[ServiceInstance]:
        """获取服务实例（使用随机负载均衡）"""
        try:
            instances = await self.get_services(
                service_name,
                use_cache=use_cache
            )
            if not instances:
                return None
            
            # 过滤出健康的实例
            healthy_instances = [
                i for i in instances
                if i.status == "UP"
            ]
            if not healthy_instances:
                return None
            
            # 随机选择一个实例
            return random.choice(healthy_instances)
        except Exception as e:
            logger.error(f"Failed to get service: {str(e)}")
            return None

    async def get_services(
        self,
        service_name: str,
        use_cache: bool = True
    ) -> List[ServiceInstance]:
        """获取服务的所有实例"""
        try:
            # 检查并清理过期缓存
            if len(self._cache) > self._max_cache_items:
                self._clean_expired_cache()
                
            # 检查缓存
            if use_cache and service_name in self._cache:
                cache_data = self._cache[service_name]
                if datetime.now() < cache_data["expires"]:
                    return cache_data["instances"]
            
            # 从注册中心获取实例
            instances = await registry.get_instances(service_name)
            
            # 更新缓存
            if use_cache:
                self._cache[service_name] = {
                    "instances": instances,
                    "expires": datetime.now() + timedelta(
                        seconds=self._cache_ttl
                    )
                }
            
            return instances
        except Exception as e:
            logger.error(f"Failed to get services: {str(e)}")
            return []

    def invalidate_cache(self, service_name: Optional[str] = None) -> None:
        """清除缓存"""
        if service_name:
            self._cache.pop(service_name, None)
        else:
            self._cache.clear()

    def _clean_expired_cache(self):
        """清理过期缓存"""
        now = datetime.now()
        expired_keys = [
            k for k, v in self._cache.items() 
            if now >= v["expires"]
        ]
        for k in expired_keys:
            self._cache.pop(k, None)

discovery_client = ServiceDiscoveryClient() 