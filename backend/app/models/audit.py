from sqlalchemy import Column, Integer, String, DateTime, JSON, Text, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.base_class import Base

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    username = Column(String(50))  # 冗余存储，方便查询
    action = Column(String(50), nullable=False)
    resource_type = Column(String(50), nullable=False)
    resource_id = Column(String(100))
    status = Column(String(20), nullable=False)
    ip_address = Column(String(50))
    user_agent = Column(String(200))
    details = Column(JSON)
    error_message = Column(Text)
    created_at = Column(DateTime, server_default=func.now(), index=True)

    # 关联
    user = relationship("User", back_populates="audit_logs") 