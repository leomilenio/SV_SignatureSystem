"""
PlaylistMedia model - Many-to-many relationship between Playlist and Media
"""
from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.database import Base


class PlaylistMedia(Base):
    __tablename__ = "playlist_media"
    
    id = Column(Integer, primary_key=True, index=True)
    playlist_id = Column(Integer, ForeignKey("playlists.id"), nullable=False, index=True)
    media_id = Column(Integer, ForeignKey("media.id"), nullable=False, index=True)
    order_index = Column(Integer, nullable=False, default=0)  # Orden dentro de la playlist
    added_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    playlist = relationship("Playlist", back_populates="playlist_media")
    media = relationship("Media", back_populates="playlist_media")
