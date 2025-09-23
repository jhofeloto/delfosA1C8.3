#!/bin/bash

# Script de despliegue para Render
# Sistema de Biomarcadores Digitales

set -e  # Detener en caso de error

echo "🚀 Iniciando despliegue en Render..."

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

# Verificar si estamos en un repositorio git
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    print_status "error" "No se encuentra un repositorio git"
    exit 1
fi

# Verificar archivos necesarios
echo "📁 Verificando archivos de configuración..."
required_files=("render.yaml" "Dockerfile" "start_services.sh" "requirements.txt")
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

# Hacer scripts ejecutables
chmod +x start_services.sh

# Verificar si hay cambios sin commitear
if [ -n "$(git status --porcelain)" ]; then
    print_status "warning" "Hay cambios sin commitear"
    echo "¿Deseas hacer commit de los cambios? (y/n)"
    read -r response
    if [[ "$response" == "y" || "$response" == "Y" ]]; then
        echo "📝 Haciendo commit de cambios..."
        git add .
        git commit -m "Preparar despliegue en Render - $(date +'%Y-%m-%d %H:%M:%S')"
        print_status "success" "Cambios commiteados"
    else
        print_status "warning" "Continuando sin hacer commit"
    fi
fi

# Verificar rama actual
current_branch=$(git branch --show-current)
print_status "info" "Rama actual: $current_branch"

# Push a la rama actual
echo "⬆️  Subiendo cambios a GitHub..."
if git push origin $current_branch; then
    print_status "success" "Cambios subidos a GitHub"
else
    print_status "error" "Error al subir cambios a GitHub"
    exit 1
fi

echo ""
echo "🎉 ¡Preparación completada!"
echo ""
echo "📋 Próximos pasos para desplegar en Render:"
echo ""
echo "1. 🌐 Ve a https://dashboard.render.com"
echo ""
echo "2. 🔗 Conecta tu repositorio de GitHub:"
echo "   - Click en 'New' > 'Blueprint'"
echo "   - Selecciona 'Docker' como runtime"
echo "   - Conecta tu repositorio de GitHub"
echo ""
echo "3. ⚙️  Configura el servicio:"
echo "   - Nombre: delfos-biomarkers"
echo "   - Runtime: Docker"
echo "   - Dockerfile Path: ./Dockerfile"
echo "   - Build Command: (dejar vacío)"
echo "   - Start Command: ./start_services.sh"
echo ""
echo "4. 🔐 Configura variables de entorno:"
echo "   - PYTHON_VERSION=3.12"
echo "   - PORT=8000"
echo "   - MLFLOW_TRACKING_URI=https://delfos-biomarkers.onrender.com/mlflow"
echo "   - RENDER=true"
echo ""
echo "5. 💾 Configura disco persistente:"
echo "   - Mount Path: /app"
echo "   - Size: 10 GB"
echo ""
echo "6. 🚀 Despliega:"
echo "   - Click en 'Create Web Service'"
echo "   - Espera a que termine el despliegue"
echo ""
echo "📋 URLs después del despliegue:"
echo "   🌐 Aplicación: https://delfos-biomarkers.onrender.com"
echo "   🔬 MLflow UI: https://delfos-biomarkers.onrender.com/mlflow"
echo "   🔌 API Docs: https://delfos-biomarkers.onrender.com/docs"
echo "   📱 Dashboard: https://delfos-biomarkers.onrender.com/dashboard"
echo ""
echo "🔍 Para verificar el despliegue:"
echo "   curl https://delfos-biomarkers.onrender.com/health"
echo ""
echo "📞 Para soporte:"
echo "   - Render Dashboard: https://dashboard.render.com"
echo "   - Documentación: https://render.com/docs"
echo ""
echo "✅ ¡Tu aplicación está lista para desplegar en Render!"