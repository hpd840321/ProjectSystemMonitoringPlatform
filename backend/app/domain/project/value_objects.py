from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import List, Dict

class ProjectStatus(Enum):
    """项目状态"""
    ACTIVE = "active"         # 运行中
    MAINTAINING = "maintaining"  # 维护中
    SUSPENDED = "suspended"   # 已暂停
    ARCHIVED = "archived"     # 已归档

class ServerStatus(Enum):
    """服务器状态"""
    ONLINE = "online"         # 在线
    OFFLINE = "offline"       # 离线
    WARNING = "warning"       # 警告
    ERROR = "error"          # 错误

class ResourceQuota:
    """资源配额"""
    def __init__(self, max_servers: int, max_agents: int):
        self.max_servers = max_servers
        self.max_agents = max_agents

    def check_server_quota(self, current_count: int) -> bool:
        return current_count < self.max_servers

@dataclass(frozen=True)
class ServerMetrics:
    """服务器指标"""
    cpu_usage: float
    memory_usage: float
    disk_usage: float
    network_io: Dict[str, float]
    timestamp: datetime 