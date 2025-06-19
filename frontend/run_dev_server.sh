#!/bin/bash

# Script de inicio para el frontend de Signance System
# Detecta automáticamente la IP local y configura el servidor de desarrollo

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Iniciando Signance System Frontend${NC}"
echo "=" | awk '{for(i=1;i<=50;i++) printf "%s", $0; print ""}'

# Detectar IP local
if command -v hostname &> /dev/null; then
    LOCAL_IP=$(hostname -I | awk '{print $1}' 2>/dev/null || echo "127.0.0.1")
else
    LOCAL_IP="127.0.0.1"
fi

# Si no se pudo obtener la IP, usar ifconfig como fallback
if [ "$LOCAL_IP" = "127.0.0.1" ] && command -v ifconfig &> /dev/null; then
    LOCAL_IP=$(ifconfig | grep -Eo 'inet (addr:)?([0-9]*\.){3}[0-9]*' | grep -Eo '([0-9]*\.){3}[0-9]*' | grep -v '127.0.0.1' | head -n1)
fi

# Si aún no se pudo obtener, mantener localhost
if [ -z "$LOCAL_IP" ]; then
    LOCAL_IP="127.0.0.1"
fi

echo -e "${GREEN}🌐 El frontend será accesible en:${NC}"
echo -e "   - Local:      ${YELLOW}http://127.0.0.1:8080${NC}"
echo -e "   - Red Local:  ${YELLOW}http://$LOCAL_IP:8080${NC}"
echo "=" | awk '{for(i=1;i<=50;i++) printf "%s", $0; print ""}'
echo -e "${BLUE}📡 Para acceder desde otras computadoras:${NC}"
echo -e "   Usa la IP: ${GREEN}$LOCAL_IP${NC}"
echo "=" | awk '{for(i=1;i<=50;i++) printf "%s", $0; print ""}'

# Verificar si npm está instalado
if ! command -v npm &> /dev/null; then
    echo -e "${RED}❌ npm no está instalado. Por favor instala Node.js y npm.${NC}"
    exit 1
fi

# Verificar si existe package.json
if [ ! -f "package.json" ]; then
    echo -e "${RED}❌ No se encontró package.json. Asegúrate de estar en el directorio frontend.${NC}"
    exit 1
fi

# Instalar dependencias si no existen node_modules
if [ ! -d "node_modules" ]; then
    echo -e "${YELLOW}📦 Instalando dependencias...${NC}"
    npm install
fi

# Iniciar el servidor de desarrollo
echo -e "${GREEN}🎯 Iniciando servidor de desarrollo...${NC}"
npm run serve
