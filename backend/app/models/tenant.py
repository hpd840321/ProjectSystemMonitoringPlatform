from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey, Table
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.base_class import Base

class Tenant(Base):
    __tablename__ = "tenants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    code = Column(String(50), unique=True, nullable=False)
    status = Column(String(20), nullable=False, default="active")
    max_users = Column(Integer)
    max_projects = Column(Integer)
    max_servers = Column(Integer)
    settings = Column(JSON)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # 关联
    users = relationship(
        "User",
        secondary="user_tenants",
        back_populates="tenants"
    )
    projects = relationship("Project", back_populates="tenant")
    servers = relationship("Server", back_populates="tenant")
    alert_rules = relationship("AlertRule", back_populates="tenant")
    backup_configs = relationship("BackupConfig", back_populates="tenant")
    notification_channels = relationship("NotificationChannel", back_populates="tenant")

class UserTenant(Base):
    __tablename__ = "user_tenants"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), primary_key=True)
    role = Column(String(50), nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    # 关联
    user = relationship("User", back_populates="tenant_roles")
    tenant = relationship("Tenant", back_populates="user_roles") 