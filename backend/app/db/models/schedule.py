# filepath: /Users/leonardoperezgomez/Desktop/Somos Voces/Signance System/backend/app/db/models/schedule.py
"""
Schedule model - Enhanced scheduling system
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON, Boolean, Date
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from enum import Enum

from app.db.database import Base


class ScheduleType(str, Enum):
    simple = "simple"      # Programación semanal simple
    advanced = "advanced"  # Programación avanzada con fechas específicas


class Schedule(Base):
    __tablename__ = "schedules"
    
    id = Column(Integer, primary_key=True, index=True)
    media_id = Column(Integer, ForeignKey("media.id"), nullable=True, index=True)  # Puede ser NULL si es para playlist
    playlist_id = Column(Integer, ForeignKey("playlists.id"), nullable=True, index=True)  # Puede ser NULL si es para media individual
    
    # Tipo de programación
    schedule_type = Column(String, nullable=False, default="simple")  # simple | advanced
    
    # Programación SIMPLE (semanal)
    is_all_day = Column(Boolean, default=False)  # Si es True, se reproduce todo el día
    daily_start = Column(String, nullable=True)  # HH:MM inicio (ej: "10:00")
    daily_end = Column(String, nullable=True)    # HH:MM fin (ej: "16:00")
    weekdays = Column(JSON, nullable=True)       # [0,1,2,3,4,5,6] donde 0=Lunes, 6=Domingo
    
    # Programación AVANZADA (fechas específicas)
    start_date = Column(Date, nullable=True)     # Fecha de inicio (ej: campaña de Halloween)
    end_date = Column(Date, nullable=True)       # Fecha de fin
    specific_times = Column(JSON, nullable=True) # Lista de fechas/horas específicas
    
    # Configuración adicional
    is_active = Column(Boolean, default=True)    # Para activar/desactivar schedule
    priority = Column(Integer, default=1)        # Prioridad para resolver conflictos
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    media = relationship("Media", back_populates="schedules")
    playlist = relationship("Playlist", back_populates="schedules")