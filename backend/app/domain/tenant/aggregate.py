from dataclasses import dataclass
from datetime import datetime

@dataclass
class Tenant:
    """租户聚合根"""
    id: str
    name: str
    status: TenantStatus
    quota: TenantQuota  # 租户级别的资源配额
    created_at: datetime
    updated_at: datetime 