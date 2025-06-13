"""
Media schemas for API validation
"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from enum import Enum
from fastapi import UploadFile


class MediaType(str, Enum):
    image = "image"
    video = "video"


class MediaBase(BaseModel):
    filename: str
    media_type: MediaType
    duration: int


class MediaCreate(MediaBase):
    pass  # El file se maneja por separado en el endpoint


class MediaRead(MediaBase):
    id: int
    filepath: str
    created_at: datetime
    file_url: Optional[str] = None
    served_filename: Optional[str] = None

    class Config:
        orm_mode = True


class MediaUpdate(BaseModel):
    duration: Optional[int] = None
    # No permitimos cambiar tipo o nombre de fichero
