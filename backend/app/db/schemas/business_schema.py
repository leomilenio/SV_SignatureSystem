"""
Business schemas for API validation
"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class BusinessBase(BaseModel):
    name: str


class BusinessCreate(BusinessBase):
    logo: Optional[bytes] = None


class BusinessRead(BusinessBase):
    id: int
    updated_at: datetime

    class Config:
        orm_mode = True


class BusinessUpdate(BaseModel):
    name: Optional[str] = None
    logo: Optional[bytes] = None
