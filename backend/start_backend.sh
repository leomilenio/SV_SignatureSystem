#!/bin/bash

echo "🚀 Iniciando Signance System Backend"
echo "=================================="

# Obtener la IP local de la red
get_local_ip() {
    # macOS/Linux - obtener IP de la interfaz activa
    if command -v ipconfig &> /dev/null; then
        # macOS
        LOCAL_IP=$(ipconfig getifaddr en0 2>/dev/null || ipconfig getifaddr en1 2>/dev/null || echo "127.0.0.1")
    elif command -v ip &> /dev/null; then
        # Linux con ip command
        LOCAL_IP=$(ip route get 8.8.8.8 | awk '{print $7; exit}' 2>/dev/null || echo "127.0.0.1")
    elif command -v hostname &> /dev/null; then
        # Fallback usando hostname
        LOCAL_IP=$(hostname -I | awk '{print $1}' 2>/dev/null || echo "127.0.0.1")
    else
        LOCAL_IP="127.0.0.1"
    fi
    echo $LOCAL_IP
}

LOCAL_IP=$(get_local_ip)

echo "🌐 Backend accesible en:"
echo "   - Local:      http://127.0.0.1:8002"
echo "   - Red local:  http://$LOCAL_IP:8002"
echo "   - Health:     http://$LOCAL_IP:8002/health"
echo ""
echo "📱 Frontend accesible en:"
echo "   - Local:      http://127.0.0.1:3000"
echo "   - Red local:  http://$LOCAL_IP:3000"
echo ""
echo "🔌 WebSocket disponible en:"
echo "   - ws://$LOCAL_IP:8002/ws"
echo ""
echo "=================================="

# Cambiar al directorio del backend
cd "$(dirname "$0")"

# Activar entorno virtual si existe
if [ -f "venv/bin/activate" ]; then
    echo "🐍 Activando entorno virtual..."
    source venv/bin/activate
elif [ -f "../venv/bin/activate" ]; then
    echo "🐍 Activando entorno virtual..."
    source ../venv/bin/activate
fi

# Instalar dependencias si es necesario
if [ -f "requirements.txt" ]; then
    echo "📦 Verificando dependencias..."
    pip install -r requirements.txt --quiet
fi

# Iniciar el servidor
echo "🎬 Iniciando servidor FastAPI..."
echo ""

python -m uvicorn app.main:app \
    --host 0.0.0.0 \
    --port 8002 \
    --reload \
    --reload-dir app \
    --log-level info
