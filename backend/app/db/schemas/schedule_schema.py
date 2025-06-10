"""
Schedule schemas for API validation
"""
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional


class ScheduleBase(BaseModel):
    media_id: int
    daily_start: Optional[str] = None
    daily_end: Optional[str] = None
    weekdays: Optional[List[int]] = None
    specific_times: Optional[List[datetime]] = None


class ScheduleCreate(ScheduleBase):
    pass


class ScheduleRead(ScheduleBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class ScheduleUpdate(BaseModel):
    daily_start: Optional[str] = None
    daily_end: Optional[str] = None
    weekdays: Optional[List[int]] = None
    specific_times: Optional[List[datetime]] = None
