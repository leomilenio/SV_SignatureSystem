#!/bin/bash
# Script para probar la conectividad del backend Signance System

echo "🧪 Probando conectividad del Backend Signance System"
echo "============================================="

BACKEND_IP="10.0.1.76"
BACKEND_PORT="8002"

echo "📡 Probando conectividad local (127.0.0.1)..."
curl -s "http://127.0.0.1:${BACKEND_PORT}/health" && echo " ✅ OK" || echo " ❌ FALLO"

echo "📡 Probando conectividad de red local (${BACKEND_IP})..."
curl -s "http://${BACKEND_IP}:${BACKEND_PORT}/health" && echo " ✅ OK" || echo " ❌ FALLO"

echo "📡 Probando endpoint de documentación..."
curl -s "http://${BACKEND_IP}:${BACKEND_PORT}/docs" > /dev/null && echo " ✅ OK" || echo " ❌ FALLO"

echo ""
echo "🔍 Verificando puertos en uso:"
netstat -an | grep "${BACKEND_PORT}" | head -5

echo ""
echo "✅ Pruebas completadas"
echo "📋 Para acceder desde otra computadora usar: http://${BACKEND_IP}:${BACKEND_PORT}"
