from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, JSON, Text, BigInteger
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.base_class import Base

class LogSource(Base):
    __tablename__ = "log_sources"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False, unique=True)
    type = Column(String(20), nullable=False)
    config = Column(JSON, nullable=False)
    enabled = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # 关联
    parse_rules = relationship("LogParseRule", secondary="log_source_rules")
    logs = relationship("Log", back_populates="source")

class LogParseRule(Base):
    __tablename__ = "log_parse_rules"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False, unique=True)
    pattern = Column(Text, nullable=False)
    fields = Column(JSON, nullable=False)
    sample = Column(Text)
    enabled = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # 关联
    sources = relationship("LogSource", secondary="log_source_rules")

class LogSourceRule(Base):
    __tablename__ = "log_source_rules"

    source_id = Column(Integer, ForeignKey("log_sources.id"), primary_key=True)
    rule_id = Column(Integer, ForeignKey("log_parse_rules.id"), primary_key=True)
    priority = Column(Integer, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

class Log(Base):
    __tablename__ = "logs"

    id = Column(BigInteger, primary_key=True, index=True)
    source_id = Column(Integer, ForeignKey("log_sources.id"))
    timestamp = Column(DateTime, nullable=False)
    level = Column(String(20))
    message = Column(Text, nullable=False)
    parsed_fields = Column(JSON)
    metadata = Column(JSON)
    created_at = Column(DateTime, server_default=func.now())

    # 关联
    source = relationship("LogSource", back_populates="logs") 