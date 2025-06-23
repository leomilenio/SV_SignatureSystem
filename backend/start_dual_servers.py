#!/usr/bin/env python3
"""
Script avanzado para iniciar backend (8000-8010) y frontend (8080-8090) en procesos separados
"""
import sys
import os
import socket
import subprocess
import threading
import time
import signal

# Agregar el directorio del proyecto al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def get_local_ip():
    """Obtiene la IP local de la máquina"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
        return local_ip
    except Exception:
        return "127.0.0.1"


def check_port_available(port):
    """Verifica si un puerto está disponible"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('0.0.0.0', port))
            return True
    except OSError:
        return False


def find_available_port(start_port, end_port):
    """Encuentra un puerto disponible en el rango especificado"""
    for port in range(start_port, end_port + 1):
        if check_port_available(port):
            return port
    return None


class ServerManager:
    def __init__(self):
        self.backend_process = None
        self.frontend_process = None
        self.backend_port = None
        self.frontend_port = None
        self.local_ip = get_local_ip()
        
    def start_backend(self):
        """Inicia el servidor backend"""
        print("🔧 Configurando backend...")
        
        # Encontrar puerto disponible para backend
        self.backend_port = find_available_port(8000, 8010)
        if not self.backend_port:
            print("❌ No hay puertos disponibles para el backend (8000-8010)")
            return False
        
        print(f"🚀 Iniciando backend en puerto {self.backend_port}")
        print(f"📡 Backend: http://0.0.0.0:{self.backend_port}")
        print(f"🌐 Red local: http://{self.local_ip}:{self.backend_port}")
        
        try:
            # Iniciar backend usando uvicorn
            cmd = [
                sys.executable, "-m", "uvicorn",
                "app.main:app",
                "--host", "0.0.0.0",
                "--port", str(self.backend_port),
                "--reload"
            ]
            
            self.backend_process = subprocess.Popen(
                cmd,
                cwd=os.path.dirname(os.path.abspath(__file__))
            )
            
            # Esperar un poco para verificar que inició correctamente
            time.sleep(2)
            if self.backend_process.poll() is None:
                print("✅ Backend iniciado correctamente")
                return True
            else:
                print("❌ Error: Backend no pudo iniciar")
                return False
                
        except Exception as e:
            print(f"❌ Error iniciando backend: {e}")
            return False
    
    def start_frontend(self):
        """Inicia el servidor frontend"""
        print("\n🔧 Configurando frontend...")
        
        # Encontrar puerto disponible para frontend
        self.frontend_port = find_available_port(8080, 8090)
        if not self.frontend_port:
            print("❌ No hay puertos disponibles para el frontend (8080-8090)")
            return False
        
        # Verificar si existe el directorio del frontend
        frontend_dist = os.path.join(os.path.dirname(__file__), "app", "frontend_dist")
        if not os.path.exists(os.path.join(frontend_dist, "index.html")):
            print(f"⚠️  Frontend no encontrado en: {frontend_dist}")
            print("💡 El frontend se servirá desde el backend integrado")
            return True  # No es un error crítico
        
        print(f"🎨 Iniciando frontend en puerto {self.frontend_port}")
        print(f"📱 Frontend: http://0.0.0.0:{self.frontend_port}")
        print(f"🌐 Red local: http://{self.local_ip}:{self.frontend_port}")
        
        try:
            # Iniciar servidor HTTP simple para el frontend
            cmd = [
                sys.executable, "-m", "http.server",
                str(self.frontend_port),
                "--bind", "0.0.0.0"
            ]
            
            self.frontend_process = subprocess.Popen(
                cmd,
                cwd=frontend_dist
            )
            
            time.sleep(1)
            if self.frontend_process.poll() is None:
                print("✅ Frontend iniciado correctamente")
                return True
            else:
                print("❌ Error: Frontend no pudo iniciar")
                return False
                
        except Exception as e:
            print(f"❌ Error iniciando frontend: {e}")
            return False
    
    def stop_servers(self):
        """Detiene ambos servidores"""
        print("\n🛑 Deteniendo servidores...")
        
        if self.backend_process:
            try:
                self.backend_process.terminate()
                self.backend_process.wait(timeout=5)
                print("✅ Backend detenido")
            except:
                self.backend_process.kill()
                print("🔨 Backend forzado a detenerse")
        
        if self.frontend_process:
            try:
                self.frontend_process.terminate()
                self.frontend_process.wait(timeout=5)
                print("✅ Frontend detenido")
            except:
                self.frontend_process.kill()
                print("🔨 Frontend forzado a detenerse")
    
    def print_summary(self):
        """Imprime un resumen de los servidores"""
        print("\n" + "=" * 60)
        print("🎯 SIGNANCE SYSTEM - SERVIDORES ACTIVOS")
        print("=" * 60)
        
        if self.backend_port:
            print(f"🔧 BACKEND (API):")
            print(f"   - Puerto: {self.backend_port}")
            print(f"   - Local:  http://127.0.0.1:{self.backend_port}")
            print(f"   - Red:    http://{self.local_ip}:{self.backend_port}")
            print(f"   - Docs:   http://{self.local_ip}:{self.backend_port}/docs")
        
        if self.frontend_port:
            print(f"\n🎨 FRONTEND:")
            print(f"   - Puerto: {self.frontend_port}")
            print(f"   - Local:  http://127.0.0.1:{self.frontend_port}")
            print(f"   - Red:    http://{self.local_ip}:{self.frontend_port}")
        else:
            print(f"\n🎨 FRONTEND (integrado en backend):")
            print(f"   - URL:    http://{self.local_ip}:{self.backend_port}")
        
        print("\n💡 Para acceder desde otras computadoras, usa la IP de red")
        print("🛑 Presiona Ctrl+C para detener ambos servidores")
        print("=" * 60)


def main():
    """Función principal"""
    print("🎯 Iniciando Signance System completo...")
    
    server_manager = ServerManager()
    
    def signal_handler(signum, frame):
        print("\n👋 Deteniendo servidores...")
        server_manager.stop_servers()
        sys.exit(0)
    
    # Configurar manejo de señales
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        # Iniciar backend
        if not server_manager.start_backend():
            print("❌ No se pudo iniciar el backend")
            sys.exit(1)
        
        # Iniciar frontend (opcional)
        server_manager.start_frontend()
        
        # Mostrar resumen
        server_manager.print_summary()
        
        # Mantener el script activo
        while True:
            time.sleep(1)
            
            # Verificar que el backend siga ejecutándose
            if server_manager.backend_process and server_manager.backend_process.poll() is not None:
                print("❌ El backend se detuvo inesperadamente")
                break
                
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"❌ Error general: {e}")
    finally:
        server_manager.stop_servers()


if __name__ == "__main__":
    main()
