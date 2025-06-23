"""
FastAPI main application
"""
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, RedirectResponse
from contextlib import asynccontextmanager
import os
import socket
import uvicorn

from app.config import settings
from app.db import init_db, get_db
from sqlalchemy.orm import Session
from app.db.crud.user_crud import count_users
from app.db.crud import business_crud
from app.api.routers import auth, media, schedules, business, ws, playlists, player


def check_port_available(port):
    """Verifica si un puerto está disponible"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('0.0.0.0', port))
            return True
    except OSError:
        return False


def find_available_port(start_port=8000, end_port=8010):
    """Encuentra un puerto disponible en el rango especificado para backend"""
    for port in range(start_port, end_port + 1):
        if check_port_available(port):
            return port
    return None


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    init_db()
    
    yield
    # Shutdown
    pass


# Crear directorio de uploads ANTES de montar archivos estáticos
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)


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

# Serve frontend from static directory
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(os.path.join(STATIC_DIR, "index.html")):
    # Montar archivos estáticos del frontend (CSS, JS, imágenes, etc.)
    app.mount("/css", StaticFiles(directory=os.path.join(STATIC_DIR, "css")), name="css")
    app.mount("/js", StaticFiles(directory=os.path.join(STATIC_DIR, "js")), name="js")
    app.mount("/fonts", StaticFiles(directory=os.path.join(STATIC_DIR, "fonts")), name="fonts")
    
    # También montar toda la carpeta static para archivos no específicos
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
    
    print(f"✅ Frontend servido desde: {STATIC_DIR}")
    print(f"   📁 Archivos estáticos disponibles desde raíz")
else:
    print(f"⚠️  Frontend no encontrado en: {STATIC_DIR}")

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(media.router, prefix="/api/media", tags=["media"])
app.include_router(schedules.router, prefix="/api/schedules", tags=["schedules"])
app.include_router(playlists.router, prefix="/api/playlists", tags=["playlists"])
app.include_router(business.router, prefix="/api/business", tags=["business"])
app.include_router(player.router, prefix="/api", tags=["player-public"])  # Endpoints públicos del player
app.include_router(ws.router)


@app.get("/health")
async def health_check():
    return {"status": "healthy", "module": "auth"}

@app.get("/api/health")
async def api_health_check():
    return {"status": "healthy", "module": "api"}


@app.get("/", include_in_schema=False)
async def root(db: Session = Depends(get_db)):
    """Serve SPA entry or redirect based on setup state"""
    if count_users(db) == 0:
        return RedirectResponse(url="/login")
    if not business_crud.business_exists(db):
        return RedirectResponse(url="/config")
    
    # Servir el frontend si existe
    index_file = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {"detail": "Frontend not built"}


@app.get("/{full_path:path}", include_in_schema=False)
async def spa_router(full_path: str):
    """Catch-all para rutas del frontend - debe ir AL FINAL"""
    # Evitar interferir con rutas de API y archivos estáticos
    if (full_path.startswith("api/") or 
        full_path.startswith("uploads/") or 
        full_path.startswith("static/") or
        full_path == "health"):
        raise HTTPException(status_code=404, detail="Not found")
    
    index_file = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {"detail": "Not Found"}


def start_server_with_dynamic_port():
    """Inicia el servidor backend con puerto dinámico"""
    # Encontrar puerto disponible para el backend
    backend_port = find_available_port(8000, 8010)
    
    if not backend_port:
        print("❌ No hay puertos disponibles en el rango 8000-8010")
        return
    
    print(f"🚀 Iniciando servidor backend en puerto {backend_port}")
    print(f"� Backend disponible en: http://0.0.0.0:{backend_port}")
    print(f"🌐 Acceso desde red local: http://[tu-ip]:{backend_port}")
    
    # Iniciar servidor con uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=backend_port,
        reload=True,
        log_level="info"
    )


if __name__ == "__main__":
    start_server_with_dynamic_port()
