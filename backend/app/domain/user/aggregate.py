from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import List

class UserRole(str, Enum):
    ADMIN = "admin"
    MEMBER = "member"
    VIEWER = "viewer"

@dataclass
class User:
    """用户聚合根"""
    id: str
    username: str
    email: str
    password_hash: str
    status: str
    created_at: datetime
    updated_at: datetime

@dataclass
class ProjectMember:
    """项目成员值对象"""
    user_id: str
    project_id: str
    role: UserRole
    joined_at: datetime 