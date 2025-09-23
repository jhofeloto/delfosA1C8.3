# Dockerfile para Sistema de Biomarcadores Digitales - Optimizado para Render
FROM python:3.12-slim

# Configurar variables de entorno para Render
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONHASHSEED=random
ENV PIP_NO_CACHE_DIR=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV RENDER=true

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Crear directorio de trabajo
WORKDIR /app

# Copiar archivos de requirements primero (para cache de Docker)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código fuente
COPY . .

# Crear directorios necesarios con permisos correctos
RUN mkdir -p /app/models /app/data /app/outputs /app/mlruns && \
    chmod -R 755 /app && \
    chmod +x start_services.sh

# Configurar usuario no-root para Render
RUN useradd --create-home --shell /bin/bash app && \
    chown -R app:app /app
USER app

# Exponer puerto principal (Render maneja el routing)
EXPOSE 8000

# Comando de inicio optimizado para Render
CMD ["python", "main.py"]