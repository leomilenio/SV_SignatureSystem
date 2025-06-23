#!/usr/bin/env python3
"""
Script de automatización para build y despliegue del frontend de Signance System.

Este script automatiza el proceso de compilación del frontend (Vue.js) y 
la copia de archivos estáticos al backend para el despliegue en producción.

Uso:
    python build_and_deploy_frontend.py
    
El script:
1. Ejecuta 'npm run build' en la carpeta frontend
2. Copia todos los archivos generados a la carpeta static del backend
3. Proporciona retroalimentación detallada del proceso
"""

import os
import sys
import subprocess
import shutil
import time
from pathlib import Path


class FrontendBuilder:
    def __init__(self):
        # Detectar la ruta base del proyecto (donde está el backend)
        self.script_dir = Path(__file__).parent.absolute()
        self.backend_dir = self.script_dir
        self.project_root = self.backend_dir.parent
        self.frontend_dir = self.project_root / "frontend"
        self.static_dir = self.backend_dir / "app" / "static"
        self.dist_dir = self.frontend_dir / "dist"
        
        # Configuración de colores para output
        self.GREEN = '\033[92m'
        self.RED = '\033[91m'
        self.YELLOW = '\033[93m'
        self.BLUE = '\033[94m'
        self.ENDC = '\033[0m'
        self.BOLD = '\033[1m'
    
    def print_colored(self, message, color=""):
        """Imprime un mensaje con color."""
        print(f"{color}{message}{self.ENDC}")
    
    def print_step(self, step_number, message):
        """Imprime el paso actual del proceso."""
        self.print_colored(f"\n{self.BOLD}[PASO {step_number}]{self.ENDC} {message}")
    
    def print_success(self, message):
        """Imprime un mensaje de éxito."""
        self.print_colored(f"✅ {message}", self.GREEN)
    
    def print_error(self, message):
        """Imprime un mensaje de error."""
        self.print_colored(f"❌ {message}", self.RED)
    
    def print_warning(self, message):
        """Imprime un mensaje de advertencia."""
        self.print_colored(f"⚠️  {message}", self.YELLOW)
    
    def print_info(self, message):
        """Imprime un mensaje informativo."""
        self.print_colored(f"ℹ️  {message}", self.BLUE)
    
    def check_directories(self):
        """Verifica que las rutas necesarias existan."""
        self.print_step(1, "Verificando estructura de directorios...")
        
        if not self.frontend_dir.exists():
            self.print_error(f"No se encontró la carpeta frontend en: {self.frontend_dir}")
            return False
        
        if not (self.frontend_dir / "package.json").exists():
            self.print_error(f"No se encontró package.json en: {self.frontend_dir}")
            return False
        
        if not self.static_dir.exists():
            self.print_warning(f"Carpeta static no existe, se creará: {self.static_dir}")
            self.static_dir.mkdir(parents=True, exist_ok=True)
        
        self.print_success("Estructura de directorios verificada")
        self.print_info(f"Frontend: {self.frontend_dir}")
        self.print_info(f"Backend static: {self.static_dir}")
        return True
    
    def check_npm(self):
        """Verifica que npm esté disponible."""
        try:
            result = subprocess.run(
                ["npm", "--version"], 
                capture_output=True, 
                text=True, 
                cwd=self.frontend_dir
            )
            if result.returncode == 0:
                self.print_success(f"npm disponible (versión: {result.stdout.strip()})")
                return True
            else:
                self.print_error("npm no está disponible")
                return False
        except FileNotFoundError:
            self.print_error("npm no encontrado. Instale Node.js y npm primero.")
            return False
    
    def install_dependencies(self):
        """Instala las dependencias de npm si es necesario."""
        node_modules = self.frontend_dir / "node_modules"
        
        if not node_modules.exists():
            self.print_step(2, "Instalando dependencias de npm...")
            try:
                result = subprocess.run(
                    ["npm", "install"],
                    cwd=self.frontend_dir,
                    capture_output=True,
                    text=True
                )
                
                if result.returncode == 0:
                    self.print_success("Dependencias instaladas correctamente")
                    return True
                else:
                    self.print_error(f"Error instalando dependencias: {result.stderr}")
                    return False
            except Exception as e:
                self.print_error(f"Error ejecutando npm install: {e}")
                return False
        else:
            self.print_info("Dependencias ya instaladas, continuando...")
            return True
    
    def build_frontend(self):
        """Ejecuta el build del frontend."""
        self.print_step(3, "Compilando frontend...")
        
        try:
            # Eliminar carpeta dist anterior si existe
            if self.dist_dir.exists():
                shutil.rmtree(self.dist_dir)
                self.print_info("Carpeta dist anterior eliminada")
            
            # Ejecutar build
            self.print_info("Ejecutando 'npm run build'...")
            start_time = time.time()
            
            result = subprocess.run(
                ["npm", "run", "build"],
                cwd=self.frontend_dir,
                capture_output=True,
                text=True
            )
            
            end_time = time.time()
            build_time = round(end_time - start_time, 2)
            
            if result.returncode == 0:
                self.print_success(f"Frontend compilado correctamente en {build_time}s")
                
                # Verificar que se generó la carpeta dist
                if self.dist_dir.exists():
                    files_count = len(list(self.dist_dir.rglob("*")))
                    self.print_info(f"Archivos generados: {files_count}")
                    return True
                else:
                    self.print_error("La carpeta dist no se generó")
                    return False
            else:
                self.print_error(f"Error compilando frontend:")
                self.print_error(result.stderr)
                return False
                
        except Exception as e:
            self.print_error(f"Error ejecutando build: {e}")
            return False
    
    def backup_static(self):
        """Crea un backup de la carpeta static actual."""
        backup_dir = self.backend_dir / f"static_backup_{int(time.time())}"
        
        if self.static_dir.exists() and any(self.static_dir.iterdir()):
            try:
                shutil.copytree(self.static_dir, backup_dir)
                self.print_info(f"Backup creado en: {backup_dir}")
                return backup_dir
            except Exception as e:
                self.print_warning(f"No se pudo crear backup: {e}")
                return None
        return None
    
    def deploy_static_files(self):
        """Copia los archivos compilados a la carpeta static del backend."""
        self.print_step(4, "Desplegando archivos estáticos...")
        
        try:
            # Crear backup si es necesario
            backup_dir = self.backup_static()
            
            # Limpiar carpeta static
            if self.static_dir.exists():
                shutil.rmtree(self.static_dir)
            self.static_dir.mkdir(parents=True, exist_ok=True)
            
            # Copiar archivos de dist a static
            self.print_info("Copiando archivos...")
            
            for item in self.dist_dir.iterdir():
                if item.is_file():
                    shutil.copy2(item, self.static_dir)
                elif item.is_dir():
                    shutil.copytree(item, self.static_dir / item.name)
            
            # Verificar que se copiaron los archivos
            copied_files = len(list(self.static_dir.rglob("*")))
            self.print_success(f"Archivos desplegados correctamente ({copied_files} archivos)")
            
            # Mostrar archivos principales
            main_files = []
            for file in ["index.html", "favicon.ico"]:
                if (self.static_dir / file).exists():
                    main_files.append(file)
            
            for folder in ["css", "js", "fonts", "img"]:
                folder_path = self.static_dir / folder
                if folder_path.exists():
                    file_count = len(list(folder_path.glob("*")))
                    main_files.append(f"{folder}/ ({file_count} archivos)")
            
            if main_files:
                self.print_info(f"Archivos principales: {', '.join(main_files)}")
            
            return True
            
        except Exception as e:
            self.print_error(f"Error desplegando archivos: {e}")
            return False
    
    def cleanup(self):
        """Limpia archivos temporales."""
        try:
            # Eliminar carpeta dist
            if self.dist_dir.exists():
                shutil.rmtree(self.dist_dir)
                self.print_info("Carpeta dist temporal eliminada")
        except Exception as e:
            self.print_warning(f"No se pudo limpiar archivos temporales: {e}")
    
    def run(self):
        """Ejecuta todo el proceso de build y despliegue."""
        self.print_colored(f"\n{self.BOLD}🚀 SIGNANCE SYSTEM - BUILD Y DESPLIEGUE FRONTEND{self.ENDC}")
        self.print_colored("=" * 60)
        
        start_time = time.time()
        
        # Verificar estructura
        if not self.check_directories():
            return False
        
        # Verificar npm
        if not self.check_npm():
            return False
        
        # Instalar dependencias
        if not self.install_dependencies():
            return False
        
        # Build frontend
        if not self.build_frontend():
            return False
        
        # Desplegar archivos
        if not self.deploy_static_files():
            return False
        
        # Limpiar archivos temporales
        self.cleanup()
        
        # Resumen final
        end_time = time.time()
        total_time = round(end_time - start_time, 2)
        
        self.print_colored(f"\n{self.BOLD}✨ PROCESO COMPLETADO EXITOSAMENTE{self.ENDC}")
        self.print_colored("=" * 60)
        self.print_success(f"Tiempo total: {total_time}s")
        self.print_info(f"Frontend desplegado en: {self.static_dir}")
        self.print_info("El backend ahora puede servir la aplicación desde /")
        
        return True


def main():
    """Función principal del script."""
    try:
        builder = FrontendBuilder()
        success = builder.run()
        
        if success:
            sys.exit(0)
        else:
            print("\n❌ El proceso falló. Revise los errores anteriores.")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n\n⚠️  Proceso cancelado por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
