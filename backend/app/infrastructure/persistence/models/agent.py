from datetime import datetime
from sqlalchemy import Column, String, Float, JSON, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base

class AgentModel(Base):
    """Agent数据库模型"""
    __tablename__ = "agents"
    
    id = Column(String(36), primary_key=True)
    server_id = Column(String(36), ForeignKey("servers.id", ondelete="CASCADE"))
    version = Column(String(10), nullable=False)
    status = Column(String(20), nullable=False)
    hostname = Column(String(255), nullable=False)
    ip_address = Column(String(45), nullable=False)
    system_info = Column(JSON, nullable=False)
    config = Column(JSON, nullable=False)
    last_heartbeat = Column(DateTime, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    
    server = relationship("ServerModel", back_populates="agents")
    metrics = relationship("AgentMetricsModel", back_populates="agent")

class AgentMetricsModel(Base):
    """Agent指标数据库模型"""
    __tablename__ = "agent_metrics"
    
    agent_id = Column(String(36), ForeignKey("agents.id", ondelete="CASCADE"))
    cpu_usage = Column(Float, nullable=False)
    memory_usage = Column(Float, nullable=False)
    disk_usage = Column(JSON, nullable=False)
    network_io = Column(JSON, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    
    agent = relationship("AgentModel", back_populates="metrics") 