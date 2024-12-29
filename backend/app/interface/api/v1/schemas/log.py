from datetime import datetime
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, constr, validator

class LogSourceBase(BaseModel):
    name: constr(min_length=1, max_length=50)
    type: constr(regex='^(file|syslog|journald)$')
    config: Dict[str, Any]
    enabled: bool = True

    @validator('config')
    def validate_config(cls, v, values):
        source_type = values.get('type')
        if source_type == 'file':
            required = {'path', 'format'}
            if not all(k in v for k in required):
                raise ValueError(f'File source config must contain: {required}')
        elif source_type == 'syslog':
            required = {'port', 'protocol'}
            if not all(k in v for k in required):
                raise ValueError(f'Syslog source config must contain: {required}')
        elif source_type == 'journald':
            required = {'unit'}
            if not all(k in v for k in required):
                raise ValueError(f'Journald source config must contain: {required}')
        return v

class LogSourceCreate(LogSourceBase):
    pass

class LogSourceUpdate(LogSourceBase):
    pass

class LogSourceInDB(LogSourceBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class LogParseRuleBase(BaseModel):
    name: constr(min_length=1, max_length=50)
    pattern: str
    fields: Dict[str, str]
    sample: Optional[str] = None
    enabled: bool = True

class LogParseRuleCreate(LogParseRuleBase):
    pass

class LogParseRuleUpdate(LogParseRuleBase):
    pass

class LogParseRuleInDB(LogParseRuleBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class LogEntry(BaseModel):
    source_id: int
    timestamp: datetime
    level: Optional[str]
    message: str
    parsed_fields: Optional[Dict[str, Any]]
    metadata: Optional[Dict[str, Any]]

class LogQuery(BaseModel):
    start_time: Optional[datetime]
    end_time: Optional[datetime]
    source_ids: Optional[List[int]]
    levels: Optional[List[str]]
    search_text: Optional[str]
    field_filters: Optional[Dict[str, Any]]
    limit: int = 100
    offset: int = 0 