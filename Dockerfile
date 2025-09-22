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

# Copiar modelos pre-entrenados (si existen)
COPY models/*.joblib /app/models/ 2>/dev/null || echo "No models found, will download later"
COPY outputs/mlruns /app/outputs/mlruns 2>/dev/null || echo "No MLflow data found"

# Configurar permisos
RUN chmod +x setup_system.py

# Ejecutar configuración inicial
RUN python setup_system.py

# Exponer puertos
EXPOSE 8002 8501 5002

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8002/health || exit 1

# Comando por defecto (se sobreescribe en railway.toml)
CMD ["python", "api.py", "--host", "0.0.0.0", "--port", "8002"]