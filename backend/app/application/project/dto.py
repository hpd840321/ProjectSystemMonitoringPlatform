from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Optional, List
from app.domain.project.aggregate import Project, Server
from app.domain.project.value_objects import ProjectStatus, ServerStatus

@dataclass
class ProjectCreateDTO:
    """项目创建DTO"""
    name: str
    description: str
    max_servers: int = 10
    max_agents: int = 10

@dataclass
class ProjectDTO:
    """项目DTO"""
    id: str
    name: str
    description: str
    status: str
    server_count: int
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_domain(cls, project: Project) -> 'ProjectDTO':
        return cls(
            id=project.id,
            name=project.name,
            description=project.description,
            status=project.status.value,
            server_count=len(project.servers),
            created_at=project.created_at,
            updated_at=project.updated_at
        )

@dataclass
class ServerCreateDTO:
    """服务器创建DTO"""
    name: str
    host: str
    description: str

@dataclass
class ServerDTO:
    """服务器DTO"""
    id: str
    name: str
    host: str
    description: str
    status: str
    last_heartbeat: Optional[datetime]
    metrics: Optional[Dict]
    agent_id: Optional[str]

    @classmethod
    def from_domain(cls, server: Server) -> 'ServerDTO':
        metrics_data = None
        if server.metrics:
            metrics_data = {
                "cpu_usage": server.metrics.cpu_usage,
                "memory_usage": server.metrics.memory_usage,
                "disk_usage": server.metrics.disk_usage,
                "network_io": server.metrics.network_io,
                "timestamp": server.metrics.timestamp
            }
        
        return cls(
            id=server.id,
            name=server.name,
            host=server.host,
            description=server.description,
            status=server.status.value,
            last_heartbeat=server.last_heartbeat,
            metrics=metrics_data,
            agent_id=server.agent_id
        )

@dataclass
class ServerMetricsDTO:
    """服务器指标DTO"""
    cpu_usage: float
    memory_usage: float
    disk_usage: float
    network_io: Dict[str, float] 