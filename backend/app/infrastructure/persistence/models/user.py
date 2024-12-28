from datetime import datetime
from sqlalchemy import Column, String, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship

from ..database import Base
from app.domain.user.aggregate import UserRole

class UserModel(Base):
    """用户数据库模型"""
    __tablename__ = "users"

    id = Column(String(36), primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)
    status = Column(String(20), nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

class ProjectMemberModel(Base):
    """项目成员数据库模型"""
    __tablename__ = "project_members"

    project_id = Column(String(36), ForeignKey("projects.id"), primary_key=True)
    user_id = Column(String(36), ForeignKey("users.id"), primary_key=True)
    role = Column(Enum(UserRole), nullable=False)
    joined_at = Column(DateTime, nullable=False)

    # 关联关系
    user = relationship("UserModel")
    project = relationship("ProjectModel") 