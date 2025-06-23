#!/usr/bin/env python3
"""
Script de verificación rápida del sistema Signance
Verifica que backend y frontend funcionen correctamente
"""

import os
import sys
import time
import requests
import threading
import webbrowser

# Importar configuración del proyecto
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))
from app.main import app, find_available_port
import uvicorn

def quick_health_check():
    """Verificación rápida de salud del sistema"""
    print("🔍 VERIFICACIÓN RÁPIDA DEL SISTEMA SIGNANCE")
    print("=" * 50)
    
    # 1. Verificar archivos críticos
    print("📁 Verificando archivos críticos...")
    
    frontend_dist = os.path.join(os.path.dirname(__file__), "app", "frontend_dist")
    critical_files = [
        "app/frontend_dist/index.html",
        "app/frontend_dist/js/app.638a7be9.js",
        "app/frontend_dist/css/app.424adba7.css",
        "app/main.py",
        "app/config.py"
    ]
    
    all_files_ok = True
    for file_path in critical_files:
        full_path = os.path.join(os.path.dirname(__file__), file_path)
        if os.path.exists(full_path):
            size = os.path.getsize(full_path)
            print(f"   ✅ {file_path} ({size:,} bytes)")
        else:
            print(f"   ❌ {file_path} - NO ENCONTRADO")
            all_files_ok = False
    
    if not all_files_ok:
        print("\n❌ ARCHIVOS FALTANTES - Sistema no puede funcionar")
        return False
    
    # 2. Iniciar servidor de prueba
    print("\n🚀 Iniciando servidor de prueba...")
    
    backend_port = find_available_port(8000, 8010)
    if not backend_port:
        print("❌ No hay puertos disponibles")
        return False
    
    backend_url = f"http://localhost:{backend_port}"
    print(f"🌐 URL de prueba: {backend_url}")
    
    def run_test_server():
        uvicorn.run(app, host="0.0.0.0", port=backend_port, log_level="error")
    
    # Iniciar servidor en hilo separado
    server_thread = threading.Thread(target=run_test_server, daemon=True)
    server_thread.start()
    
    # Esperar que esté listo
    print("⏳ Esperando servidor...")
    server_ready = False
    for i in range(10):
        try:
            response = requests.get(f"{backend_url}/health", timeout=1)
            if response.status_code == 200:
                server_ready = True
                break
        except:
            time.sleep(1)
    
    if not server_ready:
        print("❌ Servidor no responde")
        return False
    
    print("✅ Servidor listo")
    
    # 3. Probar endpoints críticos
    print("\n🔍 Probando endpoints críticos...")
    
    test_endpoints = [
        ("/health", "API Health"),
        ("/", "Frontend Principal"),
        ("/js/app.638a7be9.js", "JavaScript Principal"),
        ("/css/app.424adba7.css", "CSS Principal"),
        ("/api/playlists/public", "API Playlists")
    ]
    
    all_endpoints_ok = True
    for endpoint, description in test_endpoints:
        try:
            response = requests.get(f"{backend_url}{endpoint}", timeout=3)
            if response.status_code == 200:
                print(f"   ✅ {description}: {response.status_code}")
            else:
                print(f"   ⚠️  {description}: {response.status_code}")
                if endpoint in ["/", "/js/app.638a7be9.js"]:  # Críticos
                    all_endpoints_ok = False
        except Exception as e:
            print(f"   ❌ {description}: ERROR")
            if endpoint in ["/health", "/"]:  # Muy críticos
                all_endpoints_ok = False
    
    # 4. Resultado final
    print("\n" + "=" * 50)
    if all_endpoints_ok:
        print("🎉 ¡SISTEMA FUNCIONANDO CORRECTAMENTE!")
        print(f"🌐 Abre: {backend_url}")
        print("🔧 Para usar, ejecuta: python start_with_frontend.py")
        
        # Abrir navegador automáticamente
        try:
            webbrowser.open(backend_url)
            print("🚀 Navegador abierto automáticamente")
        except:
            pass
        
        # Mantener servidor 30 segundos para pruebas
        print("\n⏳ Manteniendo servidor 30 segundos para pruebas...")
        time.sleep(30)
        
        return True
    else:
        print("❌ PROBLEMAS DETECTADOS EN EL SISTEMA")
        return False

if __name__ == "__main__":
    success = quick_health_check()
    if success:
        print("👋 Verificación completada exitosamente")
    else:
        print("🔧 Se requiere revisión del sistema")
        sys.exit(1)
