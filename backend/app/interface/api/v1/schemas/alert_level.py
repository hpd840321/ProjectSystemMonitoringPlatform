from datetime import datetime
from typing import Optional
from pydantic import BaseModel, constr, conint

class AlertLevelBase(BaseModel):
    name: constr(min_length=1, max_length=50)
    description: Optional[str] = None
    color: constr(regex=r'^#[0-9A-Fa-f]{6}$')  # 验证颜色格式 #RRGGBB
    priority: conint(ge=1)  # 优先级必须大于等于1

class AlertLevelCreate(AlertLevelBase):
    pass

class AlertLevelUpdate(AlertLevelBase):
    pass

class AlertLevelInDB(AlertLevelBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True 