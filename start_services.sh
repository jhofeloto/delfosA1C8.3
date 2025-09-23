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

# Iniciar servicios
echo "📊 Iniciando servicios..."

# 1. MLflow UI (background)
echo "🔬 Iniciando MLflow UI..."
start_service "MLflow UI" "python -m mlflow ui --backend-store-uri mlruns --host $HOST --port 5004" 5004

# 2. API Service (principal)
echo "🔌 Iniciando API Service..."
start_service "API Service" "uvicorn api_service:app --host $HOST --port $PORT --workers 2" $PORT

# 3. Dashboard Service (background)
echo "📱 Iniciando Dashboard Service..."
start_service "Dashboard Service" "streamlit run dashboard_service.py --server.port 8501 --server.address $HOST --server.headless true" 8501

# Verificar estado de todos los servicios
echo "🔍 Verificando estado de servicios..."
sleep 10

all_services_ok=true

if check_port 5004; then
    echo "✅ MLflow UI: $BASE_URL/mlflow"
else
    echo "❌ MLflow UI no responde"
    all_services_ok=false
fi

if check_port $PORT; then
    echo "✅ API Service: $BASE_URL"
    echo "   Health check: $BASE_URL/health"
    echo "   API Docs: $BASE_URL/docs"
else
    echo "❌ API Service no responde"
    all_services_ok=false
fi

if check_port 8501; then
    echo "✅ Dashboard: $BASE_URL/dashboard"
else
    echo "❌ Dashboard no responde"
    all_services_ok=false
fi

if [ "$all_services_ok" = true ]; then
    echo "🎉 ¡Todos los servicios iniciados exitosamente!"
    echo ""
    echo "📋 URLs de acceso:"
    echo "   🌐 Aplicación: $BASE_URL"
    echo "   🔬 MLflow UI: $BASE_URL/mlflow"
    echo "   🔌 API Docs: $BASE_URL/docs"
    echo "   📱 Dashboard: $BASE_URL/dashboard"
    echo ""
    echo "💡 Para desarrollo local:"
    echo "   🔬 MLflow UI: http://localhost:5004"
    echo "   🔌 API Service: http://localhost:$PORT"
    echo "   📱 Dashboard: http://localhost:8501"
    echo ""
    echo "⏳ Manteniendo servicios activos..."
else
    echo "⚠️  Algunos servicios no se iniciaron correctamente"
    echo "🔄 Revisa los logs para más detalles"
    exit 1
fi

# Mantener el contenedor corriendo
while true; do
    sleep 30
    echo "💚 Servicios activos - $(date)"
done
