from dataclasses import dataclass
from datetime import datetime
from app.domain.user.aggregate import User, ProjectMember, UserRole
from pydantic import BaseModel, EmailStr, constr, validator
from typing import Optional

@dataclass
class UserLoginDTO:
    """用户登录DTO"""
    username: str
    password: str

@dataclass
class UserDTO:
    """用户DTO"""
    id: str
    username: str
    email: str
    status: str
    created_at: datetime

    @classmethod
    def from_domain(cls, user: User) -> 'UserDTO':
        return cls(
            id=user.id,
            username=user.username,
            email=user.email,
            status=user.status,
            created_at=user.created_at
        )

@dataclass
class AddMemberDTO:
    """添加成员DTO"""
    user_id: str
    role: str

@dataclass
class ProjectMemberDTO:
    """项目成员DTO"""
    user_id: str
    project_id: str
    role: str
    joined_at: datetime

    @classmethod
    def from_domain(cls, member: ProjectMember) -> 'ProjectMemberDTO':
        return cls(
            user_id=member.user_id,
            project_id=member.project_id,
            role=member.role.value,
            joined_at=member.joined_at
        )

@dataclass
class UserCreateDTO:
    """创建用户DTO"""
    username: str
    email: str
    password: str

@dataclass
class TokenDTO:
    """令牌DTO"""
    access_token: str
    token_type: str 

class UserRegisterDTO(BaseModel):
    """用户注册DTO"""
    username: constr(min_length=3, max_length=20, pattern=r'^[a-zA-Z0-9_-]+$')
    email: EmailStr
    password: constr(min_length=8)
    confirm_password: str
    tenant_id: Optional[str]
    captcha: constr(min_length=4, max_length=4)

    @validator('confirm_password')
    def passwords_match(cls, v, values):
        if 'password' in values and v != values['password']:
            raise ValueError('密码不匹配')
        return v

    @validator('password')
    def password_strength(cls, v):
        if not any(c.isupper() for c in v):
            raise ValueError('密码必须包含大写字母')
        if not any(c.islower() for c in v):
            raise ValueError('密码必须包含小写字母')
        if not any(c.isdigit() for c in v):
            raise ValueError('密码必须包含数字')
        return v 