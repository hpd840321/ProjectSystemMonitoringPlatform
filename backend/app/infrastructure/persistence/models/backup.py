from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from .base import Base

class BackupModel(Base):
    """备份记录模型"""
    __tablename__ = "backups"
    
    id = Column(String(36), primary_key=True)
    filename = Column(String(255), nullable=False)
    size = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False)
    created_by = Column(String(36), ForeignKey("users.id"), nullable=False)
    status = Column(String(20), nullable=False)
    error_message = Column(Text)
    backup_type = Column(String(20), nullable=False)
    metadata = Column(JSON)
    
    # 关联
    creator = relationship("UserModel", backref="backups")
    restores = relationship("BackupRestoreModel", back_populates="backup")

class BackupRestoreModel(Base):
    """备份恢复记录模型"""
    __tablename__ = "backup_restores"
    
    id = Column(String(36), primary_key=True)
    backup_id = Column(String(36), ForeignKey("backups.id"), nullable=False)
    restored_at = Column(DateTime, nullable=False)
    restored_by = Column(String(36), ForeignKey("users.id"), nullable=False)
    status = Column(String(20), nullable=False)
    error_message = Column(Text)
    
    # 关联
    backup = relationship("BackupModel", back_populates="restores")
    restorer = relationship("UserModel", backref="backup_restores") 