from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from pydantic import BaseModel
from datetime import datetime

class ServiceInstance(BaseModel):
    """服务实例"""
    id: str
    name: str
    host: str
    port: int
    metadata: Dict[str, Any] = {}
    health_check_url: Optional[str] = None
    status: str = "UP"  # UP, DOWN, STARTING, OUT_OF_SERVICE
    last_updated: datetime = datetime.now()
    
    class Config:
        # 启用字段验证缓存
        validate_assignment = True
        # 允许额外字段
        extra = "allow"

class ServiceRegistry(ABC):
    """服务注册接口"""

    @abstractmethod
    async def register(self, instance: ServiceInstance) -> bool:
        """注册服务实例"""
        pass

    @abstractmethod
    async def deregister(self, instance_id: str) -> bool:
        """注销服务实例"""
        pass

    @abstractmethod
    async def renew(self, instance_id: str) -> bool:
        """续约服务实例"""
        pass

    @abstractmethod
    async def get_instance(self, instance_id: str) -> Optional[ServiceInstance]:
        """获取服务实例"""
        pass

    @abstractmethod
    async def get_instances(self, service_name: str) -> List[ServiceInstance]:
        """获取服务的所有实例"""
        pass

    @abstractmethod
    async def update_status(
        self,
        instance_id: str,
        status: str
    ) -> bool:
        """更新服务状态"""
        pass 
        self,
        instance_id: str,
        status: str
    ) -> bool:
        """更新服务状态"""
        pass 