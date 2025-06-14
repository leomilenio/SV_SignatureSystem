"""
PlaylistMedia schemas for API validation
"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


class PlaylistMediaBase(BaseModel):
    playlist_id: int
    media_id: int
    order_index: int = 0
    duration: Optional[int] = None  # Duración específica en esta playlist (segundos), None = usar duración original del media


class PlaylistMediaCreate(PlaylistMediaBase):
    pass


class PlaylistMediaRead(PlaylistMediaBase):
    id: int
    added_at: datetime

    class Config:
        orm_mode = True


class PlaylistMediaUpdate(BaseModel):
    order_index: Optional[int] = None
    duration: Optional[int] = None


# Para operaciones bulk
class PlaylistAddMediaRequest(BaseModel):
    media_ids: List[int]


# Para agregar un solo medio
class PlaylistAddSingleMediaRequest(BaseModel):
    media_id: int
    duration: Optional[int] = None  # Duración específica para este medio en esta playlist


class PlaylistReorderRequest(BaseModel):
    media_orders: List[dict]  # [{"media_id": 1, "order_index": 0}, ...]
