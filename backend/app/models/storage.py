from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.base_class import Base

class StoragePolicy(Base):
    __tablename__ = "storage_policies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False, unique=True)
    data_type = Column(String(20), nullable=False)
    retention_days = Column(Integer, nullable=False)
    compression_enabled = Column(Boolean, nullable=False, default=False)
    compression_after_days = Column(Integer)
    backup_enabled = Column(Boolean, nullable=False, default=False)
    backup_schedule = Column(String(50))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # 关联
    executions = relationship("StoragePolicyExecution", back_populates="policy")

class StoragePolicyExecution(Base):
    __tablename__ = "storage_policy_executions"

    id = Column(Integer, primary_key=True, index=True)
    policy_id = Column(Integer, ForeignKey("storage_policies.id"))
    action_type = Column(String(20), nullable=False)
    status = Column(String(20), nullable=False)
    affected_rows = Column(Integer)
    error_message = Column(Text)
    started_at = Column(DateTime, nullable=False)
    completed_at = Column(DateTime)
    created_at = Column(DateTime, server_default=func.now())

    # 关联
    policy = relationship("StoragePolicy", back_populates="executions") 