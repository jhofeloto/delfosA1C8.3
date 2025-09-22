#!/bin/bash

# ========================================
# CONFIGURACIÓN INICIAL DE RAILWAY
# ========================================

echo "🚀 Configurando Railway para el Sistema Predictivo de Diabetes..."

# Colores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Verificar si railway CLI está instalado
if ! command -v railway &> /dev/null; then
    echo -e "${YELLOW}⚠️ Railway CLI no encontrado. Instalando...${NC}"
    curl -fsSL https://railway.app/install.sh | sh

    # Agregar a PATH si es necesario
    if [[ ":$PATH:" != *":$HOME/.railway:"* ]]; then
        echo 'export PATH="$HOME/.railway/bin:$PATH"' >> ~/.bashrc
        export PATH="$HOME/.railway/bin:$PATH"
    fi
fi

echo -e "${BLUE}🔐 Iniciando sesión en Railway...${NC}"
railway login --browserless

echo -e "${BLUE}🔗 Conectando al proyecto...${NC}"
railway link

echo -e "${BLUE}📋 Verificando estructura del proyecto...${NC}"

# Verificar archivos necesarios
required_files=("railway.toml" "Dockerfile" ".env.example" "requirements.txt")
for file in "${required_files[@]}"; do
    if [[ -f "$file" ]]; then
        echo -e "${GREEN}✅ $file encontrado${NC}"
    else
        echo -e "${RED}❌ $file no encontrado${NC}"
        exit 1
    fi
done

echo -e "${BLUE}🏗️ Creando ambientes...${NC}"

# Crear ambiente de test
if ! railway environments | grep -q "test"; then
    echo -e "${YELLOW}Creando ambiente TEST...${NC}"
    railway environment create test
else
    echo -e "${GREEN}✅ Ambiente TEST ya existe${NC}"
fi

# Crear ambiente de producción
if ! railway environments | grep -q "production"; then
    echo -e "${YELLOW}Creando ambiente PRODUCTION...${NC}"
    railway environment create production
else
    echo -e "${GREEN}✅ Ambiente PRODUCTION ya existe${NC}"
fi

echo -e "${BLUE}⚙️ Configurando variables de entorno...${NC}"

# Variables comunes para ambos ambientes
for env in "test" "production"; do
    echo -e "${BLUE}Configurando ambiente: $env${NC}"

    railway variables set ENVIRONMENT="$env" --environment "$env"
    railway variables set LOG_LEVEL="INFO" --environment "$env"
    railway variables set API_HOST="0.0.0.0" --environment "$env"
    railway variables set API_PORT="8002" --environment "$env"
    railway variables set STREAMLIT_SERVER_ADDRESS="0.0.0.0" --environment "$env"
    railway variables set STREAMLIT_SERVER_PORT="8501" --environment "$env"
    railway variables set STREAMLIT_SERVER_HEADLESS="true" --environment "$env"
    railway variables set MLFLOW_TRACKING_URI="file:///app/outputs/mlruns" --environment "$env"
    railway variables set MLFLOW_HOST="0.0.0.0" --environment "$env"
    railway variables set MLFLOW_PORT="5002" --environment "$env"
done

# Variables específicas para TEST
railway variables set DEBUG="true" --environment test
railway variables set API_WORKERS="1" --environment test

# Variables específicas para PRODUCTION
railway variables set DEBUG="false" --environment production
railway variables set API_WORKERS="4" --environment production

echo -e "${BLUE}📊 Verificando servicios configurados...${NC}"
railway status

echo ""
echo -e "${GREEN}✅ Configuración de Railway completada!${NC}"
echo ""
echo -e "${BLUE}🌐 Próximos pasos:${NC}"
echo "1. Configurar variables específicas en Railway dashboard"
echo "2. Ejecutar: ./scripts/deploy_test.sh"
echo "3. Probar el ambiente de test"
echo "4. Configurar producción con: ./scripts/deploy_production.sh"
echo ""
echo -e "${YELLOW}📝 Variables que necesitas configurar manualmente:${NC}"
echo "- DATABASE_URL (para producción)"
echo "- SECRET_KEY (para producción)"
echo "- JWT_SECRET_KEY (para producción)"
echo "- Dominios personalizados (opcional)"