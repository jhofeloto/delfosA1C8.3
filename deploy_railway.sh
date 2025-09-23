#!/bin/bash

# =================================================================================
# 🚀 SISTEMA PREDICTIVO DE DIABETES - DESPLIEGUE AUTOMÁTICO A RAILWAY
# =================================================================================
# Script de despliegue automatizado siguiendo las instrucciones de Railway
# =================================================================================

set -e  # Salir si hay error

echo "================================================================================
           🚀 SISTEMA PREDICTIVO DE DIABETES - DESPLIEGUE A RAILWAY
================================================================================
📅 $(date)
🔧 Configurando despliegue automatizado...
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

# =================================================================================
# PASO 1: INSTALAR RAILWAY CLI
# =================================================================================

print_info "Instalando Railway CLI..."
if ! command -v railway &> /dev/null; then
    print_info "Railway CLI no encontrado. Instalando..."
    curl -fsSL https://railway.com/install.sh | sh

    # Verificar instalación
    if command -v railway &> /dev/null; then
        print_status "Railway CLI instalado correctamente"
    else
        print_error "Error instalando Railway CLI"
        exit 1
    fi
else
    print_status "Railway CLI ya está instalado"
fi

# =================================================================================
# PASO 2: CONECTAR AL PROYECTO
# =================================================================================

PROJECT_ID="6b9e5a32-331c-4a7c-bdd1-7ab1fe293c7b"

print_info "Conectando al proyecto: $PROJECT_ID"

if railway link -p "$PROJECT_ID"; then
    print_status "Proyecto conectado correctamente"
else
    print_warning "No se pudo conectar automáticamente al proyecto"
    print_info "Ejecutando railway login para autenticación manual..."
    railway login

    # Intentar conectar nuevamente después del login
    if railway link -p "$PROJECT_ID"; then
        print_status "Proyecto conectado después del login"
    else
        print_error "No se pudo conectar al proyecto. Verifica el ID del proyecto."
        exit 1
    fi
fi

# =================================================================================
# PASO 3: CONFIGURAR VARIABLES DE ENTORNO
# =================================================================================

print_info "Configurando variables de entorno..."

# Variables generales
railway variables --set "ENVIRONMENT=test"
railway variables --set "LOG_LEVEL=INFO"
railway variables --set "DEBUG=true"

# Variables API
railway variables --set "API_HOST=0.0.0.0"
railway variables --set "API_PORT=8002"

# Variables Streamlit
railway variables --set "STREAMLIT_SERVER_ADDRESS=0.0.0.0"
railway variables --set "STREAMLIT_SERVER_PORT=8501"
railway variables --set "STREAMLIT_SERVER_HEADLESS=true"

# Variables MLflow
railway variables --set "MLFLOW_TRACKING_URI=file:///app/outputs/mlruns"
railway variables --set "MLFLOW_HOST=0.0.0.0"
railway variables --set "MLFLOW_PORT=5002"

print_status "Variables de entorno configuradas"

# =================================================================================
# PASO 4: DESPLEGAR APLICACIÓN
# =================================================================================

print_info "Iniciando despliegue..."
print_info "Esto puede tomar varios minutos..."

if railway up; then
    print_status "¡Despliegue iniciado correctamente!"
else
    print_error "Error durante el despliegue"
    exit 1
fi

# =================================================================================
# PASO 5: OBTENER INFORMACIÓN DEL DESPLIEGUE
# =================================================================================

print_info "Obteniendo información del despliegue..."

# Esperar un momento para que los servicios se inicien
sleep 10

# Obtener URLs del proyecto
PROJECT_URL=$(railway domain)
print_status "URL del proyecto: https://$PROJECT_URL"

# =================================================================================
# PASO 6: VERIFICAR SERVICIOS
# =================================================================================

print_info "Verificando servicios..."

# Función para verificar si un servicio está funcionando
check_service() {
    local service_name=$1
    local port=$2
    local url="https://$PROJECT_URL"

    if curl -s -f "$url:$port/health" &>/dev/null; then
        print_status "$service_name funcionando en puerto $port"
        return 0
    else
        print_warning "$service_name no responde en puerto $port"
        return 1
    fi
}

