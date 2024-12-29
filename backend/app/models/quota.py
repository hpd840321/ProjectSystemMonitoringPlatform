from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.db.base_class import Base

class ProjectQuota(Base):
    __tablename__ = "project_quotas"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    resource_type = Column(String(50), nullable=False)
    quota_limit = Column(Integer, nullable=False)
    used_amount = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

class ResourceUsage(Base):
    __tablename__ = "resource_usage"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    resource_type = Column(String(50), nullable=False)
    amount = Column(Integer, nullable=False)
    operation = Column(String(20), nullable=False)
    created_at = Column(DateTime, server_default=func.now()) 