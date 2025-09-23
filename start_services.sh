#!/bin/bash

# Script de inicio para Render - Sistema de Biomarcadores Digitales
echo "🚀 Iniciando Sistema de Biomarcadores Digitales en Render..."

# Función para verificar si un puerto está disponible
check_port() {
    local port=$1
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null ; then
        echo "✅ Puerto $port está disponible"
        return 0
    else
        echo "❌ Puerto $port no está disponible"
        return 1
    fi
}

# Función para iniciar servicio con retry
start_service() {
    local service_name=$1
    local command=$2
    local port=$3
    local max_retries=3

    echo "🔄 Iniciando $service_name en puerto $port..."

    for i in $(seq 1 $max_retries); do
        echo "Intento $i de $max_retries para $service_name..."

        # Iniciar servicio en background
        $command &
        local pid=$!

        # Esperar un momento para que el servicio inicie
        sleep 5

        # Verificar si el servicio está corriendo
        if check_port $port; then
            echo "✅ $service_name iniciado exitosamente (PID: $pid)"
            return 0
        else
            echo "❌ Falló el intento $i para $service_name"
            kill $pid 2>/dev/null
        fi
    done

    echo "❌ No se pudo iniciar $service_name después de $max_retries intentos"
    return 1
}

# Verificar si estamos en Render
if [ -n "$RENDER" ]; then
    echo "🌐 Detectado entorno Render"
    HOST="0.0.0.0"
    BASE_URL="https://delfos-biomarkers.onrender.com"
else
    echo "💻 Entorno local detectado"
    HOST="127.0.0.1"
    BASE_URL="http://localhost:8000"
fi

# Configurar variables de entorno para Render
export MLFLOW_TRACKING_URI=${MLFLOW_TRACKING_URI:-$BASE_URL/mlflow}
export PORT=${PORT:-8000}

echo "🔧 Configuración:"
echo "   Host: $HOST"
echo "   Puerto principal: $PORT"
echo "   MLflow URI: $MLFLOW_TRACKING_URI"
echo "   Base URL: $BASE_URL"

# Iniciar servicio principal
echo "🚀 Iniciando servicio principal..."

# Servicio principal que integra API y Dashboard
echo "🔌 Iniciando Delfos Biomarkers Service..."
start_service "Delfos Biomarkers" "python main.py" $PORT

# Verificar estado del servicio principal
echo "🔍 Verificando estado del servicio..."
sleep 10

if check_port $PORT; then
    echo "✅ Delfos Biomarkers Service: $BASE_URL"
    echo "   Health check: $BASE_URL/health"
    echo "   Dashboard: $BASE_URL"
    echo "   Info: $BASE_URL/info"
    echo ""
    echo "🎉 ¡Servicio iniciado exitosamente!"
    echo ""
    echo "📋 URLs de acceso:"
    echo "   🌐 Dashboard: $BASE_URL"
    echo "   🔌 API Predict: $BASE_URL/predict"
    echo "   ℹ️ Información: $BASE_URL/info"
    echo "   💚 Health Check: $BASE_URL/health"
    echo ""
    echo "⏳ Manteniendo servicio activo..."
else
    echo "❌ Servicio principal no responde"
    echo "🔄 Revisa los logs para más detalles"
    exit 1
fi

# Mantener el contenedor corriendo
while true; do
    sleep 30
    echo "💚 Servicios activos - $(date)"
done
