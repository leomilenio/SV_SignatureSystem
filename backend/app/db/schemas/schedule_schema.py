"""
Schedule schemas for API validation - Enhanced scheduling system
"""
from pydantic import BaseModel, validator, root_validator
from datetime import datetime, date
from typing import Optional, List
from enum import Enum


class ScheduleType(str, Enum):
    simple = "simple"
    advanced = "advanced"


class ScheduleBase(BaseModel):
    media_id: Optional[int] = None
    playlist_id: Optional[int] = None
    schedule_type: ScheduleType = ScheduleType.simple
    
    # Simple scheduling
    is_all_day: bool = False
    daily_start: Optional[str] = None  # "HH:MM"
    daily_end: Optional[str] = None    # "HH:MM"
    weekdays: Optional[List[int]] = None  # [0,1,2,3,4,5,6]
    
    # Advanced scheduling
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    specific_times: Optional[List[str]] = None  # ["2024-10-31T10:00:00", ...]
    
    # Configuration
    is_active: bool = True
    priority: int = 1

    @root_validator
    def validate_target(cls, values):
        media_id = values.get('media_id')
        playlist_id = values.get('playlist_id')
        
        # Debe tener al menos uno
        if not media_id and not playlist_id:
            raise ValueError('Debe especificar media_id o playlist_id')
        
        # No puede tener ambos
        if media_id and playlist_id:
            raise ValueError('No puede especificar media_id y playlist_id al mismo tiempo')
        
        return values


class ScheduleCreate(ScheduleBase):
    pass


class ScheduleRead(ScheduleBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True


class ScheduleUpdate(BaseModel):
    schedule_type: Optional[ScheduleType] = None
    is_all_day: Optional[bool] = None
    daily_start: Optional[str] = None
    daily_end: Optional[str] = None
    weekdays: Optional[List[int]] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    specific_times: Optional[List[str]] = None
    is_active: Optional[bool] = None
    priority: Optional[int] = None
