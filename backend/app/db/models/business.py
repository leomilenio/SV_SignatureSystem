# filepath: /Users/leonardoperezgomez/Desktop/Somos Voces/Signance System/backend/app/db/models/business.py
"""
Business model
"""
from sqlalchemy import Column, Integer, String, DateTime, LargeBinary
from sqlalchemy.sql import func

from app.db.database import Base


class Business(Base):
    __tablename__ = "businesses"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    logo = Column(LargeBinary, nullable=True)  # Logo almacenado como BLOB
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())