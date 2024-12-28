from dataclasses import dataclass
from datetime import datetime
from app.domain.user.aggregate import User, ProjectMember, UserRole

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