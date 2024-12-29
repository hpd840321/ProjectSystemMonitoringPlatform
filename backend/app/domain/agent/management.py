from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Dict, Optional

class AgentStatus(str, Enum):
    ONLINE = "online"
    OFFLINE = "offline"
    UPDATING = "updating"

class UpdateTaskStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"

@dataclass
class AgentVersion:
    id: str
    version: str
    description: Optional[str]
    package_url: str
    checksum: str
    is_latest: bool
    created_at: datetime
    updated_at: datetime

@dataclass
class AgentStatusInfo:
    agent_id: str
    server_id: str
    version: str
    status: AgentStatus
    last_heartbeat: datetime
    system_info: Optional[Dict]
    metrics: Optional[Dict]
    error: Optional[str]
    created_at: datetime
    updated_at: datetime

@dataclass
class AgentUpdateTask:
    id: str
    agent_id: str
    from_version: str
    to_version: str
    status: UpdateTaskStatus
    error: Optional[str]
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime 