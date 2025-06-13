# filepath: /Users/leonardoperezgomez/Desktop/Somos Voces/Signance System/backend/app/db/models/media.py
"""
Media model
"""
from sqlalchemy import Column, Integer, String, DateTime, Enum as SQLEnum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from enum import Enum

from app.db.database import Base


class MediaType(str, Enum):
    image = "image"
    video = "video"


class Media(Base):
    __tablename__ = "media"
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False, index=True)
    filepath = Column(String, nullable=False)  # Almacenado en /media/uploads
    media_type = Column(SQLEnum(MediaType), nullable=False)
    duration = Column(Integer, nullable=False)  # Segundos de reproducción
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    schedules = relationship("Schedule", back_populates="media", cascade="all, delete-orphan")
    playlist_media = relationship("PlaylistMedia", back_populates="media", cascade="all, delete-orphan")