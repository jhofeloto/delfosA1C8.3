#!/bin/bash
echo "🚀 DESPLIEGUE AUTOMÁTICO EN RENDER"
echo "="*50

# Verificar archivos
echo "📋 Verificando archivos..."
for file in Procfile runtime.txt requirements.txt render.yaml; do
    if [ -f "$file" ]; then
        echo "   ✅ $file"
    else
        echo "   ❌ $file no encontrado"
        exit 1
    fi
done

echo ""
echo "🌐 URLs esperadas:"
echo "   • API: https://diabetes-api.onrender.com"
echo "   • Docs: https://diabetes-api.onrender.com/docs"
echo "   • Health: https://diabetes-api.onrender.com/health"
echo ""
echo "📊 Variables de entorno automáticas:"
echo "   • ENVIRONMENT=production"
echo "   • DEBUG=false"
echo "   • LOG_LEVEL=INFO"
echo "   • SECRET_KEY (generada)"
echo "   • JWT_SECRET_KEY (generada)"
echo "   • API_HOST=0.0.0.0"
echo "   • API_PORT=8002"
echo "   • STREAMLIT_SERVER_ADDRESS=0.0.0.0"
echo "   • STREAMLIT_SERVER_PORT=8501"
echo "   • STREAMLIT_SERVER_HEADLESS=true"
echo "   • MLFLOW_TRACKING_URI=file:///app/outputs/mlruns"
echo "   • MLFLOW_HOST=0.0.0.0"
echo "   • MLFLOW_PORT=5002"
echo ""
echo "💡 INSTRUCCIONES:"
echo "1. Ve a: https://render.com"
echo "2. Regístrate con GitHub"
echo "3. New → Web Service"
echo "4. Conecta repositorio"
echo "5. Configura servicio:"
echo "   - Nombre: diabetes-api"
echo "   - Runtime: Python 3"
echo "   - Build: pip install -r requirements.txt"
echo "   - Start: python api.py --host 0.0.0.0 --port $PORT"
echo "6. Variables se configuran automáticamente"
echo "7. ¡Create Service!"
echo ""
echo "⏱️ Tiempo: 5-10 minutos"
echo "💰 Costo: GRATIS (750 horas)"
echo "🌍 URL final: https://diabetes-api.onrender.com"
