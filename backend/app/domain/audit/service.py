from datetime import datetime
from typing import Dict, Optional, List
from uuid import uuid4
from .repository import AuditLogRepository
from .aggregate import AuditLog, AuditAction

class AuditService:
    """审计日志服务"""
    
    def __init__(self, audit_repo: AuditLogRepository):
        self.audit_repo = audit_repo
    
    async def log_action(
        self,
        user_id: str,
        action: AuditAction,
        resource_type: str,
        resource_id: Optional[str],
        details: Dict,
        ip_address: str,
        user_agent: str
    ) -> None:
        """记录审计日志"""
        log = AuditLog(
            id=str(uuid4()),
            user_id=user_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            details=details,
            ip_address=ip_address,
            user_agent=user_agent,
            created_at=datetime.now()
        )
        await self.audit_repo.save(log)
    
    async def get_user_logs(
        self,
        user_id: str,
        start_time: datetime,
        end_time: datetime,
        limit: int = 100,
        offset: int = 0
    ) -> List[AuditLog]:
        """获取用户审计日志"""
        return await self.audit_repo.list_by_user(
            user_id,
            start_time,
            end_time,
            limit,
            offset
        )
    
    async def get_resource_logs(
        self,
        resource_type: str,
        resource_id: str,
        limit: int = 100,
        offset: int = 0
    ) -> List[AuditLog]:
        """获取资源审计日志"""
        return await self.audit_repo.list_by_resource(
            resource_type,
            resource_id,
            limit,
            offset
        ) 