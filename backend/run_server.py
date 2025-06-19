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

def check_port_available(port):
    """Verifica si un puerto está disponible"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('0.0.0.0', port))
            return True
    except OSError:
        return False

def find_available_port(start_port=8000, end_port=8010):
    """Encuentra un puerto disponible en el rango especificado"""
    for port in range(start_port, end_port + 1):
        if check_port_available(port):
            return port
    return None

def main():
    """Función principal para iniciar el servidor"""
    local_ip = get_local_ip()
    
    # Verificar si el puerto configurado está disponible
    target_port = settings.PORT
    if not check_port_available(target_port):
        print(f"⚠️  Puerto {target_port} está ocupado, buscando puerto alternativo...")
        alternative_port = find_available_port()
        if alternative_port:
            target_port = alternative_port
            print(f"✅ Usando puerto alternativo: {target_port}")
        else:
            print("❌ No se encontró ningún puerto disponible en el rango 8000-8010")
            sys.exit(1)
    
    # Verificar configuración
    print("🔧 Configuración del servidor:")
    print(f"   - Host configurado: {settings.HOST}")
    print(f"   - Puerto configurado: {settings.PORT}")
    print(f"   - Puerto a usar: {target_port}")
    print()
    
    print("🚀 Iniciando Signance System Backend")
    print("=" * 50)
    print(f"🌐 El backend será accesible en:")
    print(f"   - Localhost:  http://127.0.0.1:{target_port}")
    print(f"   - Red Local:  http://{local_ip}:{target_port}")
    print(f"   - Todas IPs:  http://0.0.0.0:{target_port}")
    print("=" * 50)
    print(f"📋 Endpoints importantes:")
    print(f"   - Health:     http://{local_ip}:{target_port}/health")
    print(f"   - API Docs:   http://{local_ip}:{target_port}/docs")
    print(f"   - Frontend:   http://{local_ip}:{target_port}/")
    print("=" * 50)
    print("📡 Para acceder desde otras computadoras:")
    print(f"   Usa la IP: {local_ip}")
    print("=" * 50)
    
    # Iniciar el servidor
    try:
        print(f"🚀 Iniciando servidor en {settings.HOST}:{target_port}...")
        uvicorn.run(
            "app.main:app",
            host=settings.HOST,
            port=target_port,
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
