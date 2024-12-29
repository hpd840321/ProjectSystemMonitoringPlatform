from datetime import datetime
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, constr

class PluginBase(BaseModel):
    name: constr(min_length=1, max_length=100)
    version: constr(min_length=1, max_length=20)
    description: Optional[str] = None
    author: Optional[str] = None
    settings: Optional[Dict[str, Any]] = None

class PluginCreate(PluginBase):
    id: constr(min_length=1, max_length=50)

class PluginUpdate(BaseModel):
    settings: Optional[Dict[str, Any]] = None
    enabled: Optional[bool] = None

class PluginInDB(PluginBase):
    id: str
    enabled: bool
    installed_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class PluginStatus(BaseModel):
    id: str
    enabled: bool
    health: bool
    error: Optional[str] = None 