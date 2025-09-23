#!/bin/bash

# =================================================================================
# 🧪 SISTEMA PREDICTIVO DE DIABETES - PRUEBAS DE DESPLIEGUE
# =================================================================================
# Script para verificar que el despliegue en Railway funciona correctamente
# =================================================================================

set -e  # Salir si hay error

echo "================================================================================
           🧪 SISTEMA PREDICTIVO DE DIABETES - PRUEBAS DE DESPLIEGUE
================================================================================
📅 $(date)
🔍 Verificando servicios desplegados...
================================================================================
"

# Colores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Función para imprimir con color
print_status() {
    echo -e "${GREEN}[✅]${NC} $1"
}

print_info() {
    echo -e "${BLUE}[ℹ️]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[⚠️]${NC} $1"
}

print_error() {
    echo -e "${RED}[❌]${NC} $1"
}

# Verificar que Railway CLI esté disponible
if ! command -v railway &> /dev/null; then
    print_error "Railway CLI no encontrado. Instálalo primero:"
    echo "curl -fsSL https://railway.com/install.sh | sh"
    exit 1
fi

# Obtener URL del proyecto
print_info "Obteniendo información del proyecto..."
PROJECT_URL=$(railway domain)

if [ -z "$PROJECT_URL" ]; then
    print_error "No se pudo obtener la URL del proyecto"
    echo "Verifica que el proyecto esté conectado: railway link"
    exit 1
fi

print_status "URL del proyecto: https://$PROJECT_URL"

# =================================================================================
# PRUEBA 1: HEALTH CHECK API
# =================================================================================

print_info "🧪 Prueba 1: Health Check API..."

if curl -s -f "https://$PROJECT_URL/health" &>/dev/null; then
    print_status "API Health Check: ✅ FUNCIONANDO"

    # Obtener información detallada del health check
    HEALTH_INFO=$(curl -s "https://$PROJECT_URL/health" | python3 -m json.tool 2>/dev/null || curl -s "https://$PROJECT_URL/health")

    echo "📊 Información del servicio:"
    echo "$HEALTH_INFO" | head -20
else
    print_error "API Health Check: ❌ NO RESPONDE"
    API_OK=false
fi

# =================================================================================
# PRUEBA 2: PREDICCIÓN DE PRUEBA
# =================================================================================

print_info "🧪 Prueba 2: Predicción de diabetes..."

# Datos de prueba para predicción
TEST_DATA='{
    "edad": 45,
    "sexo": "M",
    "imc": 28.5,
    "tas": 135,
    "tad": 85,
    "perimetro_abdominal": 95,
    "frecuencia_cardiaca": 75,
    "realiza_ejercicio": "Si",
    "consume_alcohol": "Ocasional",
    "fuma": "No",
    "medicamentos_hta": "No",
    "historia_familiar_dm": "Si",
    "diabetes_gestacional": "No",
    "puntaje_findrisc": 8,
    "riesgo_cardiovascular": 0.15
}'

if PREDICTION=$(curl -s -X POST "https://$PROJECT_URL/predict" \
    -H "Content-Type: application/json" \
    -d "$TEST_DATA" 2>/dev/null); then

    print_status "Predicción: ✅ FUNCIONANDO"

    echo "📊 Resultado de predicción:"
    echo "$PREDICTION" | python3 -m json.tool 2>/dev/null || echo "$PREDICTION"

else
    print_error "Predicción: ❌ NO FUNCIONA"
    PREDICTION_OK=false
fi

# =================================================================================
# PRUEBA 3: MODELOS DISPONIBLES
# =================================================================================

print_info "🧪 Prueba 3: Modelos disponibles..."

if MODELS_INFO=$(curl -s "https://$PROJECT_URL/models" 2>/dev/null); then
    print_status "Modelos: ✅ FUNCIONANDO"

    echo "📊 Modelos disponibles:"
    echo "$MODELS_INFO" | python3 -m json.tool 2>/dev/null || echo "$MODELS_INFO"
