"""
FastAPI main application
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import os

from app.config import settings
from app.db import init_db
from app.api.routers import auth, media, schedules, business


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    init_db()
    
    # Create upload directory
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    
    yield
    # Shutdown
    pass


app = FastAPI(
    title="Signance System API",
    description="Sistema de gestión de contenido digital",
    version="1.0.0",
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files
app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(media.router, prefix="/api/media", tags=["media"])
app.include_router(schedules.router, prefix="/api/schedules", tags=["schedules"])
app.include_router(business.router, prefix="/api/business", tags=["business"])


@app.get("/")
async def root():
    return {"message": "Signance System API - Authentication Module"}


@app.get("/health")
async def health_check():
    return {"status": "healthy", "module": "auth"}