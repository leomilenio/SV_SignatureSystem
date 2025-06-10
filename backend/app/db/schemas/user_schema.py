"""
User schemas for validation
"""
from typing import Optional
from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    password: str


class UserInDB(BaseModel):
    id: int
    username: str
    hashed_password: str
    role: str
    
    class Config:
        orm_mode = True


class UserResponse(BaseModel):
    id: int
    username: str
    role: str
    
    class Config:
        orm_mode = True
