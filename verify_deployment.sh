#!/bin/bash

# Script de verificación de despliegue en Railway
# Sistema de Biomarcadores Digitales

set -e  # Detener en caso de error

echo "🔍 Verificando despliegue en Railway..."
echo "====================================="

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

# Verificar si Railway CLI está instalado
echo "🔧 Verificando Railway CLI..."
if ! command -v railway &> /dev/null; then
    print_status "error" "Railway CLI no está instalado"
    echo "💡 Instálalo con: npm install -g @railway/cli"
    exit 1
else
    print_status "success" "Railway CLI instalado"
fi

# Verificar si hay proyecto conectado
echo ""
echo "🔗 Verificando conexión con Railway..."
if railway status &> /dev/null; then
    print_status "success" "Proyecto Railway conectado"
else
    print_status "error" "No hay proyecto Railway conectado"
    echo "💡 Conecta tu proyecto con: railway link"
    exit 1
fi

# Obtener información del proyecto
echo ""
echo "📊 Información del proyecto:"
APP_NAME=$(railway status | grep "Project:" | awk '{print $2}' || echo "N/A")
APP_URL=$(railway domain 2>/dev/null || echo "N/A")

echo "   Nombre: $APP_NAME"
echo "   URL: $APP_URL"

# Verificar archivos necesarios
echo ""
echo "📁 Verificando archivos de configuración..."
required_files=("railway.toml" "Dockerfile" "start_services.sh" "requirements.txt")
all_files_exist=true

for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        print_status "success" "Archivo encontrado: $file"
    else
        print_status "error" "Archivo faltante: $file"
        all_files_exist=false
    fi
done

if [ "$all_files_exist" = false ]; then
    print_status "error" "Faltan archivos necesarios para el despliegue"
    exit 1
fi

# Verificar estado del despliegue
echo ""
echo "🚀 Verificando estado del despliegue..."
if railway status | grep -q "Status: SUCCESS"; then
    print_status "success" "Despliegue exitoso"
elif railway status | grep -q "Status: FAILED"; then
    print_status "error" "Despliegue fallido"
    echo "🔍 Revisa los logs con: railway logs"
    exit 1
else
    print_status "warning" "Despliegue en progreso o estado desconocido"
fi

# Verificar servicios
echo ""
echo "🔍 Verificando servicios..."
services=("api" "mlflow" "dashboard")
for service in "${services[@]}"; do
    if railway status | grep -q "$service"; then
        print_status "success" "Servicio $service configurado"
    else
        print_status "warning" "Servicio $service no encontrado"
    fi
done

# Verificar variables de entorno
echo ""
echo "🔐 Verificando variables de entorno..."
env_vars=("PYTHON_VERSION" "PORT" "MLFLOW_TRACKING_URI")
for var in "${env_vars[@]}"; do
    if railway variables | grep -q "$var"; then
        print_status "success" "Variable configurada: $var"
    else
        print_status "warning" "Variable no configurada: $var"
    fi
done

# Probar conectividad (si hay URL)
if [ "$APP_URL" != "N/A" ] && [ "$APP_URL" != "" ]; then
    echo ""
    echo "🌐 Probando conectividad..."
    if curl -s -f "$APP_URL/health" > /dev/null 2>&1; then
        print_status "success" "Health check exitoso"
    else
        print_status "warning" "Health check fallido - servicios pueden estar iniciando"
    fi
fi

# Ver logs recientes
echo ""
echo "📋 Logs recientes:"
railway logs --tail 10

# Resumen final
echo ""
echo "📊 RESUMEN DE VERIFICACIÓN"
echo "=========================="

if [ "$all_files_exist" = true ]; then
    print_status "success" "Todos los archivos de configuración están presentes"
else
    print_status "error" "Faltan archivos de configuración"
fi

if railway status | grep -q "Status: SUCCESS"; then
    print_status "success" "Despliegue completado exitosamente"
    echo ""
    echo "🎉 ¡Tu Sistema de Biomarcadores Digitales está desplegado!"
    echo ""
    echo "📋 URLs de acceso:"
    echo "   🌐 Aplicación: https://$APP_URL"
    echo "   🔬 MLflow UI: https://$APP_URL"
    echo "   🔌 API Docs: https://$APP_URL/docs"
    echo "   📱 Dashboard: https://$APP_URL"
    echo ""
    echo "🔍 Comandos útiles:"
    echo "   railway logs          # Ver logs en tiempo real"
    echo "   railway open          # Abrir aplicación en navegador"
    echo "   railway status        # Ver estado del proyecto"
    echo "   railway variables     # Ver variables de entorno"
else
    print_status "warning" "El despliegue puede estar en progreso"
    echo "⏳ Espera un momento y ejecuta este script nuevamente"
fi

echo ""
echo "💡 Para más información, consulta RAILWAY_DEPLOYMENT.md"