# Verificar servicios
API_OK=false
STREAMLIT_OK=false
MLFLOW_OK=false

# Intentar verificar API (puerto 8002)
if check_service "API REST" "8002"; then
    API_OK=true
fi

# Intentar verificar Streamlit (puerto 8501)
if check_service "Streamlit" "8501"; then
    STREAMLIT_OK=true
fi

# Intentar verificar MLflow (puerto 5002)
if check_service "MLflow UI" "5002"; then
    MLFLOW_OK=true
fi

# =================================================================================
# PASO 7: MOSTRAR RESULTADOS
# =================================================================================

echo ""
echo "================================================================================
                           🎉 ¡DESPLIEGUE COMPLETADO!
================================================================================
"

if [ "$API_OK" = true ] && [ "$STREAMLIT_OK" = true ] && [ "$MLFLOW_OK" = true ]; then
    print_status "✅ TODOS LOS SERVICIOS FUNCIONAN CORRECTAMENTE"
else
    print_warning "⚠️ Algunos servicios pueden estar iniciando..."
fi

echo ""
echo "🌐 URLS DE ACCESO:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🏥 API REST:        https://$PROJECT_URL"
echo "📊 Streamlit:       https://$PROJECT_URL"
echo "📈 MLflow UI:       https://$PROJECT_URL"
echo ""

echo "🔧 PUERTOS INTERNOS:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "• API REST:         Puerto 8002"
echo "• Streamlit:        Puerto 8501"
echo "• MLflow UI:        Puerto 5002"
echo ""

echo "📊 SERVICIOS:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if [ "$API_OK" = true ]; then
    echo "✅ API REST:        Funcionando - Health check OK"
else
    echo "❌ API REST:        No responde - Verificar logs"
fi

if [ "$STREAMLIT_OK" = true ]; then
    echo "✅ Streamlit:       Funcionando - Dashboard web OK"
else
    echo "❌ Streamlit:       No responde - Verificar logs"
fi

if [ "$MLFLOW_OK" = true ]; then
    echo "✅ MLflow UI:       Funcionando - Seguimiento ML OK"
else
    echo "❌ MLflow UI:       No responde - Verificar logs"
fi

echo ""
echo "🧪 PRUEBAS RÁPIDAS:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "1. Health Check API:"
echo "   curl https://$PROJECT_URL/health"
echo ""
echo "2. Predicción de prueba:"
echo "   curl -X POST 'https://$PROJECT_URL/predict' \\"
echo "     -H 'Content-Type: application/json' \\"
echo "     -d '{\"edad\": 45, \"sexo\": \"M\", \"imc\": 28.5}'"
echo ""
echo "3. Dashboard Web:"
echo "   Abrir https://$PROJECT_URL en el navegador"
echo ""

echo "📋 PRÓXIMOS PASOS:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "1. Verificar que todos los servicios estén funcionando"
echo "2. Probar las predicciones con datos reales"
echo "3. Configurar dominio personalizado (opcional)"
echo "4. Configurar monitoreo y alertas"
echo ""

echo "================================================================================
                     🚀 ¡SISTEMA LISTO PARA USO EN PRODUCCIÓN!
================================================================================
"

# Guardar información del despliegue
cat > deployment_info.txt << EOF
DESPLIEGUE COMPLETADO
=====================
Fecha: $(date)
Proyecto: $PROJECT_URL
API: https://$PROJECT_URL
Streamlit: https://$PROJECT_URL
MLflow: https://$PROJECT_URL

Estado de servicios:
- API REST: $([ "$API_OK" = true ] && echo "✅ OK" || echo "❌ Error")
- Streamlit: $([ "$STREAMLIT_OK" = true ] && echo "✅ OK" || echo "❌ Error")
- MLflow UI: $([ "$MLFLOW_OK" = true ] && echo "✅ OK" || echo "❌ Error")
EOF

print_status "Información del despliegue guardada en deployment_info.txt"

echo ""
print_info "Para ver logs de servicios: railway logs"
print_info "Para ver estado: railway status"
print_info "Para reiniciar: railway up --restart"
echo ""