from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Optional

@dataclass
class AgentRegisterDTO:
    """Agent注册DTO"""
    server_id: str
    hostname: str
    ip_address: str
    system_info: Dict
    version: str

@dataclass
class AgentDTO:
    """Agent DTO"""
    id: str
    server_id: str
    version: str
    status: str
    hostname: str
    ip_address: str
    system_info: Dict
    config: Dict
    last_heartbeat: datetime
    created_at: datetime

@dataclass
class AgentMetricsDTO:
    """Agent指标DTO"""
    cpu_usage: float
    memory_usage: float
    disk_usage: Dict[str, float]
    network_io: Dict[str, int]
    timestamp: datetime 