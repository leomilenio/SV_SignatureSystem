#!/usr/bin/env python3
"""
Script de inicio para el backend de Signance System
Detecta automáticamente la IP local y inicia el servidor en todas las interfaces
"""

import uvicorn
import socket
import sys
import os
from app.config import settings

def get_local_ip():
    """Obtiene la IP local de la máquina"""
    try:
        # Conectar a un servidor remoto para obtener la IP local
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
        return local_ip
    except Exception:
        # Fallback a localhost si no se puede obtener la IP
        return "127.0.0.1"

def main():
    """Función principal para iniciar el servidor"""
    local_ip = get_local_ip()
    
    print("🚀 Iniciando Signance System Backend")
    print("=" * 50)
    print(f"🌐 El backend será accesible en:")
    print(f"   - Local:      http://127.0.0.1:{settings.PORT}")
    print(f"   - Red Local:  http://{local_ip}:{settings.PORT}")
    print(f"   - Todas IPs:  http://0.0.0.0:{settings.PORT}")
    print("=" * 50)
    print(f"📋 Endpoints importantes:")
    print(f"   - Health:     http://{local_ip}:{settings.PORT}/health")
    print(f"   - API Docs:   http://{local_ip}:{settings.PORT}/docs")
    print(f"   - Frontend:   http://{local_ip}:{settings.PORT}/")
    print("=" * 50)
    print("📡 Para acceder desde otras computadoras:")
    print(f"   Usa la IP: {local_ip}")
    print("=" * 50)
    
    # Iniciar el servidor
    try:
        uvicorn.run(
            "app.main:app",
            host=settings.HOST,
            port=settings.PORT,
            reload=True,
            reload_dirs=["app"],
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n👋 Servidor detenido por el usuario")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error al iniciar el servidor: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
