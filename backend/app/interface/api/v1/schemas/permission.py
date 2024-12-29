from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, constr

class PermissionBase(BaseModel):
    code: constr(min_length=1, max_length=100)
    name: constr(min_length=1, max_length=100)
    description: Optional[str] = None
    module: constr(min_length=1, max_length=50)

class PermissionCreate(PermissionBase):
    pass

class PermissionUpdate(PermissionBase):
    pass

class PermissionInDB(PermissionBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class RoleBase(BaseModel):
    name: constr(min_length=1, max_length=50)
    description: Optional[str] = None
    is_system: bool = False

class RoleCreate(RoleBase):
    permission_ids: List[int]

class RoleUpdate(RoleBase):
    permission_ids: List[int]

class RoleInDB(RoleBase):
    id: int
    created_at: datetime
    updated_at: datetime
    permissions: List[PermissionInDB]

    class Config:
        orm_mode = True

class UserRoleUpdate(BaseModel):
    role_ids: List[int] 