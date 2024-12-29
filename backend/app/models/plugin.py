from sqlalchemy import Column, String, Boolean, JSON, DateTime
from sqlalchemy.sql import func

from app.db.base_class import Base

class Plugin(Base):
    __tablename__ = "plugins"

    id = Column(String(50), primary_key=True)
    name = Column(String(100), nullable=False)
    version = Column(String(20), nullable=False)
    description = Column(String(500))
    author = Column(String(100))
    enabled = Column(Boolean, default=False)
    settings = Column(JSON)
    installed_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now()) 