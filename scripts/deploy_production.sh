#!/bin/bash

# ========================================
# DEPLOY A AMBIENTE DE PRODUCCIÓN EN RAILWAY
# ========================================

echo "🚀 Iniciando despliegue en ambiente PRODUCCIÓN..."

# Variables de entorno para PRODUCCIÓN
export RAILWAY_ENVIRONMENT="production"
export ENVIRONMENT="production"
export DEBUG="false"
export LOG_LEVEL="WARNING"
export API_WORKERS="4"

# Colores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}📋 Configuración del ambiente PRODUCCIÓN:${NC}"
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

# Verificar que existe el ambiente de producción
echo -e "${BLUE}🔍 Verificando ambientes disponibles...${NC}"
railway environments

# Crear ambiente de producción si no existe
if ! railway environments | grep -q "production"; then
    echo -e "${YELLOW}⚠️ Ambiente de producción no encontrado. Creando...${NC}"
    railway environment create production
fi

# Configurar variables de entorno para PRODUCCIÓN
echo -e "${BLUE}⚙️ Configurando variables de entorno para PRODUCCIÓN...${NC}"
railway variables set ENVIRONMENT="production" --environment production
railway variables set DEBUG="false" --environment production
railway variables set LOG_LEVEL="WARNING" --environment production
railway variables set API_WORKERS="4" --environment production

# Variables específicas de producción
echo -e "${BLUE}🔒 Configurando variables de seguridad para PRODUCCIÓN...${NC}"
read -p "Ingrese la URL de la base de datos de producción: " DB_URL
read -p "Ingrese el SECRET_KEY para producción: " SECRET_KEY
read -s -p "Ingrese el JWT_SECRET_KEY para producción: " JWT_SECRET
echo ""

railway variables set DATABASE_URL="$DB_URL" --environment production
railway variables set SECRET_KEY="$SECRET_KEY" --environment production
railway variables set JWT_SECRET_KEY="$JWT_SECRET" --environment production

# Deploy a ambiente PRODUCCIÓN
echo -e "${GREEN}🚀 Desplegando en ambiente PRODUCCIÓN...${NC}"
railway up --environment production

# Verificar servicios
echo -e "${BLUE}🔍 Verificando servicios desplegados...${NC}"
railway status --environment production

# Verificar health check
echo -e "${BLUE}🏥 Verificando health check de la API...${NC}"
sleep 10
if railway domain | grep -q "production"; then
    API_URL=$(railway domain | grep "diabetes-api-production" | head -1)
    if curl -f "https://$API_URL/health" > /dev/null 2>&1; then
        echo -e "${GREEN}✅ Health check de API exitoso${NC}"
    else
        echo -e "${RED}❌ Health check de API falló${NC}"
    fi
fi

echo ""
echo -e "${GREEN}✅ Despliegue en PRODUCCIÓN completado!${NC}"
echo ""
echo -e "${BLUE}🌐 URLs del ambiente PRODUCCIÓN:${NC}"
echo "API: https://diabetes-api-production.up.railway.app"
echo "Streamlit: https://diabetes-streamlit-production.up.railway.app"
echo "MLflow: https://diabetes-mlflow-production.up.railway.app"
echo ""
echo -e "${YELLOW}📝 Para ver logs: railway logs --environment production${NC}"
echo -e "${YELLOW}📝 Para ver variables: railway variables --environment production${NC}"
echo ""
echo -e "${RED}⚠️ IMPORTANTE: Configurar dominio personalizado en Railway${NC}"
echo -e "${RED}⚠️ Configurar SSL/TLS en producción${NC}"
echo -e "${RED}⚠️ Configurar monitoreo y alertas${NC}"