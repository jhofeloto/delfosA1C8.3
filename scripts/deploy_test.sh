#!/bin/bash

# ========================================
# DEPLOY A AMBIENTE DE TEST EN RAILWAY
# ========================================

echo "🚀 Iniciando despliegue en ambiente TEST..."

# Variables de entorno para TEST
export RAILWAY_ENVIRONMENT="test"
export ENVIRONMENT="test"
export DEBUG="true"
export LOG_LEVEL="DEBUG"
export API_WORKERS="1"

# Colores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}📋 Configuración del ambiente TEST:${NC}"
echo "Environment: $RAILWAY_ENVIRONMENT"
echo "Debug: $DEBUG"
echo "Log Level: $LOG_LEVEL"
echo "API Workers: $API_WORKERS"
echo ""

# Verificar si railway CLI está instalado
if ! command -v railway &> /dev/null; then
    echo -e "${YELLOW}⚠️ Railway CLI no encontrado. Instalando...${NC}"
    curl -fsSL https://railway.app/install.sh | sh
fi

# Login a Railway (si no está logueado)
echo -e "${BLUE}🔐 Verificando autenticación en Railway...${NC}"
railway login

# Conectar al proyecto
echo -e "${BLUE}🔗 Conectando al proyecto Railway...${NC}"
railway link

# Configurar variables de entorno para TEST
echo -e "${BLUE}⚙️ Configurando variables de entorno para TEST...${NC}"
railway variables set ENVIRONMENT="test" --environment test
railway variables set DEBUG="true" --environment test
railway variables set LOG_LEVEL="DEBUG" --environment test
railway variables set API_WORKERS="1" --environment test

# Deploy a ambiente TEST
echo -e "${GREEN}🚀 Desplegando en ambiente TEST...${NC}"
railway up --environment test

# Verificar servicios
echo -e "${BLUE}🔍 Verificando servicios desplegados...${NC}"
railway status --environment test

echo ""
echo -e "${GREEN}✅ Despliegue en TEST completado!${NC}"
echo ""
echo -e "${BLUE}🌐 URLs del ambiente TEST:${NC}"
echo "API: https://diabetes-api-test.up.railway.app"
echo "Streamlit: https://diabetes-streamlit-test.up.railway.app"
echo "MLflow: https://diabetes-mlflow-test.up.railway.app"
echo ""
echo -e "${YELLOW}📝 Para ver logs: railway logs --environment test${NC}"
echo -e "${YELLOW}📝 Para ver variables: railway variables --environment test${NC}"