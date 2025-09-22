# 🚀 **DESPLIEGUE EN RAILWAY - SISTEMA PREDICTIVO DE DIABETES**

## 📋 **VISIÓN GENERAL**

Este documento describe el proceso completo para desplegar el Sistema Predictivo de Diabetes en Railway con ambientes separados de **test** y **producción**.

---

## 🏗️ **ARQUITECTURA EN RAILWAY**

```
🌐 Railway Project
├── 🏥 API REST (Puerto 8002)
├── 📊 Streamlit Web App (Puerto 8501)
├── 📈 MLflow UI (Puerto 5002)
├── 🗄️ PostgreSQL Database
└── 💾 Persistent Volumes (models, logs, mlruns)
```

### **Ambientes Disponibles:**
- **🟢 Test:** Para desarrollo y pruebas
- **🔴 Production:** Para uso en producción

---

## ⚡ **DESPLIEGUE RÁPIDO**

### **Paso 1: Preparación**
```bash
# Clonar el repositorio
git clone <tu-repositorio>
cd diabetes-prediction-system

# Ejecutar configuración inicial
chmod +x scripts/setup_railway.sh
./scripts/setup_railway.sh
```

### **Paso 2: Deploy a Test**
```bash
# Deploy automático a ambiente de test
./scripts/deploy_test.sh
```

### **Paso 3: Deploy a Producción**
```bash
# Deploy a ambiente de producción
./scripts/deploy_production.sh
```

---

## 📁 **ESTRUCTURA DE ARCHIVOS**

```
📦 diabetes-prediction-system/
├── 🏗️ railway.toml          # Configuración Railway
├── 🐳 Dockerfile             # Imagen Docker
├── 📋 .env.example           # Variables de entorno
├── 📜 requirements.txt       # Dependencias Python
├── 🏥 api.py                 # API REST
├── 📊 web_app.py             # Streamlit App
├── 📈 predictor.py           # Lógica de predicción
├── 🤖 models/                # Modelos ML
├── 📊 outputs/mlruns/        # Datos MLflow
└── 📜 scripts/
    ├── setup_railway.sh      # Config inicial
    ├── deploy_test.sh        # Deploy test
    └── deploy_production.sh  # Deploy prod
```

---

## ⚙️ **CONFIGURACIÓN DETALLADA**

### **1. railway.toml**
Configura múltiples servicios con diferentes puertos y variables de entorno específicas para cada ambiente.

### **2. Dockerfile**
- ✅ Python 3.12 slim
- ✅ Instala dependencias del sistema
- ✅ Copia modelos y datos MLflow
- ✅ Configura directorios persistentes
- ✅ Health check automático

### **3. Variables de Entorno**

#### **Variables Globales:**
```bash
ENVIRONMENT=test|production
LOG_LEVEL=DEBUG|INFO|WARNING
DEBUG=true|false
```

#### **API REST (Puerto 8002):**
```bash
API_HOST=0.0.0.0
API_PORT=8002
API_WORKERS=1|4
API_TIMEOUT=30
```

#### **Streamlit (Puerto 8501):**
```bash
STREAMLIT_SERVER_ADDRESS=0.0.0.0
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_HEADLESS=true
```

#### **MLflow (Puerto 5002):**
```bash
MLFLOW_TRACKING_URI=file:///app/outputs/mlruns
MLFLOW_HOST=0.0.0.0
MLFLOW_PORT=5002
```

#### **Base de Datos:**
```bash
DATABASE_URL=postgresql://...
DB_HOST=postgresql.railway.internal
DB_PORT=5432
```

---

## 🚀 **PROCESO DE DESPLIEGUE**

### **FASE 1: Configuración Inicial**

1. **Crear cuenta Railway** (si no tienes)
2. **Instalar Railway CLI:**
   ```bash
   curl -fsSL https://railway.app/install.sh | sh
   ```

3. **Configurar proyecto:**
   ```bash
   railway login
   railway link
   ./scripts/setup_railway.sh
   ```

### **FASE 2: Deploy a Test**

1. **Ejecutar deploy:**
   ```bash
   ./scripts/deploy_test.sh
   ```

2. **Verificar servicios:**
   ```bash
   railway status --environment test
   railway logs --environment test
   ```

3. **URLs de Test:**
   - API: `https://diabetes-api-test.up.railway.app`
   - Streamlit: `https://diabetes-streamlit-test.up.railway.app`
   - MLflow: `https://diabetes-mlflow-test.up.railway.app`

### **FASE 3: Deploy a Producción**

1. **Configurar variables de seguridad:**
   ```bash
   ./scripts/deploy_production.sh
   ```

2. **Verificar health check:**
   ```bash
   curl https://diabetes-api-production.up.railway.app/health
   ```

3. **URLs de Producción:**
   - API: `https://diabetes-api-production.up.railway.app`
   - Streamlit: `https://diabetes-streamlit-production.up.railway.app`
   - MLflow: `https://diabetes-mlflow-production.up.railway.app`

---

## 🔧 **COMANDOS ÚTILES DE RAILWAY**

### **Gestión de Ambientes:**
```bash
railway environments          # Listar ambientes
railway environment create    # Crear ambiente
railway environment destroy   # Eliminar ambiente
```

### **Variables de Entorno:**
```bash
railway variables             # Ver variables
railway variables set KEY=VALUE --environment test
railway variables delete KEY --environment production
```

