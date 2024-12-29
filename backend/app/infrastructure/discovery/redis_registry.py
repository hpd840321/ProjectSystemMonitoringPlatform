import json
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import aioredis
from aioredis import ConnectionPool

from app.infrastructure.discovery.base import ServiceRegistry, ServiceInstance
from app.core.config import settings

logger = logging.getLogger(__name__)

class RedisServiceRegistry(ServiceRegistry):
    """基于Redis的服务注册中心"""

    def __init__(self, redis_url: str):
        # 使用连接池
        self._pool = ConnectionPool.from_url(
            redis_url,
            max_connections=10,  # 限制最大连接数
            timeout=30
        )
        self._redis = aioredis.Redis(
            connection_pool=self._pool,
            decode_responses=True
        )
        self._key_prefix = "service:"
        self._ttl = 60  # 从30秒改为60秒

    async def register(self, instance: ServiceInstance) -> bool:
        """注册服务实例"""
        try:
            # 生成Redis键
            instance_key = f"{self._key_prefix}{instance.name}:{instance.id}"
            service_key = f"{self._key_prefix}{instance.name}"

            # 使用pipeline批量操作
            async with self._redis.pipeline() as pipe:
                pipe.hset(instance_key, mapping={
                    "id": instance.id,
                    "name": instance.name,
                    "host": instance.host,
                    "port": instance.port,
                    "metadata": json.dumps(instance.metadata),
                    "health_check_url": instance.health_check_url or "",
                    "status": instance.status,
                    "last_updated": datetime.now().isoformat()
                })
                pipe.expire(instance_key, self._ttl)
                pipe.sadd(service_key, instance.id)
                await pipe.execute()
                return True
        except aioredis.RedisError as e:
            logger.error(f"Redis error: {str(e)}")
            # 使用本地缓存作为降级方案
            return self._fallback_register(instance)
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return False

    def _fallback_register(self, instance: ServiceInstance) -> bool:
        """Redis不可用时的降级方案"""
        try:
            # 使用内存存储
            self._local_cache[instance.id] = instance
            return True
        except Exception:
            return False

    async def deregister(self, instance_id: str) -> bool:
        """注销服务实例"""
        try:
            # 查找实例
            instance = await self.get_instance(instance_id)
            if not instance:
                return False

            # 删除实例信息
            instance_key = f"{self._key_prefix}{instance.name}:{instance.id}"
            service_key = f"{self._key_prefix}{instance.name}"
            
            await self._redis.delete(instance_key)
            await self._redis.srem(service_key, instance.id)
            
            return True
        except Exception as e:
            logger.error(f"Failed to deregister service instance: {str(e)}")
            return False

    async def renew(self, instance_id: str) -> bool:
        """续约服务实例"""
        try:
            # 查找实例
            instance = await self.get_instance(instance_id)
            if not instance:
                return False

            # 更新最后更新时间并刷新TTL
            instance_key = f"{self._key_prefix}{instance.name}:{instance.id}"
            await self._redis.hset(
                instance_key,
                "last_updated",
                datetime.now().isoformat()
            )
            await self._redis.expire(instance_key, self._ttl)
            
            return True
        except Exception as e:
            logger.error(f"Failed to renew service instance: {str(e)}")
            return False

    async def get_instance(self, instance_id: str) -> Optional[ServiceInstance]:
        """获取服务实例"""
        try:
            # 遍历所有服务查找实例
            async for key in self._redis.scan_iter(f"{self._key_prefix}*"):
                if not key.endswith(f":{instance_id}"):
                    continue
                
                data = await self._redis.hgetall(key)
                if not data:
                    continue
                
                return ServiceInstance(
                    id=data["id"],
                    name=data["name"],
                    host=data["host"],
                    port=int(data["port"]),
                    metadata=json.loads(data["metadata"]),
                    health_check_url=data["health_check_url"] or None,
                    status=data["status"],
                    last_updated=datetime.fromisoformat(data["last_updated"])
                )
            return None
        except Exception as e:
            logger.error(f"Failed to get service instance: {str(e)}")
            return None

    async def get_instances(self, service_name: str) -> List[ServiceInstance]:
        """获取服务的所有实例"""
        try:
            instances = []
            service_key = f"{self._key_prefix}{service_name}"
            
            # 获取服务的所有实例ID
            instance_ids = await self._redis.smembers(service_key)
            
            # 获取每个实例的详细信息
            for instance_id in instance_ids:
                instance_key = f"{self._key_prefix}{service_name}:{instance_id}"
                data = await self._redis.hgetall(instance_key)
                if not data:
                    continue
                
                instances.append(ServiceInstance(
                    id=data["id"],
                    name=data["name"],
                    host=data["host"],
                    port=int(data["port"]),
                    metadata=json.loads(data["metadata"]),
                    health_check_url=data["health_check_url"] or None,
                    status=data["status"],
                    last_updated=datetime.fromisoformat(data["last_updated"])
                ))
            
            return instances
        except Exception as e:
            logger.error(f"Failed to get service instances: {str(e)}")
            return []

    async def update_status(
        self,
        instance_id: str,
        status: str
    ) -> bool:
        """更新服务状态"""
        try:
            instance = await self.get_instance(instance_id)
            if not instance:
                return False

            instance_key = f"{self._key_prefix}{instance.name}:{instance.id}"
            await self._redis.hset(instance_key, "status", status)
            return True
        except Exception as e:
            logger.error(f"Failed to update service status: {str(e)}")
            return False

registry = RedisServiceRegistry(settings.REDIS_URL) 