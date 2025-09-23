# 🚀 Despliegue en Producción con Render

## 🏥 Sistema Predictivo de Diabetes Mellitus Tipo 2

Este documento describe el despliegue completo del sistema en la plataforma Render, incluyendo configuración de servicios, variables de entorno, y procedimientos de mantenimiento.

---

## 📋 Resumen de Servicios

El sistema se despliega en Render con **4 servicios principales**:

1. **API REST** (`diabetes-api`) - Puerto 8002
2. **Interfaz Web** (`diabetes-streamlit`) - Puerto 8501
3. **MLflow UI** (`diabetes-mlflow`) - Puerto 5000
4. **Base de Datos** (`diabetes-db`) - PostgreSQL

---

## 🔧 Configuración de Render

### 📄 Archivo `render.yaml`

```yaml
services:
  # API REST del Sistema Predictivo de Diabetes
  - type: web
    name: diabetes-api
    runtime: python3
    buildCommand: pip install -r requirements.txt
    startCommand: python api.py --host 0.0.0.0 --port $PORT
    healthCheckPath: /health
    envVars:
      - key: ENVIRONMENT
        value: production
      - key: DEBUG
        value: false
      - key: LOG_LEVEL
        value: INFO
      - key: SECRET_KEY
        generateValue: true
      - key: JWT_SECRET_KEY
        generateValue: true
      - key: API_HOST
        value: 0.0.0.0
      - key: API_PORT
        value: 8002
      - key: STREAMLIT_SERVER_ADDRESS
        value: 0.0.0.0
      - key: STREAMLIT_SERVER_PORT
        value: 8501
      - key: STREAMLIT_SERVER_HEADLESS
        value: true
      - key: MLFLOW_TRACKING_URI
        value: ./outputs/mlruns
      - key: MLFLOW_HOST
        value: 0.0.0.0
      - key: MLFLOW_PORT
        value: 5002

  # Interfaz Web Streamlit
  - type: web
    name: diabetes-streamlit
    runtime: python3
    buildCommand: pip install -r requirements.txt
    startCommand: streamlit run web_app.py --server.port $PORT --server.address 0.0.0.0 --server.headless true
    healthCheckPath: /
    envVars:
      - key: ENVIRONMENT
        value: production
      - key: DEBUG
        value: false
      - key: LOG_LEVEL
        value: INFO
      - key: STREAMLIT_SERVER_ADDRESS
        value: 0.0.0.0
      - key: STREAMLIT_SERVER_PORT
        value: 8501
      - key: STREAMLIT_SERVER_HEADLESS
        value: true
      - key: MLFLOW_TRACKING_URI
        value: ./outputs/mlruns
      - key: API_BASE_URL
        value: https://delfosa1c8-3.onrender.com

  # Sistema MLflow UI
  - type: web
    name: diabetes-mlflow
    runtime: python3
    buildCommand: pip install -r requirements.txt
    startCommand: python scripts/start_mlflow.py
    healthCheckPath: /
    healthCheckTimeout: 120
    envVars:
      - key: ENVIRONMENT
        value: production
      - key: DEBUG
        value: false
      - key: LOG_LEVEL
        value: INFO
      - key: MLFLOW_TRACKING_URI
        value: /app/outputs/mlruns
      - key: MLFLOW_HOST
        value: 0.0.0.0
      - key: MLFLOW_PORT
        value: 5000
      - key: MLFLOW_BACKEND_STORE_URI
        value: /app/outputs/mlruns
      - key: HOME
        value: /app
      - key: PORT
        value: 5000

  # Base de datos PostgreSQL
  - type: pserv
    name: diabetes-db
    envVars:
      - key: DATABASE_URL
        fromService:
          type: pserv
          name: diabetes-db
          property: connectionString
```

### 📄 Archivo `Procfile`

```bash
web: python api.py --host 0.0.0.0 --port $PORT
```

### 📄 Archivo `runtime.txt`

```txt
python-3.12.0
```

---

## 🌐 Variables de Entorno

### Variables Generales (Todos los servicios):
```bash
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=INFO
```

### Variables API (`diabetes-api`):
```bash
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here
API_HOST=0.0.0.0
API_PORT=8002
STREAMLIT_SERVER_ADDRESS=0.0.0.0
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_HEADLESS=true
MLFLOW_TRACKING_URI=./outputs/mlruns
MLFLOW_HOST=0.0.0.0
MLFLOW_PORT=5002
```

