from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Table
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.base_class import Base

# 角色-权限关联表
role_permissions = Table(
    'role_permissions',
    Base.metadata,
    Column('role_id', Integer, ForeignKey('roles.id'), primary_key=True),
    Column('permission_id', Integer, ForeignKey('permissions.id'), primary_key=True),
    Column('created_at', DateTime, server_default=func.now())
)

# 用户-角色关联表
user_roles = Table(
    'user_roles',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('role_id', Integer, ForeignKey('roles.id'), primary_key=True),
    Column('created_at', DateTime, server_default=func.now())
)

class Permission(Base):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(100), unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(String)
    module = Column(String(50), nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    # 关联
    roles = relationship(
        "Role",
        secondary=role_permissions,
        back_populates="permissions"
    )

class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(String)
    is_system = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # 关联
    permissions = relationship(
        "Permission",
        secondary=role_permissions,
        back_populates="roles"
    )
    users = relationship(
        "User",
        secondary=user_roles,
        back_populates="roles"
    ) 