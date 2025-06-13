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


class PlaylistMediaCreate(PlaylistMediaBase):
    pass


class PlaylistMediaRead(PlaylistMediaBase):
    id: int
    added_at: datetime

    class Config:
        orm_mode = True


class PlaylistMediaUpdate(BaseModel):
    order_index: Optional[int] = None


# Para operaciones bulk
class PlaylistAddMediaRequest(BaseModel):
    media_ids: List[int]


class PlaylistReorderRequest(BaseModel):
    media_orders: List[dict]  # [{"media_id": 1, "order_index": 0}, ...]
