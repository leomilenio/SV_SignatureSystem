# filepath: /Users/leonardoperezgomez/Desktop/Somos Voces/Signance System/backend/app/db/models/schedule.py
"""
Schedule model
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.database import Base


class Schedule(Base):
    __tablename__ = "schedules"
    
    id = Column(Integer, primary_key=True, index=True)
    media_id = Column(Integer, ForeignKey("media.id"), nullable=False, index=True)
    # Configuración genérica: desde-hasta diario o días específicos
    daily_start = Column(String, nullable=True)  # HH:MM inicio
    daily_end = Column(String, nullable=True)    # HH:MM fin
    weekdays = Column(JSON, nullable=True)       # [0=lun..6=dom]
    # Calendario avanzado: lista de datetimes explícitos  
    specific_times = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    media = relationship("Media", back_populates="schedules")