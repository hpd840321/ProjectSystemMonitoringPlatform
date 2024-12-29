from sqlalchemy import Column, Integer, String, DateTime, Boolean, JSON, Text, ForeignKey, ARRAY
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.base_class import Base

class NotificationChannel(Base):
    __tablename__ = "notification_channels"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    type = Column(String(20), nullable=False)
    config = Column(JSON, nullable=False)
    enabled = Column(Boolean, nullable=False, default=True)
    description = Column(Text)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # 关联
    logs = relationship("NotificationLog", back_populates="channel")

class NotificationTemplate(Base):
    __tablename__ = "notification_templates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    type = Column(String(20), nullable=False)
    subject_template = Column(Text, nullable=False)
    content_template = Column(Text, nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # 关联
    logs = relationship("NotificationLog", back_populates="template")

class NotificationLog(Base):
    __tablename__ = "notification_logs"

    id = Column(Integer, primary_key=True, index=True)
    channel_id = Column(Integer, ForeignKey("notification_channels.id"))
    template_id = Column(Integer, ForeignKey("notification_templates.id"))
    event_type = Column(String(50), nullable=False)
    recipients = Column(ARRAY(String))
    subject = Column(Text, nullable=False)
    content = Column(Text, nullable=False)
    status = Column(String(20), nullable=False)
    error_message = Column(Text)
    created_at = Column(DateTime, server_default=func.now())

    # 关联
    channel = relationship("NotificationChannel", back_populates="logs")
    template = relationship("NotificationTemplate", back_populates="logs") 