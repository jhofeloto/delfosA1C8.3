# Dockerfile optimizado para Railway
FROM python:3.12-slim

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Crear directorio de trabajo
WORKDIR /app

# Copiar archivos de dependencias
COPY requirements.txt .
COPY setup_system.py .

# Instalar Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código fuente
COPY . .

# Crear directorios necesarios
RUN mkdir -p /app/models /app/outputs/mlruns /app/logs /app/data

# Copiar modelos - Railway los tendrá disponibles en el build context
COPY models/*.joblib /app/models/ 2>/dev/null || echo "Modelos se copiarán en tiempo de ejecución"
COPY models/scaler.joblib /app/models/ 2>/dev/null || echo "Scaler se copiará en tiempo de ejecución"
COPY models/model_metadata.json /app/models/ 2>/dev/null || echo "Metadata se copiará en tiempo de ejecución"

# Copiar modelos pre-entrenados (si existen)
# Nota: Los modelos se copiarán en tiempo de ejecución si no existen
RUN mkdir -p /app/models /app/outputs/mlruns

# Configurar permisos
RUN chmod +x setup_system.py

# Crear script de inicialización
RUN echo '#!/bin/bash\n\
echo "🚀 Iniciando Sistema Predictivo de Diabetes..."\n\
\n\
# Crear directorios necesarios\n\
mkdir -p /app/models /app/outputs/mlruns /app/logs /app/data\n\
\n\
# Copiar modelos si existen\n\
echo "📦 Verificando modelos disponibles..."\n\
if [ -f "/app/models/gradient_boosting.joblib" ]; then\n\
    echo "✅ Modelos ya disponibles en /app/models/"\n\
else\n\
    echo "📥 Copiando modelos desde el build context..."\n\
    # Copiar modelos desde el directorio de trabajo\n\
    if [ -d "/tmp/models" ] && ls /tmp/models/*.joblib 1> /dev/null 2>&1; then\n\
        cp /tmp/models/*.joblib /app/models/\n\
        echo "✅ Modelos copiados desde /tmp/models/"\n\
    else\n\
        echo "⚠️ No se encontraron modelos en /tmp/models/, intentando copia directa..."\n\
        # Intentar copiar directamente (esto debería funcionar si los modelos están en el build context)\n\
        cp -r /app/models_orig/* /app/models/ 2>/dev/null || echo "⚠️ No se pudieron copiar modelos"\n\
    fi\n\
fi\n\
\n\
# Verificar que los modelos críticos existen\n\
if [ -f "/app/models/gradient_boosting.joblib" ] || [ -f "/app/models/random_forest.joblib" ]; then\n\
    echo "✅ Modelos principales encontrados"\n\
else\n\
    echo "❌ No se encontraron modelos principales - esto causará problemas"\n\
fi\n\
\n\
# Copiar datos de MLflow si existen\n\
if [ -d "/app/outputs/mlruns" ]; then\n\
    echo "✅ Datos de MLflow ya disponibles"\n\
else\n\
    echo "📊 Copiando datos de MLflow..."\n\
    if [ -d "/tmp/mlruns" ]; then\n\
        cp -r /tmp/mlruns /app/outputs/\n\
        echo "✅ Datos de MLflow copiados"\n\
    else\n\
        echo "⚠️ No se encontraron datos de MLflow"\n\
    fi\n\
fi\n\
\n\
# Configurar permisos\n\
chmod +x /app/setup_system.py\n\
\n\
# Ejecutar configuración del sistema\n\
echo "⚙️ Ejecutando configuración del sistema..."\n\
python /app/setup_system.py\n\
\n\
echo "✅ Sistema inicializado correctamente"\n\
echo "🌐 URLs disponibles:"\n\
echo "  - API: http://localhost:8002"\n\
echo "  - Streamlit: http://localhost:8501"\n\
echo "  - MLflow: http://localhost:5002"\n\
' > /app/init.sh

RUN chmod +x /app/init.sh

# Exponer puertos
EXPOSE 8002 8501 5002

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8002/health || exit 1

# Comando por defecto (se sobreescribe en railway.toml)
CMD ["/app/init.sh"]