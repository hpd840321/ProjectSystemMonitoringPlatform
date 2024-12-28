from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Optional
from uuid import uuid4

from .value_objects import ProjectStatus, ServerStatus, ResourceQuota, ServerMetrics
from .exceptions import QuotaExceededError, ServerNotFoundError

@dataclass
class Project:
    """项目聚合根"""
    id: str
    name: str
    description: str
    tenant_id: str
    status: ProjectStatus
    quota: ResourceQuota
    created_at: datetime
    updated_at: datetime
    servers: List['Server'] = field(default_factory=list)
    config: Dict = field(default_factory=dict)

    @classmethod
    def create(cls, name: str, description: str, quota: ResourceQuota) -> 'Project':
        """创建新项目"""
        now = datetime.now()
        return cls(
            id=str(uuid4()),
            name=name,
            description=description,
            status=ProjectStatus.ACTIVE,
            quota=quota,
            created_at=now,
            updated_at=now
        )

    def add_server(self, server: 'Server') -> None:
        """添加服务器"""
        if not self.quota.check_server_quota(len(self.servers)):
            raise QuotaExceededError("Server quota exceeded")
        self.servers.append(server)
        self.updated_at = datetime.now()

    def remove_server(self, server_id: str) -> None:
        """移除服务器"""
        self.servers = [s for s in self.servers if s.id != server_id]
        self.updated_at = datetime.now()

    def get_server(self, server_id: str) -> Optional['Server']:
        """获取服务器"""
        return next((s for s in self.servers if s.id == server_id), None)

    def update_status(self, status: ProjectStatus) -> None:
        """更新项目状态"""
        self.status = status
        self.updated_at = datetime.now()

@dataclass
class Server:
    """服务器实体"""
    id: str
    name: str
    host: str
    description: str
    status: ServerStatus
    last_heartbeat: Optional[datetime]
    metrics: Optional[ServerMetrics] = None
    agent_id: Optional[str] = None

    @classmethod
    def create(cls, name: str, host: str, description: str) -> 'Server':
        """创建新服务器"""
        return cls(
            id=str(uuid4()),
            name=name,
            host=host,
            description=description,
            status=ServerStatus.OFFLINE,
            last_heartbeat=None
        )

    def update_metrics(self, metrics: ServerMetrics) -> None:
        """更新服务器指标"""
        self.metrics = metrics
        self.last_heartbeat = datetime.now()
        self._update_status_from_metrics()

    def bind_agent(self, agent_id: str) -> None:
        """绑定Agent"""
        self.agent_id = agent_id
        self.status = ServerStatus.ONLINE
        self.last_heartbeat = datetime.now()

    def _update_status_from_metrics(self) -> None:
        """根据指标更新状态"""
        if not self.metrics:
            return

        if self.metrics.cpu_usage > 90 or self.metrics.memory_usage > 90:
            self.status = ServerStatus.WARNING
        elif self.metrics.cpu_usage > 95 or self.metrics.memory_usage > 95:
            self.status = ServerStatus.ERROR
        else:
            self.status = ServerStatus.ONLINE 