#!/usr/bin/env python3
"""
Script simplificado para build rápido del frontend.

Uso rápido:
    python quick_build.py
"""

import subprocess
import sys
from pathlib import Path


def quick_build():
    """Build rápido sin muchos mensajes."""
    script_dir = Path(__file__).parent.absolute()
    build_script = script_dir / "build_and_deploy_frontend.py"
    
    if not build_script.exists():
        print("❌ Script principal no encontrado")
        return False
    
    print("🚀 Iniciando build rápido...")
    
    try:
        result = subprocess.run([
            sys.executable, 
            str(build_script)
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Build completado exitosamente")
            return True
        else:
            print("❌ Error en el build:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


if __name__ == "__main__":
    success = quick_build()
    sys.exit(0 if success else 1)
