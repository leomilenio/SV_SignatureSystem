#!/usr/bin/env python3
"""
Script de diagnóstico completo para el frontend Vue.js
Identifica problemas con el servicio de archivos estáticos desde FastAPI
"""

import os
import sys
import time
import requests
import subprocess
import threading
from pathlib import Path

# Importar configuración del proyecto
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))
from app.main import app, find_available_port
import uvicorn

class FrontendDiagnostic:
    def __init__(self):
        self.backend_port = None
        self.server_process = None
        self.backend_url = None
        
    def check_file_structure(self):
        """Verificar la estructura de archivos del frontend"""
        print("🔍 Verificando estructura de archivos frontend...")
        
        frontend_dist = os.path.join(os.path.dirname(__file__), "app", "frontend_dist")
        
        required_files = [
            "index.html",
            "js/app.638a7be9.js",
            "js/chunk-vendors.f8bbfc4f.js",
            "css/app.424adba7.css",
            "css/chunk-vendors.f67f1fba.css",
            "favicon.ico"
        ]
        
        print(f"📁 Directorio frontend: {frontend_dist}")
        print(f"   Existe: {'✅' if os.path.exists(frontend_dist) else '❌'}")
        
        all_exist = True
        for file_path in required_files:
            full_path = os.path.join(frontend_dist, file_path)
            exists = os.path.exists(full_path)
            if exists:
                size = os.path.getsize(full_path)
                print(f"   📄 {file_path}: ✅ ({size:,} bytes)")
            else:
                print(f"   📄 {file_path}: ❌ NO ENCONTRADO")
                all_exist = False
        
        return all_exist
    
    def check_index_html_content(self):
        """Analizar el contenido de index.html"""
        print("\n🔍 Analizando index.html...")
        
        frontend_dist = os.path.join(os.path.dirname(__file__), "app", "frontend_dist")
        index_path = os.path.join(frontend_dist, "index.html")
        
        if not os.path.exists(index_path):
            print("   ❌ index.html no encontrado")
            return False
        
        with open(index_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"   📏 Tamaño: {len(content):,} caracteres")
        
        # Verificar rutas de assets
        asset_paths = [
            '/js/chunk-vendors.f8bbfc4f.js',
            '/js/app.638a7be9.js',
            '/css/chunk-vendors.f67f1fba.css',
            '/css/app.424adba7.css',
            '/favicon.ico'
        ]
        
        print("   🔗 Referencias de assets:")
        for asset in asset_paths:
            if asset in content:
                print(f"      ✅ {asset}")
            else:
                print(f"      ❌ {asset} NO ENCONTRADO")
        
        # Verificar div#app
        if 'id="app"' in content:
            print("   ✅ div#app encontrado")
        else:
            print("   ❌ div#app NO encontrado")
        
        return True
    
    def start_backend_server(self):
        """Iniciar servidor backend en hilo separado"""
        print("\n🚀 Iniciando servidor backend...")
        
        self.backend_port = find_available_port(8000, 8010)
        if not self.backend_port:
            print("   ❌ No hay puertos disponibles")
            return False
        
        self.backend_url = f"http://localhost:{self.backend_port}"
        print(f"   🌐 Puerto: {self.backend_port}")
        print(f"   🔗 URL: {self.backend_url}")
        
        def run_server():
            uvicorn.run(
                app,
                host="0.0.0.0",
                port=self.backend_port,
                log_level="error"  # Reducir logs para diagnóstico
            )
        
        # Iniciar en hilo separado
        server_thread = threading.Thread(target=run_server, daemon=True)
        server_thread.start()
        
        # Esperar a que el servidor esté listo
        print("   ⏳ Esperando que el servidor esté listo...")
        for i in range(30):  # 30 segundos máximo
            try:
                response = requests.get(f"{self.backend_url}/health", timeout=1)
                if response.status_code == 200:
                    print(f"   ✅ Servidor listo en {i+1} segundos")
                    return True
            except:
                time.sleep(1)
        
        print("   ❌ El servidor no responde")
        return False
    
    def test_static_routes(self):
        """Probar todas las rutas estáticas"""
        print("\n🔍 Probando rutas estáticas...")
        
        test_routes = [
            "/",
            "/static/index.html",
            "/static/js/app.638a7be9.js",
            "/static/js/chunk-vendors.f8bbfc4f.js",
            "/static/css/app.424adba7.css",
            "/static/css/chunk-vendors.f67f1fba.css",
            "/static/favicon.ico"
        ]
        
        results = {}
        
        for route in test_routes:
            url = f"{self.backend_url}{route}"
            try:
                response = requests.get(url, timeout=5)
                content_type = response.headers.get('content-type', 'unknown')
                
                results[route] = {
                    'status': response.status_code,
                    'content_type': content_type,
                    'size': len(response.content),
                    'success': 200 <= response.status_code < 300
                }
                
                status_icon = "✅" if results[route]['success'] else "❌"
                print(f"   {status_icon} {route}: {response.status_code} ({content_type}) - {len(response.content):,} bytes")
                
            except Exception as e:
                results[route] = {
                    'status': 'ERROR',
                    'error': str(e),
                    'success': False
                }
                print(f"   ❌ {route}: ERROR - {e}")
        
        return results
    
    def test_spa_routes(self):
        """Probar rutas SPA (Single Page Application)"""
        print("\n🔍 Probando rutas SPA...")
        
        spa_routes = [
            "/admin",
            "/config", 
            "/login",
            "/dashboard",
            "/some-random-path"  # Debería servir index.html
        ]
        
        for route in spa_routes:
            url = f"{self.backend_url}{route}"
            try:
                response = requests.get(url, timeout=5)
                content_type = response.headers.get('content-type', 'unknown')
                
                # Para SPA, todas las rutas deberían devolver index.html
                is_html = 'text/html' in content_type
                status_icon = "✅" if response.status_code == 200 and is_html else "❌"
                
                print(f"   {status_icon} {route}: {response.status_code} ({content_type}) - {len(response.content):,} bytes")
                
                # Verificar que realmente es index.html
                if is_html and 'id="app"' in response.text:
                    print(f"      ✅ Contiene div#app (index.html válido)")
                elif is_html:
                    print(f"      ⚠️  Es HTML pero no contiene div#app")
                    
            except Exception as e:
                print(f"   ❌ {route}: ERROR - {e}")
    
    def test_browser_compatibility(self):
        """Simular solicitudes del navegador"""
        print("\n🔍 Simulando solicitudes del navegador...")
        
        # Headers típicos de un navegador
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Cache-Control': 'no-cache'
        }
        
        # Probar página principal
        try:
            response = requests.get(self.backend_url, headers=headers, timeout=10)
            print(f"   🌐 Página principal: {response.status_code}")
            
            if response.status_code == 200:
                content = response.text
                
                # Verificar elementos críticos
                checks = [
                    ('div#app', 'id="app"' in content),
                    ('Scripts JS', '/js/app.' in content and '/js/chunk-vendors.' in content),
                    ('CSS', '/css/app.' in content and '/css/chunk-vendors.' in content),
                    ('Favicon', '/favicon.ico' in content),
                    ('Meta viewport', 'viewport' in content),
                    ('Lang attribute', 'lang="es"' in content)
                ]
                
                for check_name, result in checks:
                    icon = "✅" if result else "❌"
                    print(f"      {icon} {check_name}")
                
                # Guardar HTML para inspección manual
                output_file = "/tmp/signance_frontend_test.html"
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"   💾 HTML guardado en: {output_file}")
                
            else:
                print(f"   ❌ Error de respuesta: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Error de conexión: {e}")
    
    def run_full_diagnostic(self):
        """Ejecutar diagnóstico completo"""
        print("🔬 DIAGNÓSTICO COMPLETO DEL FRONTEND SIGNANCE SYSTEM")
        print("=" * 60)
        
        # 1. Verificar estructura de archivos
        files_ok = self.check_file_structure()
        
        # 2. Analizar index.html
        html_ok = self.check_index_html_content()
        
        if not files_ok or not html_ok:
            print("\n❌ PROBLEMAS ENCONTRADOS EN ARCHIVOS")
            print("   Verifica que el build de Vue se haya completado correctamente")
            return False
        
        # 3. Iniciar servidor
        server_ok = self.start_backend_server()
        if not server_ok:
            print("\n❌ NO SE PUDO INICIAR EL SERVIDOR")
            return False
        
        # 4. Probar rutas estáticas
        static_results = self.test_static_routes()
        
        # 5. Probar rutas SPA
        self.test_spa_routes()
        
        # 6. Simular navegador
        self.test_browser_compatibility()
        
        # Resumen final
        print("\n" + "=" * 60)
        print("📊 RESUMEN DEL DIAGNÓSTICO")
        
        failed_static = [route for route, data in static_results.items() if not data.get('success', False)]
        
        if failed_static:
            print(f"❌ Rutas estáticas fallidas: {len(failed_static)}")
            for route in failed_static:
                print(f"   - {route}")
        else:
            print("✅ Todas las rutas estáticas funcionan")
        
        print(f"\n🌐 Para probar manualmente, visita: {self.backend_url}")
        print("🔧 Para detener, presiona Ctrl+C")
        
        # Mantener servidor corriendo para pruebas manuales
        try:
            print("\n⏳ Manteniendo servidor activo para pruebas manuales...")
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n👋 Diagnóstico completado")


if __name__ == "__main__":
    diagnostic = FrontendDiagnostic()
    diagnostic.run_full_diagnostic()
