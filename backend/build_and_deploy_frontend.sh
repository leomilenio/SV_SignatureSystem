#!/bin/bash

# Script de build y despliegue para Unix/Linux/macOS
# Ejecutar desde la carpeta backend

echo ""
echo "================================================"
echo "  SIGNANCE SYSTEM - BUILD Y DESPLIEGUE FRONTEND"
echo "================================================"
echo ""

# Verificar que Python esté disponible
if ! command -v python3 &> /dev/null; then
    echo "❌ ERROR: Python3 no encontrado. Instale Python primero."
    exit 1
fi

# Ejecutar el script de Python
echo "🚀 Ejecutando script de build..."
python3 build_and_deploy_frontend.py

# Verificar resultado
if [ $? -eq 0 ]; then
    echo ""
    echo "✅ ÉXITO: Build completado correctamente."
else
    echo ""
    echo "❌ ERROR: El build falló. Revise los errores anteriores."
    exit 1
fi
