from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Dict, Optional

class AgentStatus(str, Enum):
    ONLINE = "online"
    OFFLINE = "offline"
    ERROR = "error"

class AgentVersion(str, Enum):
    V1_0 = "1.0"
    V1_1 = "1.1"
    V2_0 = "2.0"

@dataclass
class Agent:
    """Agent聚合根"""
    id: str
    server_id: str
    version: AgentVersion
    status: AgentStatus
    hostname: str
    ip_address: str
    system_info: Dict  # 系统信息
    config: Dict  # Agent配置
    last_heartbeat: datetime
    created_at: datetime
    updated_at: datetime

@dataclass
class AgentMetrics:
    """Agent指标"""
    agent_id: str
    cpu_usage: float
    memory_usage: float
    disk_usage: Dict[str, float]
    network_io: Dict[str, int]
    timestamp: datetime 