### Variables Streamlit (`diabetes-streamlit`):
```bash
STREAMLIT_SERVER_ADDRESS=0.0.0.0
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_HEADLESS=true
MLFLOW_TRACKING_URI=./outputs/mlruns
API_BASE_URL=https://your-api-url.onrender.com
```

### Variables MLflow (`diabetes-mlflow`):
```bash
MLFLOW_TRACKING_URI=/app/outputs/mlruns
MLFLOW_HOST=0.0.0.0
MLFLOW_PORT=5000
MLFLOW_BACKEND_STORE_URI=/app/outputs/mlruns
HOME=/app
PORT=5000
```

---

## 📋 Pasos para Despliegue

### 1. Preparación del Repositorio

1. **Asegurar archivos de configuración:**
   - `render.yaml` - Configuración de servicios
   - `Procfile` - Comando de inicio
   - `runtime.txt` - Versión de Python
   - `requirements.txt` - Dependencias

2. **Variables de entorno:**
   - Configurar todas las variables necesarias en Render Dashboard
   - Generar claves secretas automáticamente

3. **Modelos de ML:**
   - Asegurar que los modelos estén en el directorio `models/`
   - Verificar que `mlruns/` contenga los experimentos

### 2. Despliegue en Render

1. **Crear cuenta en Render** (si no tienes)
2. **Conectar repositorio GitHub**
3. **Configurar servicios:**
   - Importar configuración desde `render.yaml`
   - Configurar variables de entorno
   - Establecer dominios personalizados (opcional)

4. **Deploy inicial:**
   - Render detectará automáticamente la configuración
   - Construirá e iniciará todos los servicios
   - Tiempo estimado: 5-10 minutos

### 3. Verificación del Despliegue

1. **Health Checks:**
   - API: `https://your-api.onrender.com/health`
   - Streamlit: `https://your-streamlit.onrender.com/`
   - MLflow: `https://your-mlflow.onrender.com/`

2. **Pruebas de funcionamiento:**
   - Realizar predicción de prueba
   - Verificar carga de modelos
   - Confirmar conectividad entre servicios

---

## 🔍 URLs de Producción

### Servicios Principales:
- **API REST:** `https://diabetes-api-xxxx.onrender.com`
- **Streamlit:** `https://diabetes-streamlit-xxxx.onrender.com`
- **MLflow UI:** `https://diabetes-mlflow-xxxx.onrender.com`
- **Base de Datos:** Conexión interna

### Endpoints Importantes:
- **Health Check:** `GET /health`
- **Predicción:** `POST /predict`
- **Documentación:** `/docs` (Swagger UI)
- **Métricas:** `GET /model/info`

---

## 📊 Monitoreo y Logs

### Health Checks Automáticos:
- **API:** `/health` - Verifica estado del modelo
- **Streamlit:** `/` - Verifica interfaz web
- **MLflow:** `/` - Verifica UI de MLflow

### Logs en Render:
1. **Dashboard de Render:** Logs en tiempo real
2. **Métricas:** CPU, memoria, response times
3. **Alertas:** Notificaciones de fallos

### Monitoreo Personalizado:
```python
# Health check manual
import requests

response = requests.get("https://your-api.onrender.com/health")
print(f"Status: {response.json()['status']}")
print(f"Model Loaded: {response.json()['model_loaded']}")
```

---

## 🔧 Mantenimiento y Operaciones

### Actualizaciones del Sistema:

1. **Push a GitHub:**
   ```bash
   git add .
   git commit -m "Actualización del sistema"
   git push origin main
   ```

2. **Deploy automático:**
   - Render detecta cambios automáticamente
   - Reconstruye servicios afectados
   - Mantiene servicios activos durante el deploy

3. **Rollback:**
   - Revertir commit en GitHub
   - Render hará deploy automático de la versión anterior

### Gestión de Modelos:

1. **Actualizar modelos:**
   - Subir nuevos modelos a `models/`
   - Actualizar `mlruns/` con nuevos experimentos
   - Push a GitHub para deploy

2. **Verificar modelos:**
   ```bash
   curl -X GET "https://your-api.onrender.com/model/info"
   ```

### Backup y Recuperación:

1. **Base de datos:**
   - PostgreSQL snapshots automáticos en Render
   - Export manual: `pg_dump` si es necesario

2. **Modelos de ML:**
   - Versionados en Git (archivos .joblib)
   - Backup en MLflow UI

---

## 🛠️ Solución de Problemas

### Problemas Comunes:

