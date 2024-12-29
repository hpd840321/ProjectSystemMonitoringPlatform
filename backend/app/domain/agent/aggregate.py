from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Dict, Optional

class AgentStatus(str, Enum):
    ONLINE = "online"
    OFFLINE = "offline"
    ERROR = "error"

class UpgradeTaskStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"

@dataclass
class Agent:
    """Agent聚合根"""
    id: str
    server_id: str
    version: str
    status: AgentStatus
    last_heartbeat: Optional[datetime]
    config: Dict
    created_at: datetime
    updated_at: datetime

@dataclass
class AgentVersion:
    """Agent版本聚合根"""
    id: str
    version: str
    file_path: str
    checksum: str
    description: Optional[str]
    is_latest: bool
    created_at: datetime
    updated_at: datetime

@dataclass
class UpgradeTask:
    """升级任务聚合根"""
    id: str
    agent_id: str
    from_version: str
    to_version: str
    status: UpgradeTaskStatus
    error: Optional[str]
    created_at: datetime
    updated_at: datetime 