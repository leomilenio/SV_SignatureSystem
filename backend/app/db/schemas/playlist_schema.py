"""
Playlist schemas for API validation
"""
from pydantic import BaseModel, validator
from datetime import datetime
from typing import Optional, List


class PlaylistBase(BaseModel):
    name: str
    description: Optional[str] = None

    @validator('name')
    def name_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('El nombre de la playlist no puede estar vacío')
        return v.strip()


class PlaylistCreate(PlaylistBase):
    pass


class PlaylistRead(PlaylistBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    media_count: Optional[int] = 0  # Número de medias en la playlist
    total_duration: Optional[int] = 0  # Duración total en segundos

    class Config:
        orm_mode = True


class PlaylistUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

    @validator('name')
    def name_must_not_be_empty(cls, v):
        if v is not None and not v.strip():
            raise ValueError('El nombre de la playlist no puede estar vacío')
        return v.strip() if v else v


class PlaylistStats(BaseModel):
    total_playlists: int
    total_scheduled_items: int