#### 1. Error 502 Bad Gateway
**Causa:** Modelo no cargado o error en startup
**Solución:**
```bash
# Verificar logs en Render Dashboard
# Verificar variables de entorno
# Reiniciar servicio manualmente
```

#### 2. Model Loading Error
**Causa:** Modelos no encontrados o corruptos
**Solución:**
```bash
# Verificar que modelos estén en el repositorio
# Revisar logs de carga del modelo
# Verificar paths en configuración
```

#### 3. Memory Issues
**Causa:** Servicios consumiendo demasiada memoria
**Solución:**
```bash
# Optimizar carga de modelos
# Implementar lazy loading
# Considerar servicios separados
```

#### 4. Database Connection Issues
**Causa:** Problemas de conectividad PostgreSQL
**Solución:**
```bash
# Verificar configuración de red
# Revisar variables de entorno de DB
# Verificar estado del servicio de BD
```

### Comandos de Diagnóstico:

```bash
# Health check
curl -f https://your-api.onrender.com/health

# Model info
curl -X GET https://your-api.onrender.com/model/info

# Test prediction
curl -X POST https://your-api.onrender.com/predict \
  -H "Content-Type: application/json" \
  -d '{"edad": 45, "sexo": "M", "imc": 25.5, ...}'
```

### Logs de Debug:

1. **Render Dashboard:** Logs en tiempo real
2. **API Logs:** `/health` endpoint muestra estado
3. **Streamlit:** Logs del navegador de desarrollo
4. **MLflow:** Logs en la interfaz web

---

## 📈 Escalabilidad y Rendimiento

### Configuración Actual:
- **API:** 512MB RAM, 0.5 CPU
- **Streamlit:** 512MB RAM, 0.5 CPU
- **MLflow:** 512MB RAM, 0.5 CPU
- **Database:** 512MB RAM, 0.5 CPU

### Optimizaciones Implementadas:
- ✅ Lazy loading de modelos
- ✅ Health checks robustos
- ✅ Manejo de errores graceful
- ✅ Logging estructurado
- ✅ Configuración de producción

### Mejoras Futuras:
- 🔄 Load balancing para API
- 🔄 CDN para assets estáticos
- 🔄 Caching con Redis
- 🔄 Auto-scaling basado en demanda

---

## 🔒 Seguridad en Producción

### Configuraciones de Seguridad:
- ✅ HTTPS automático (Render)
- ✅ Variables de entorno seguras
- ✅ Health checks protegidos
- ✅ Logs sin datos sensibles
- ✅ Validación de entrada estricta

### Mejoras de Seguridad:
- 🔒 Autenticación JWT
- 🔒 Rate limiting
- 🔒 CORS configurado
- 🔒 Headers de seguridad
- 🔒 Monitoreo de seguridad

---

## 📞 Soporte y Contacto

### Información de Servicios:
- **API URL:** `https://diabetes-api-xxxx.onrender.com`
- **Streamlit URL:** `https://diabetes-streamlit-xxxx.onrender.com`
- **MLflow URL:** `https://diabetes-mlflow-xxxx.onrender.com`

### Monitoreo:
- **Dashboard:** Render Dashboard
- **Logs:** Logs en tiempo real
- **Métricas:** CPU, memoria, response times

### Contacto Técnico:
- 📧 Email: soporte@sistemadiabetes.com
- 📚 Documentación: `/docs` en API
- 🔄 Estado: `/health` endpoint

---

## 📋 Checklist de Despliegue

### Pre-Deploy:
- [ ] ✅ Repositorio actualizado en GitHub
- [ ] ✅ Modelos de ML en `models/`
- [ ] ✅ `requirements.txt` actualizado
- [ ] ✅ Variables de entorno configuradas
- [ ] ✅ `render.yaml` validado

### Deploy:
- [ ] ✅ Servicios creados en Render
- [ ] ✅ Variables de entorno configuradas
- [ ] ✅ Build exitoso
- [ ] ✅ Health checks funcionando

### Post-Deploy:
- [ ] ✅ API respondiendo correctamente
- [ ] ✅ Streamlit accesible
- [ ] ✅ MLflow funcionando
- [ ] ✅ Base de datos conectada
- [ ] ✅ Predicciones funcionando

---

**⚠️ Descargo de Responsabilidad:** Este sistema es una herramienta de apoyo para profesionales de la salud. No sustituye el juicio médico profesional ni los análisis de laboratorio. Siempre consultar con un médico para diagnósticos y tratamientos.

**📅 Última actualización:** Septiembre 2025
**🏥 Versión del Sistema:** 2.0.0