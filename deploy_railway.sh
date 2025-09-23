#!/bin/bash

# Script de despliegue para Railway
# Sistema de Biomarcadores Digitales

set -e  # Detener en caso de error

echo "🚀 Iniciando despliegue en Railway..."

# Verificar si Railway CLI está instalado
if ! command -v railway &> /dev/null; then
    echo "❌ Railway CLI no está instalado"
    echo "💡 Instálalo con: npm install -g @railway/cli"
    exit 1
fi

# Verificar si estamos en un repositorio git
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "❌ No se encuentra un repositorio git"
    exit 1
fi

# Verificar archivos necesarios
required_files=("railway.toml" "Dockerfile" "start_services.sh" "requirements.txt")
for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        echo "❌ Archivo requerido no encontrado: $file"
        exit 1
    fi
done

echo "✅ Verificación de archivos completada"

# Hacer el script ejecutable
chmod +x start_services.sh

# Verificar configuración de Railway
echo "🔧 Verificando configuración de Railway..."
railway status || {
    echo "⚠️  No hay proyecto Railway conectado"
    echo "💡 Conecta tu proyecto con: railway link"
    echo "¿Deseas conectar un proyecto existente? (y/n)"
    read -r response
    if [[ "$response" == "y" || "$response" == "Y" ]]; then
        railway link
    else
        echo "❌ Despliegue cancelado. Conecta tu proyecto primero."
        exit 1
    fi
}

# Configurar variables de entorno
echo "🔐 Configurando variables de entorno..."
railway variables set PYTHON_VERSION=3.12
railway variables set PORT=8000
railway variables set MLFLOW_TRACKING_URI=https://your-app.railway.app/mlflow

# Desplegar aplicación
echo "📦 Desplegando aplicación..."
railway up --detach

# Esperar a que el despliegue termine
echo "⏳ Esperando despliegue..."
sleep 30

# Verificar estado del despliegue
echo "🔍 Verificando estado del despliegue..."
railway status

# Obtener URL de la aplicación
APP_URL=$(railway domain)
if [ -n "$APP_URL" ]; then
    echo "🎉 ¡Despliegue exitoso!"
    echo ""
    echo "📋 URLs de acceso:"
    echo "   🌐 Aplicación: https://$APP_URL"
    echo "   🔬 MLflow UI: https://$APP_URL"
    echo "   🔌 API Docs: https://$APP_URL/docs"
    echo "   📱 Dashboard: https://$APP_URL"
    echo ""
    echo "💡 Para verificar el estado:"
    echo "   railway logs"
    echo "   railway open"
else
    echo "⚠️  No se pudo obtener la URL de la aplicación"
    echo "🔍 Revisa el estado con: railway status"
fi

echo "✅ Despliegue completado"