from datetime import datetime
from sqlalchemy import Column, String, DateTime, Integer, Enum, ForeignKey, JSON
from sqlalchemy.orm import relationship

from ..database import Base
from app.domain.project.value_objects import ProjectStatus, ServerStatus

class ProjectModel(Base):
    """项目数据库模型"""
    __tablename__ = "projects"

    id = Column(String(36), primary_key=True)
    tenant_id = Column(String(36), ForeignKey("tenants.id"), nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(String(500))
    status = Column(Enum(ProjectStatus), nullable=False)
    max_servers = Column(Integer, nullable=False, default=10)
    max_agents = Column(Integer, nullable=False, default=10)
    config = Column(JSON)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

    # 关联关系
    servers = relationship("ServerModel", back_populates="project")

class ServerModel(Base):
    """服务器数据库模型"""
    __tablename__ = "servers"

    id = Column(String(36), primary_key=True)
    project_id = Column(String(36), ForeignKey("projects.id"), nullable=False)
    name = Column(String(100), nullable=False)
    host = Column(String(200), nullable=False)
    description = Column(String(500))
    status = Column(Enum(ServerStatus), nullable=False)
    agent_id = Column(String(36))
    last_heartbeat = Column(DateTime)
    metrics = Column(JSON)

    # 关联关系
    project = relationship("ProjectModel", back_populates="servers") 