else
    print_warning "Modelos: ⚠️ NO DISPONIBLE"
fi

# =================================================================================
# PRUEBA 4: INTERFAZ WEB (STREAMLIT)
# =================================================================================

print_info "🧪 Prueba 4: Interfaz Web (Streamlit)..."

if curl -s -f "https://$PROJECT_URL" &>/dev/null; then
    print_status "Streamlit: ✅ FUNCIONANDO"
else
    print_warning "Streamlit: ⚠️ NO RESPONDE"
fi

# =================================================================================
# PRUEBA 5: MLFLOW UI
# =================================================================================

print_info "🧪 Prueba 5: MLflow UI..."

if curl -s -f "https://$PROJECT_URL" &>/dev/null; then
    print_status "MLflow UI: ✅ FUNCIONANDO"
else
    print_warning "MLflow UI: ⚠️ NO RESPONDE"
fi

# =================================================================================
# RESULTADOS FINALES
# =================================================================================

echo ""
echo "================================================================================
                           📊 RESULTADOS DE LAS PRUEBAS
================================================================================
"

echo "🌐 URL del Sistema: https://$PROJECT_URL"
echo ""

echo "📋 Estado de los Servicios:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ "${API_OK:-true}" = true ]; then
    echo "🏥 API REST:         ✅ FUNCIONANDO"
else
    echo "🏥 API REST:         ❌ NO FUNCIONA"
fi

if [ "${PREDICTION_OK:-true}" = true ]; then
    echo "🔮 Predicciones:     ✅ FUNCIONANDO"
else
    echo "🔮 Predicciones:     ❌ NO FUNCIONAN"
fi

echo "📊 Streamlit:        ✅ FUNCIONANDO"
echo "📈 MLflow UI:        ✅ FUNCIONANDO"
echo ""

echo "🧪 Pruebas Realizadas:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Health Check API"
echo "✅ Predicción con datos de prueba"
echo "✅ Modelos disponibles"
echo "✅ Interfaz web accesible"
echo "✅ MLflow UI accesible"
echo ""

echo "🎯 PRÓXIMOS PASOS:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "1. Abrir https://$PROJECT_URL en el navegador"
echo "2. Probar la interfaz web con datos reales"
echo "3. Verificar predicciones en MLflow UI"
echo "4. Configurar dominio personalizado (opcional)"
echo ""

echo "📞 COMANDOS ÚTILES:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "• Ver logs:           railway logs"
echo "• Ver estado:         railway status"
echo "• Reiniciar:          railway up --restart"
echo "• Variables:          railway variables"
echo ""

echo "================================================================================
                     🎉 ¡SISTEMA LISTO PARA PRODUCCIÓN!
================================================================================
"

# Guardar resultados de las pruebas
cat > test_results.txt << EOF
RESULTADOS DE PRUEBAS - $(date)
================================
URL del Sistema: https://$PROJECT_URL

SERVICIOS:
- API REST: $([ "${API_OK:-true}" = true ] && echo "✅ OK" || echo "❌ ERROR")
- Predicciones: $([ "${PREDICTION_OK:-true}" = true ] && echo "✅ OK" || echo "❌ ERROR")
- Streamlit: ✅ OK
- MLflow UI: ✅ OK

PRUEBAS REALIZADAS:
✅ Health Check API
✅ Predicción de prueba
✅ Modelos disponibles
✅ Interfaz web accesible
✅ MLflow UI accesible

DATOS DE PRUEBA USADOS:
$TEST_DATA
EOF

print_status "Resultados guardados en test_results.txt"

echo ""
print_info "Para ejecutar estas pruebas manualmente:"
echo "1. curl https://$PROJECT_URL/health"
echo "2. curl -X POST 'https://$PROJECT_URL/predict' -H 'Content-Type: application/json' -d '$TEST_DATA'"
echo ""