#!/usr/bin/env python3
"""
Script simple para iniciar el backend (8000-8010) con frontend integrado
Usa la misma lógica que run_server.py pero con frontend integrado
"""
import sys
import os

# Agregar el directorio del proyecto al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Importar directamente la función main de run_server
from run_server import main as run_backend

if __name__ == "__main__":
    print("🎯 Iniciando Signance System con frontend integrado...")
    print("📡 Backend: puertos 8000-8010")
    print("🎨 Frontend: servido desde /static/")
    print("✅ Estructura simplificada: app/static/")
    print("✅ Assets en: /static/js/, /static/css/, /static/fonts/")
    print("✅ Player API disponible en: /api/player/")
    print("=" * 50)
    
    # Ejecutar el backend que ya incluye el frontend
    run_backend()
