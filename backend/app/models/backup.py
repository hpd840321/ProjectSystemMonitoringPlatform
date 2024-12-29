from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text, BigInteger
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.base_class import Base

class BackupConfig(Base):
    __tablename__ = "backup_configs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False, unique=True)
    type = Column(String(20), nullable=False)
    target_path = Column(Text, nullable=False)
    retention_count = Column(Integer, nullable=False, default=7)
    schedule = Column(String(50), nullable=False)
    enabled = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # 关联
    records = relationship("BackupRecord", back_populates="config")

class BackupRecord(Base):
    __tablename__ = "backup_records"

    id = Column(Integer, primary_key=True, index=True)
    config_id = Column(Integer, ForeignKey("backup_configs.id"))
    file_path = Column(Text, nullable=False)
    file_size = Column(BigInteger, nullable=False)
    status = Column(String(20), nullable=False)
    error_message = Column(Text)
    started_at = Column(DateTime, nullable=False)
    completed_at = Column(DateTime)
    created_at = Column(DateTime, server_default=func.now())

    # 关联
    config = relationship("BackupConfig", back_populates="records") 