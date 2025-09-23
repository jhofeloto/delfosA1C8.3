#!/bin/bash

# Script de inicio para Render - Sistema de Biomarcadores Digitales
echo "🚀 Iniciando Sistema de Biomarcadores Digitales en Render..."

# Función simple para verificar puerto usando netstat
check_port() {
    local port=$1
    if netstat -tln | grep -q ":$port "; then
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
        sleep 10

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

# Configurar variables de entorno para Render
export PORT=${PORT:-8000}
export HOST=${HOST:-"0.0.0.0"}

echo "🔧 Configuración:"
echo "   Host: $HOST"
echo "   Puerto: $PORT"

# Iniciar servicio principal
echo "🚀 Iniciando Delfos Biomarkers Service..."

# Iniciar el servicio directamente sin verificaciones complejas
python main.py
