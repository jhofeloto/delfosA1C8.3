#!/bin/bash

# Script de verificación de despliegue en Render
# Sistema de Biomarcadores Digitales

set -e  # Detener en caso de error

echo "🔍 Verificando despliegue en Render..."
echo "===================================="

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Función para imprimir status
print_status() {
    local status=$1
    local message=$2

    if [ "$status" = "success" ]; then
        echo -e "${GREEN}✅ $message${NC}"
    elif [ "$status" = "warning" ]; then
        echo -e "${YELLOW}⚠️  $message${NC}"
    elif [ "$status" = "error" ]; then
        echo -e "${RED}❌ $message${NC}"
    else
        echo "ℹ️  $message"
    fi
}

# Configurar URL base
BASE_URL=${1:-"https://delfos-biomarkers.onrender.com"}

echo "🌐 Verificando: $BASE_URL"
echo ""

# Función para probar endpoint
test_endpoint() {
    local endpoint=$1
    local description=$2
    local timeout=${3:-10}

    local url="$BASE_URL$endpoint"

    if curl -s --max-time $timeout "$url" > /dev/null 2>&1; then
        print_status "success" "$description: $url"
        return 0
    else
        print_status "error" "$description: $url (no accesible)"
        return 1
    fi
}

# Verificar conectividad básica
echo "🔌 Probando conectividad básica..."
if curl -s --max-time 30 "$BASE_URL" > /dev/null 2>&1; then
    print_status "success" "Aplicación responde en $BASE_URL"
else
    print_status "error" "No se puede acceder a la aplicación"
    echo "💡 Posibles causas:"
    echo "   - El despliegue está en progreso"
    echo "   - Hay un error en la aplicación"
    echo "   - La URL es incorrecta"
    exit 1
fi

echo ""
echo "🔍 Probando endpoints específicos..."

# Probar health check
test_endpoint "/health" "Health Check" 5

# Probar API documentation
test_endpoint "/docs" "API Documentation" 10

# Probar MLflow UI
test_endpoint "/" "MLflow UI" 10

# Probar predicción (con datos de prueba)
echo ""
echo "🧪 Probando funcionalidad de predicción..."
test_data='{
    "edad": 45,
    "sexo": "F",
    "peso": 70.5,
    "altura": 165,
    "presion_sistolica": 120,
    "presion_diastolica": 80,
    "glucosa": 95,
    "colesterol_total": 180,
    "colesterol_hdl": 50,
    "colesterol_ldl": 110,
    "trigliceridos": 150,
    "imc": 25.8,
    "perimetro_abdominal": 85,
    "actividad_fisica": "moderada",
    "historial_familiar": "si",
    "tabaquismo": "no",
    "consumo_alcohol": "ocasional"
}'

if curl -s -X POST \
    -H "Content-Type: application/json" \
    -d "$test_data" \
    --max-time 30 \
    "$BASE_URL/predict" > /dev/null 2>&1; then
    print_status "success" "API de predicción funcional"
else
    print_status "warning" "API de predicción no responde (puede estar iniciando)"
fi

# Verificar rendimiento
echo ""
echo "⚡ Probando rendimiento..."
start_time=$(date +%s)

if curl -s --max-time 30 "$BASE_URL/health" > /dev/null 2>&1; then
    end_time=$(date +%s)
    response_time=$((end_time - start_time))
    print_status "success" "Tiempo de respuesta: ${response_time}s"

    if [ $response_time -lt 5 ]; then
        print_status "success" "Rendimiento excelente"
    elif [ $response_time -lt 15 ]; then
        print_status "warning" "Rendimiento aceptable"
    else
        print_status "error" "Rendimiento lento"
    fi
else
    print_status "error" "No se pudo medir el rendimiento"
fi

# Verificar logs de Render
echo ""
echo "📋 Información de despliegue:"
echo "💡 Para ver logs en Render Dashboard:"
echo "   1. Ve a https://dashboard.render.com"
echo "   2. Selecciona tu servicio 'delfos-biomarkers'"
echo "   3. Ve a la pestaña 'Logs'"
echo ""

# Resumen final
echo "📊 RESUMEN DE VERIFICACIÓN"
echo "=========================="

echo ""
echo "📋 URLs de acceso:"
echo "   🌐 Aplicación: $BASE_URL"
echo "   🔬 MLflow UI: $BASE_URL"
echo "   🔌 API Docs: $BASE_URL/docs"
echo "   📱 Dashboard: $BASE_URL"
echo ""

echo "🔧 Comandos útiles para Render:"
echo "   render logs                    # Ver logs"
echo "   render open                    # Abrir aplicación"
echo "   render restart                 # Reiniciar servicio"
echo "   render scale 2                 # Escalar a 2 instancias"
echo ""

echo "📞 Soporte de Render:"
echo "   - Dashboard: https://dashboard.render.com"
echo "   - Documentación: https://render.com/docs"
echo "   - Estado: https://status.render.com"
echo ""

echo "✅ ¡Verificación completada!"
echo ""
echo "💡 Si encuentras problemas:"
echo "   1. Revisa los logs en Render Dashboard"
echo "   2. Verifica las variables de entorno"
echo "   3. Asegúrate de que todos los servicios estén corriendo"
echo "   4. Consulta la documentación en RENDER_DEPLOYMENT.md"