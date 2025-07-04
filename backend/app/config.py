"""
Configuration settings
"""
import os
from typing import List
from pydantic import BaseSettings


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "sqlite:///./signance.db"
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production-9876543210abcdef"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    
    # CORS - Permitir acceso desde cualquier IP de la red local
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",
        "http://localhost:8080",
        "http://127.0.0.1:8080",
        "http://localhost:8002",
        "http://127.0.0.1:8002",
        "*"  # Permite todos los orígenes para acceso desde red local
    ]
    
    # Network configuration - FORZAR ESCUCHA EN TODAS LAS INTERFACES
    HOST: str = "0.0.0.0"  # Escuchar en todas las interfaces de red (OBLIGATORIO para acceso remoto)
    PORT: int = 8000  # Puerto preferido cambiado a 8000
    
    # Media
    UPLOAD_DIR: str = "media/uploads"
    MAX_FILE_SIZE: int = 100 * 1024 * 1024  # 100MB
    ALLOWED_EXTENSIONS: List[str] = [".mp4", ".avi", ".mov", ".jpg", ".jpeg", ".png", ".gif"]
    
    class Config:
        env_file = ".env"


settings = Settings()
