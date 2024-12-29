from sqlalchemy import Column, Integer, String, DateTime, BigInteger, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base_class import Base

# 服务器和分组的多对多关系表
server_group_relation = Table(
    'server_group_relations',
    Base.metadata,
    Column('server_id', Integer, ForeignKey('servers.id')),
    Column('group_id', Integer, ForeignKey('server_groups.id')),
    Column('created_at', DateTime, server_default=func.now())
)

class Server(Base):
    __tablename__ = "servers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    hostname = Column(String(255), nullable=False)
    ip_address = Column(String(39), nullable=False)
    os_type = Column(String(50))
    os_version = Column(String(50))
    cpu_cores = Column(Integer)
    memory_size = Column(BigInteger)
    disk_size = Column(BigInteger)
    status = Column(String(20), nullable=False, default='inactive')
    agent_version = Column(String(50))
    last_seen_at = Column(DateTime)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # 关联服务器组
    groups = relationship("ServerGroup", secondary=server_group_relation, back_populates="servers")

class ServerGroup(Base):
    __tablename__ = "server_groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(String)
    created_at = Column(DateTime, server_default=func.now())

    # 关联服务器
    servers = relationship("Server", secondary=server_group_relation, back_populates="groups") 