from pydantic import BaseModel, Field
from typing import Dict, Optional, List
from datetime import datetime
from .agent_metrics import MetricsQuery, MetricsResponse, HourlyMetricsResponse

class AgentRegisterRequest(BaseModel):
    """Agent注册请求"""
    version: str = Field(..., description="Agent版本")
    config: Dict = Field(..., description="Agent配置")

class AgentResponse(BaseModel):
    """Agent响应"""
    id: str
    server_id: str
    version: str
    status: str
    last_heartbeat: Optional[datetime]
    config: Dict
    created_at: datetime
    updated_at: datetime
    
    @classmethod
    def from_domain(cls, agent):
        return cls(
            id=agent.id,
            server_id=agent.server_id,
            version=agent.version,
            status=agent.status.value,
            last_heartbeat=agent.last_heartbeat,
            config=agent.config,
            created_at=agent.created_at,
            updated_at=agent.updated_at
        )

class AgentVersionCreate(BaseModel):
    """创建Agent版本请求"""
    version: str = Field(..., description="版本号")
    description: Optional[str] = Field(None, description="版本描述")
    is_latest: bool = Field(True, description="是否为最新版本")

class AgentVersionResponse(BaseModel):
    """Agent版本响应"""
    id: str
    version: str
    file_path: str
    checksum: str
    description: Optional[str]
    is_latest: bool
    created_at: datetime
    updated_at: datetime
    
    @classmethod
    def from_domain(cls, version):
        return cls(
            id=version.id,
            version=version.version,
            file_path=version.file_path,
            checksum=version.checksum,
            description=version.description,
            is_latest=version.is_latest,
            created_at=version.created_at,
            updated_at=version.updated_at
        )

class UpgradeTaskCreate(BaseModel):
    """创建升级任务请求"""
    to_version: str = Field(..., description="目标版本")

class UpgradeTaskResponse(BaseModel):
    """升级任务响应"""
    id: str
    agent_id: str
    from_version: str
    to_version: str
    status: str
    error: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    @classmethod
    def from_domain(cls, task):
        return cls(
            id=task.id,
            agent_id=task.agent_id,
            from_version=task.from_version,
            to_version=task.to_version,
            status=task.status.value,
            error=task.error,
            created_at=task.created_at,
            updated_at=task.updated_at
        ) 