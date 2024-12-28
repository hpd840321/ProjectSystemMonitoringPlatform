from abc import ABC, abstractmethod
from typing import List
from datetime import datetime
from .aggregate import AuditLog

class AuditLogRepository(ABC):
    """审计日志仓储接口"""
    
    @abstractmethod
    async def save(self, log: AuditLog) -> None:
        """保存审计日志"""
        pass
    
    @abstractmethod
    async def list_by_user(
        self,
        user_id: str,
        start_time: datetime,
        end_time: datetime,
        limit: int = 100,
        offset: int = 0
    ) -> List[AuditLog]:
        """获取用户审计日志"""
        pass
    
    @abstractmethod
    async def list_by_resource(
        self,
        resource_type: str,
        resource_id: str,
        limit: int = 100,
        offset: int = 0
    ) -> List[AuditLog]:
        """获取资源审计日志"""
        pass
    
    @abstractmethod
    async def cleanup_old_logs(self, threshold: datetime) -> None:
        """清理过期日志"""
        pass 