### **Logs y Monitoreo:**
```bash
railway logs                  # Logs en tiempo real
railway logs --environment test
railway logs --service api    # Logs de servicio específico
```

### **Gestión de Servicios:**
```bash
railway status                # Estado de servicios
railway domain                # URLs de servicios
railway open                  # Abrir en navegador
```

---

## 📊 **MONITOREO Y MANTENIMIENTO**

### **Health Checks:**
- ✅ API: `/health` endpoint
- ✅ Streamlit: Página principal
- ✅ MLflow: UI accesible

### **Logs Importantes:**
```bash
# Ver logs de API
railway logs --service diabetes-api-test

# Ver logs de Streamlit
railway logs --service diabetes-streamlit-test

# Ver logs de MLflow
railway logs --service diabetes-mlflow-test
```

### **Métricas a Monitorear:**
- ⏱️ **Tiempo de respuesta** de la API
- 📊 **Uso de CPU y memoria**
- 💾 **Espacio en disco** (modelos, logs)
- 🔄 **Estado de servicios**

---

## 🔒 **SEGURIDAD EN PRODUCCIÓN**

### **Variables Sensibles:**
```bash
# Configurar en Railway dashboard:
SECRET_KEY=tu-secret-key-super-seguro
JWT_SECRET_KEY=tu-jwt-secret-key
DATABASE_URL=postgresql://user:pass@host:5432/db
```

### **Configuraciones de Seguridad:**
- ✅ **Debug = false** en producción
- ✅ **Logs nivel WARNING** en producción
- ✅ **Variables de entorno** encriptadas
- ✅ **Health checks** habilitados
- ✅ **Auto-scaling** configurado

---

## 🆘 **SOLUCIÓN DE PROBLEMAS**

### **Problema: Deploy falla**
```bash
# Ver logs detallados
railway logs --tail 1000

# Verificar variables de entorno
railway variables

# Reiniciar servicios
railway service restart diabetes-api-production
```

### **Problema: API no responde**
```bash
# Verificar health check
curl https://diabetes-api-production.up.railway.app/health

# Ver logs de la API
railway logs --service diabetes-api-production
```

### **Problema: Modelos no cargan**
```bash
# Verificar que los modelos existen
railway volume ls

# Ver logs de carga de modelos
railway logs --service diabetes-api-production | grep -i "model"
```

### **Problema: Base de datos no conecta**
```bash
# Verificar variables de DB
railway variables | grep DATABASE

# Probar conexión
railway run --environment production "python -c 'import psycopg2; print(\"DB OK\")'"
```

---

## 📈 **ESCALABILIDAD**

### **Configuración Actual:**
- **Test:** 1 worker, recursos mínimos
- **Production:** 4 workers, auto-scaling

### **Para Mayor Tráfico:**
1. **Aumentar workers:** `API_WORKERS=8`
2. **Configurar auto-scaling** en Railway
3. **Usar Redis** para cache
4. **CDN** para archivos estáticos

---

## 💰 **COSTOS ESTIMADOS**

### **Railway Pricing:**
- **Starter Plan:** $5/mes
- **Hobby Plan:** $20/mes (recomendado)
- **Pro Plan:** $50/mes (alta demanda)

### **Recursos por Ambiente:**
- **Test:** ~$5-10/mes
- **Production:** ~$20-50/mes
- **Base de datos:** ~$10-20/mes

---

## 🔄 **MIGRACIÓN FUTURA A GCP**

Cuando necesites más escalabilidad:

1. **Exportar datos** de Railway
2. **Configurar Cloud Run** con la misma imagen Docker
3. **Migrar base de datos** a Cloud SQL
4. **Configurar Load Balancer**
5. **Actualizar DNS**

---

## 📞 **SOPORTE**

### **Comandos de Emergencia:**
```bash
# Ver todos los servicios
railway status

# Reiniciar todos los servicios
railway up --reset

# Ver logs de todos los servicios
railway logs --all

# Acceder al shell de un servicio
railway run --environment production bash
```

### **Contacto:**
- 📧 **Email:** soporte@tusistema.com
- 📱 **Monitoreo:** Railway dashboard
- 📊 **Métricas:** Railway analytics

---

## ✅ **CHECKLIST DE DESPLIEGUE**

- [ ] ✅ Railway CLI instalado
- [ ] ✅ Proyecto conectado a Railway
- [ ] ✅ Ambientes test y production creados
- [ ] ✅ Variables de entorno configuradas
- [ ] ✅ Deploy a test exitoso
- [ ] ✅ Health checks funcionando
- [ ] ✅ Logs accesibles
- [ ] ✅ URLs funcionando
- [ ] ✅ Variables de producción configuradas
- [ ] ✅ Deploy a producción exitoso
- [ ] ✅ Monitoreo configurado
- [ ] ✅ Documentación actualizada

---

**🎉 ¡Tu Sistema Predictivo de Diabetes está listo para producción en Railway!**

**Próximos pasos:**
1. Ejecuta `./scripts/deploy_test.sh`
2. Prueba el sistema en test
3. Configura producción con `./scripts/deploy_production.sh`
4. ¡Comienza a usar tu API!

---

## 📚 **REFERENCIAS**

- [Railway Documentation](https://docs.railway.app)
- [Railway CLI Reference](https://docs.railway.app/develop/cli)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Python Production Checklist](https://12factor.net/)

---

**🚀 ¡Éxito con tu despliegue!**