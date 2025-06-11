"""
FastAPI main application
"""
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, RedirectResponse
from contextlib import asynccontextmanager
import os

from app.config import settings
from app.db import init_db, get_db
from sqlalchemy.orm import Session
from app.db.crud.user_crud import count_users
from app.db.crud import business_crud
from app.api.routers import auth, media, schedules, business, ws


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

# Serve frontend if built
FRONTEND_DIST = os.path.join(os.path.dirname(__file__), "../../frontend/dist")
if os.path.exists(os.path.join(FRONTEND_DIST, "index.html")):
    app.mount(
        "/static",
        StaticFiles(directory=os.path.join(FRONTEND_DIST, "assets")),
        name="static",
    )

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(media.router, prefix="/api/media", tags=["media"])
app.include_router(schedules.router, prefix="/api/schedules", tags=["schedules"])
app.include_router(business.router, prefix="/api/business", tags=["business"])
app.include_router(ws.router)


@app.get("/", include_in_schema=False)
async def root(db: Session = Depends(get_db)):
    """Serve SPA entry or redirect based on setup state"""
    if count_users(db) == 0:
        return RedirectResponse(url="/login")
    if not business_crud.business_exists(db):
        return RedirectResponse(url="/config")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "module": "auth"}


@app.get("/{full_path:path}", include_in_schema=False)
async def spa_router(full_path: str):
    index_file = os.path.join(FRONTEND_DIST, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {"detail": "Not Found"}
