# Dockerfile simplificado para Railway
FROM python:3.12-slim

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
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

# Copiar modelos directamente - Railway debería incluirlos en el build context
COPY models/*.joblib /app/models/ 2>/dev/null || echo "Modelos se copiarán en tiempo de ejecución"
COPY models/scaler.joblib /app/models/ 2>/dev/null || echo "Scaler se copiará en tiempo de ejecución"
COPY models/model_metadata.json /app/models/ 2>/dev/null || echo "Metadata se copiará en tiempo de ejecución"

# Configurar permisos
RUN chmod +x setup_system.py

# Crear script de inicialización simple
RUN echo '#!/bin/bash\n\
echo "🚀 Iniciando Sistema Predictivo de Diabetes..."\n\
\n\
# Crear directorios necesarios\n\
mkdir -p /app/models /app/outputs/mlruns /app/logs /app/data\n\
\n\
# Verificar modelos\n\
echo "📦 Verificando modelos..."\n\
if ls /app/models/*.joblib 1> /dev/null 2>&1; then\n\
    echo "✅ Modelos encontrados: $(ls /app/models/*.joblib | wc -l) archivos"\n\
else\n\
    echo "⚠️ No se encontraron modelos .joblib en /app/models/"\n\
fi\n\
\n\
# Ejecutar configuración del sistema\n\
echo "⚙️ Ejecutando configuración del sistema..."\n\
python /app/setup_system.py\n\
\n\
echo "✅ Sistema inicializado correctamente"\n\
' > /app/init.sh

RUN chmod +x /app/init.sh

# Exponer puertos
EXPOSE 8002 8501 5002

# Health check simple
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8002/health || exit 1

# Comando por defecto
CMD ["/app/init.sh"]