#!/usr/bin/env python3
"""
Diagnóstico de problemas entre modo dev y build de producción
Identifica diferencias en la carga de MediaManager y PlayerView
"""

import os
import sys
import time
import requests
import threading
import json
from pathlib import Path

# Importar configuración del proyecto
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))
from app.main import app, find_available_port
import uvicorn

class DevVsBuildDiagnostic:
    def __init__(self):
        self.backend_port = None
        self.backend_url = None
        
    def start_backend(self):
        """Iniciar servidor backend"""
        print("🚀 Iniciando servidor backend...")
        
        self.backend_port = find_available_port(8000, 8010)
        if not self.backend_port:
            print("❌ No hay puertos disponibles")
            return False
        
        self.backend_url = f"http://localhost:{self.backend_port}"
        print(f"🌐 Backend URL: {self.backend_url}")
        
        def run_server():
            uvicorn.run(app, host="0.0.0.0", port=self.backend_port, log_level="error")
        
        server_thread = threading.Thread(target=run_server, daemon=True)
        server_thread.start()
        
        # Esperar que esté listo
        print("⏳ Esperando backend...")
        for i in range(15):
            try:
                response = requests.get(f"{self.backend_url}/health", timeout=1)
                if response.status_code == 200:
                    print(f"✅ Backend listo en {i+1} segundos")
                    return True
            except:
                time.sleep(1)
        
        print("❌ Backend no responde")
        return False
    
    def test_player_endpoints(self):
        """Probar endpoints específicos del player"""
        print("\n🎬 Probando endpoints del player...")
        
        player_endpoints = [
            ("/api/health", "Health Check"),
            ("/api/playlists/public", "Playlists Públicas (Player)"),
            ("/api/player/playlists", "Player API - Playlists"),
            ("/api/player/media", "Player API - Media"),
            ("/api/playlists", "Playlists Admin (requiere auth)")
        ]
        
        results = {}
        
        for endpoint, description in player_endpoints:
            url = f"{self.backend_url}{endpoint}"
            try:
                response = requests.get(url, timeout=5)
                
                results[endpoint] = {
                    'status': response.status_code,
                    'success': response.status_code in [200, 401, 422],  # 401/422 son OK para endpoints protegidos
                    'content_type': response.headers.get('content-type', ''),
                    'size': len(response.content),
                    'data': response.text[:200] if response.status_code == 200 else None
                }
                
                icon = "✅" if results[endpoint]['success'] else "❌"
                print(f"   {icon} {description}: {response.status_code}")
                
                if response.status_code == 200 and endpoint.endswith('/public'):
                    try:
                        data = response.json()
                        if isinstance(data, list):
                            print(f"      📊 {len(data)} playlists encontradas")
                    except:
                        pass
                        
            except Exception as e:
                results[endpoint] = {
                    'status': 'ERROR',
                    'success': False,
                    'error': str(e)
                }
                print(f"   ❌ {description}: ERROR - {e}")
        
        return results
    
    def test_frontend_build_vs_dev(self):
        """Comparar frontend build vs dev"""
        print("\n🌐 Analizando frontend build vs dev...")
        
        # 1. Verificar archivos del build
        static_dir = os.path.join(os.path.dirname(__file__), "app", "static")
        
        if not os.path.exists(static_dir):
            print("❌ Directorio static no existe")
            return False
        
        print(f"📁 Directorio static: {static_dir}")
        
        # 2. Verificar index.html
        index_path = os.path.join(static_dir, "index.html")
        if os.path.exists(index_path):
            with open(index_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            print(f"   📄 index.html: {len(content)} bytes")
            
            # Buscar referencias de API
            api_refs = []
            if 'localhost:8080' in content:
                api_refs.append("❌ Referencias hardcodeadas a localhost:8080")
            if 'localhost:8000' in content:
                api_refs.append("⚠️  Referencias hardcodeadas a localhost:8000")
            if '/api/' in content:
                api_refs.append("ℹ️  Referencias a /api/ encontradas")
            
            for ref in api_refs:
                print(f"      {ref}")
        
        # 3. Verificar JavaScript principal
        js_files = []
        js_dir = os.path.join(static_dir, "js")
        if os.path.exists(js_dir):
            js_files = [f for f in os.listdir(js_dir) if f.endswith('.js') and not f.endswith('.map')]
            print(f"   📜 Archivos JS: {len(js_files)}")
            
            # Verificar app.js principal
            app_js = [f for f in js_files if f.startswith('app.')]
            if app_js:
                app_js_path = os.path.join(js_dir, app_js[0])
                with open(app_js_path, 'r', encoding='utf-8') as f:
                    js_content = f.read()
                
                print(f"   📦 {app_js[0]}: {len(js_content):,} bytes")
                
                # Buscar problemas comunes
                issues = []
                if 'localhost:8080' in js_content:
                    issues.append("❌ Hardcoded localhost:8080 en JS")
                if 'console.log' in js_content:
                    count = js_content.count('console.log')
                    issues.append(f"ℹ️  {count} console.log statements")
                if 'baseURL' in js_content:
                    issues.append("ℹ️  Configuración baseURL encontrada")
                
                for issue in issues:
                    print(f"      {issue}")
        
        return True
    
    def test_browser_simulation(self):
        """Simular carga del navegador desde /static/"""
        print("\n🌐 Simulando carga del navegador desde /static/...")
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8'
        }
        
        # 1. Cargar página principal (como sería desde /static/)
        try:
            response = requests.get(self.backend_url, headers=headers, timeout=10)
            print(f"   📄 Página principal: {response.status_code} ({len(response.content)} bytes)")
            
            if response.status_code == 200:
                content = response.text
                
                # Extraer recursos referenciados
                import re
                js_files = re.findall(r'src="(/static/js/[^"]+)"', content)
                css_files = re.findall(r'href="(/static/css/[^"]+)"', content)
                
                print(f"   📜 Scripts encontrados: {len(js_files)}")
                print(f"   🎨 CSS encontrados: {len(css_files)}")
                
                # Probar carga de cada recurso
                all_resources_ok = True
                
                for js_file in js_files[:2]:  # Probar primeros 2
                    url = f"{self.backend_url}{js_file}"
                    try:
                        js_response = requests.get(url, timeout=5)
                        icon = "✅" if js_response.status_code == 200 else "❌"
                        print(f"      {icon} {js_file}: {js_response.status_code}")
                        if js_response.status_code != 200:
                            all_resources_ok = False
                    except Exception as e:
                        print(f"      ❌ {js_file}: ERROR - {e}")
                        all_resources_ok = False
                
                for css_file in css_files[:2]:  # Probar primeros 2
                    url = f"{self.backend_url}{css_file}"
                    try:
                        css_response = requests.get(url, timeout=5)
                        icon = "✅" if css_response.status_code == 200 else "❌"
                        print(f"      {icon} {css_file}: {css_response.status_code}")
                        if css_response.status_code != 200:
                            all_resources_ok = False
                    except Exception as e:
                        print(f"      ❌ {css_file}: ERROR - {e}")
                        all_resources_ok = False
                
                return all_resources_ok
            else:
                print(f"   ❌ Error cargando página principal: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"   ❌ Error en simulación: {e}")
            return False
    
    def analyze_api_detection_context(self):
        """Analizar contexto para detección de API"""
        print("\n🔍 Analizando contexto de detección de API...")
        
        # Simular contexto de dev vs producción
        print("   📊 Contexto de desarrollo (npm run serve):")
        print("      🌐 Frontend URL: http://localhost:8080")
        print("      🔗 Backend URL: http://localhost:8000-8010 (auto-detectado)")
        print("      ✅ CORS configurado para development")
        print("      ✅ Proxy dev server puede manejar requests")
        
        print("\n   📊 Contexto de producción (/static/):")
        print(f"      🌐 Frontend URL: {self.backend_url}")
        print(f"      🔗 Backend URL: {self.backend_url}/api (mismo dominio)")
        print("      ✅ Sin problemas de CORS (mismo origen)")
        print("      ⚠️  JavaScript debe detectar baseURL correctamente")
        
        # Verificar si el contexto de detección es diferente
        print("\n   🔍 Posibles problemas:")
        print("      1. baseURL detection: window.location.hostname cambió")
        print("      2. API initialization: timing diferente en build vs dev")
        print("      3. Asset loading: rutas relativas vs absolutas")
        print("      4. Backend detection: caché puede estar interfiriendo")
        
        return True
    
    def run_diagnosis(self):
        """Ejecutar diagnóstico completo"""
        print("🔬 DIAGNÓSTICO: DEV vs BUILD PRODUCCIÓN")
        print("=" * 60)
        
        # 1. Iniciar backend
        if not self.start_backend():
            return False
        
        # 2. Probar endpoints del player
        player_results = self.test_player_endpoints()
        
        # 3. Analizar frontend build
        frontend_ok = self.test_frontend_build_vs_dev()
        
        # 4. Simular navegador
        browser_ok = self.test_browser_simulation()
        
        # 5. Analizar contexto de detección
        self.analyze_api_detection_context()
        
        # Resumen final
        print("\n" + "=" * 60)
        print("📊 RESUMEN DEL DIAGNÓSTICO")
        
        # Verificar endpoints críticos del player
        critical_endpoints = ['/api/playlists/public', '/api/player/playlists']
        player_endpoints_ok = all(
            player_results.get(ep, {}).get('success', False) 
            for ep in critical_endpoints
        )
        
        print(f"✅ Endpoints del player: {'OK' if player_endpoints_ok else 'FALLÓ'}")
        print(f"✅ Frontend build: {'OK' if frontend_ok else 'FALLÓ'}")
        print(f"✅ Carga de recursos: {'OK' if browser_ok else 'FALLÓ'}")
        
        if not player_endpoints_ok:
            print("\n❌ PROBLEMA DETECTADO: Endpoints del player no funcionan")
            print("   Solución: Verificar que player.router esté incluido en main.py")
        
        if not browser_ok:
            print("\n❌ PROBLEMA DETECTADO: Recursos no cargan correctamente")
            print("   Solución: Verificar rutas en index.html y montaje /static/")
        
        # Recomendaciones específicas
        print("\n🔧 RECOMENDACIONES:")
        print("1. Verificar que backendDetector use window.location.origin")
        print("2. Confirmar que API endpoints respondan desde mismo dominio")
        print("3. Revisar console.log del navegador para errores de JS")
        print("4. Probar clearing localStorage/cache del navegador")
        
        print(f"\n🌐 Para probar manualmente: {self.backend_url}")
        print("🔧 Presiona Ctrl+C para detener")
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n👋 Diagnóstico completado")

if __name__ == "__main__":
    diagnostic = DevVsBuildDiagnostic()
    diagnostic.run_diagnosis()
