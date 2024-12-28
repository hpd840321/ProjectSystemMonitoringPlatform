from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Dict, Optional

class AuditAction(str, Enum):
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
    LOGIN = "login"
    LOGOUT = "logout"

@dataclass
class AuditLog:
    """审计日志聚合根"""
    id: str
    user_id: str
    action: AuditAction
    resource_type: str  # 资源类型(project/server/agent等)
    resource_id: Optional[str]  # 资源ID
    details: Dict  # 操作详情
    ip_address: str
    user_agent: str
    created_at: datetime 