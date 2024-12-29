from datetime import datetime
from typing import Optional
from pydantic import BaseModel, IPvAnyAddress

class ServerBase(BaseModel):
    name: str
    hostname: str
    ip_address: IPvAnyAddress
    os_type: Optional[str] = None
    os_version: Optional[str] = None
    cpu_cores: Optional[int] = None
    memory_size: Optional[int] = None
    disk_size: Optional[int] = None
    agent_version: Optional[str] = None

class ServerCreate(ServerBase):
    pass

class ServerUpdate(ServerBase):
    status: Optional[str] = None
    last_seen_at: Optional[datetime] = None

class ServerInDB(ServerBase):
    id: int
    status: str
    last_seen_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class ServerGroupBase(BaseModel):
    name: str
    description: Optional[str] = None

class ServerGroupCreate(ServerGroupBase):
    pass

class ServerGroupInDB(ServerGroupBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True 