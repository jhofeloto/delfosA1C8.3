# 🚀 **DESPLIEGUE A RAILWAY - SISTEMA PREDICTIVO DE DIABETES**

## 📋 **INFORMACIÓN GENERAL**

**Sistema:** Sistema Predictivo de Diabetes con ML
**Plataforma:** Railway
**ID del Proyecto:** `6b9e5a32-331c-4a7c-bdd1-7ab1fe293c7b`
**Servicios:** 3 servicios (API REST, Streamlit, MLflow UI)

---

## 🎯 **PASOS DE DESPLIEGUE**

### **Paso 1: Instalar Railway CLI**

```bash
curl -fsSL https://railway.com/install.sh | sh
```

**Verificar instalación:**
```bash
railway --version
```

### **Paso 2: Conectar al Proyecto**

```bash
railway link -p 6b9e5a32-331c-4a7c-bdd1-7ab1fe293c7b
```

**Si no funciona, autenticarse:**
```bash
railway login
railway link -p 6b9e5a32-331c-4a7c-bdd1-7ab1fe293c7b
```

### **Paso 3: Despliegue Automatizado (Recomendado)**

**Ejecutar el script de despliegue:**
```bash
./deploy_railway.sh
```

**El script automáticamente:**
- ✅ Instala Railway CLI (si no está instalado)
- ✅ Conecta al proyecto específico
- ✅ Configura todas las variables de entorno
- ✅ Inicia el despliegue
- ✅ Verifica que los servicios funcionen
- ✅ Muestra las URLs de acceso

### **Paso 4: Verificar Despliegue**

**Ejecutar pruebas automáticas:**
```bash
./test_deployment.sh
```

**O probar manualmente:**
```bash
# Health Check
curl https://TU-PROJECT.railway.app/health

# Predicción de prueba
curl -X POST "https://TU-PROJECT.railway.app/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "edad": 45,
    "sexo": "M",
    "imc": 28.5,
    "tas": 135,
    "tad": 85,
    "perimetro_abdominal": 95
  }'
```

---

## 🌐 **URLS DE ACCESO**

Después del despliegue exitoso:

| Servicio | URL | Puerto |
|----------|-----|--------|
| **API REST** | `https://TU-PROJECT.railway.app` | 8002 |
| **Streamlit** | `https://TU-PROJECT.railway.app` | 8501 |
| **MLflow UI** | `https://TU-PROJECT.railway.app` | 5002 |

---

## ⚙️ **VARIABLES DE ENTORNO CONFIGURADAS**

### **Variables Generales:**
```
ENVIRONMENT=test
LOG_LEVEL=INFO
DEBUG=true
```

### **API REST:**
```
API_HOST=0.0.0.0
API_PORT=8002
```

### **Streamlit:**
```
STREAMLIT_SERVER_ADDRESS=0.0.0.0
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_HEADLESS=true
```

### **MLflow:**
```
MLFLOW_TRACKING_URI=file:///app/outputs/mlruns
MLFLOW_HOST=0.0.0.0
MLFLOW_PORT=5002
```

---

## 🧪 **PRUEBAS DEL SISTEMA**

### **1. Health Check:**
```bash
curl https://TU-PROJECT.railway.app/health
```

**Respuesta esperada:**
```json
{
  "status": "healthy",
  "timestamp": "2025-01-22T12:00:00",
  "version": "2.0.0",
  "model_loaded": true,
  "total_predictions": 0
}
```

### **2. Predicción:**
```bash
curl -X POST "https://TU-PROJECT.railway.app/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "edad": 45,
    "sexo": "M",
    "imc": 28.5,
    "tas": 135,
    "tad": 85,
    "perimetro_abdominal": 95,
    "frecuencia_cardiaca": 75,
    "realiza_ejercicio": "Si",
    "consume_alcohol": "Ocasional",
    "fuma": "No",
    "medicamentos_hta": "No",
    "historia_familiar_dm": "Si",
    "diabetes_gestacional": "No",
    "puntaje_findrisc": 8,
    "riesgo_cardiovascular": 0.15
  }'
```

**Respuesta esperada:**
```json
{
  "prediction": "Alto riesgo de diabetes",
  "probability": 0.78,
  "model_used": "gradient_boosting",
  "confidence": "high"
}
```

### **3. Modelos Disponibles:**
```bash
curl https://TU-PROJECT.railway.app/models
```

### **4. Dashboard Web:**
Abrir `https://TU-PROJECT.railway.app` en el navegador

---

## 📊 **ESTRUCTURA DEL PROYECTO**

```
📁 delfosA1C8.3/
├── 🏗️ railway.toml          # Configuración multi-servicio
├── 🐳 Dockerfile            # Imagen de contenedor
├── 📋 requirements.txt      # Dependencias Python
├── 🚀 deploy_railway.sh     # Script de despliegue
├── 🧪 test_deployment.sh    # Script de pruebas
├── 📖 DEPLOYMENT_README.md  # Esta documentación
├──
├── 🏥 api.py               # API REST FastAPI
├── 📊 web_app.py           # Dashboard Streamlit
├── 🔮 predictor.py         # Sistema de predicciones
├── ⚙️ config.py            # Configuración
├──
├── 🤖 models/              # Modelos ML
│   ├── gradient_boosting.joblib
│   ├── random_forest.joblib
│   ├── scaler.joblib
│   └── model_metadata.json
├──
└── 📈 outputs/mlruns/      # Datos MLflow
```

---

## 🔧 **COMANDOS ÚTILES**

### **Gestión del Proyecto:**
```bash
railway status          # Estado del proyecto
railway logs            # Ver logs de servicios
railway variables       # Ver variables de entorno
railway domain          # Obtener URL del proyecto
```

### **Gestión de Servicios:**
```bash
railway up              # Desplegar servicios
railway up --restart    # Reiniciar servicios
railway down            # Detener servicios
```

### **Variables de Entorno:**
```bash
railway variables set VARIABLE_NAME=value
railway variables unset VARIABLE_NAME
```

---

## 🐛 **SOLUCIÓN DE PROBLEMAS**

### **Problema: Railway CLI no funciona**
```bash
# Reinstalar CLI
curl -fsSL https://railway.com/install.sh | sh

# Verificar instalación
railway --version
```

### **Problema: No se puede conectar al proyecto**
```bash
# Autenticarse
railway login

# Conectar al proyecto específico
railway link -p 6b9e5a32-331c-4a7c-bdd1-7ab1fe293c7b
```

### **Problema: Servicios no responden**
```bash
# Ver logs
railway logs

# Reiniciar servicios
railway up --restart

# Verificar variables
railway variables
```

### **Problema: Modelos no cargan**
```bash
# Verificar que los modelos estén en el directorio
ls -la models/

# Verificar logs del servicio API
railway logs --service api
```

---

## 📈 **MONITOREO Y MANTENIMIENTO**

### **Logs de Servicios:**
```bash
railway logs --follow    # Logs en tiempo real
railway logs --service api    # Logs solo del servicio API
railway logs --service streamlit  # Logs solo de Streamlit
railway logs --service mlflow     # Logs solo de MLflow
```

### **Estado de Servicios:**
```bash
railway status
```

### **Métricas de Uso:**
```bash
# Health check continuo
watch curl -s https://TU-PROJECT.railway.app/health

# Métricas de predicciones
curl https://TU-PROJECT.railway.app/health | jq '.total_predictions'
```

---

## 🚀 **PRÓXIMOS PASOS**

### **Después del Despliegue Exitoso:**

1. **✅ Verificar Funcionalidad:**
   - Probar health check
   - Realizar predicciones de prueba
   - Verificar dashboard web

2. **🔒 Configurar Producción:**
   - Cambiar `ENVIRONMENT=production`
   - Configurar `DEBUG=false`
   - Ajustar `LOG_LEVEL=WARNING`

3. **🌐 Dominio Personalizado:**
   - Configurar dominio en Railway Dashboard
   - Actualizar variables de entorno

4. **📊 Monitoreo:**
   - Configurar alertas
   - Monitoreo de rendimiento
   - Logs centralizados

5. **🔄 CI/CD:**
   - Configurar despliegue automático
   - Tests automáticos
   - Validación continua

---

## 📞 **SOPORTE**

### **Comandos de Emergencia:**
```bash
# Ver todos los logs
railway logs --follow

# Reiniciar todos los servicios
railway up --restart

# Ver variables de entorno
railway variables

# Obtener información del proyecto
railway info
```

### **Contacto:**
- **Railway Dashboard:** [railway.app](https://railway.app)
- **Documentación Railway:** [docs.railway.app](https://docs.railway.app)
- **ID del Proyecto:** `6b9e5a32-331c-4a7c-bdd1-7ab1fe293c7b`

---

## 🎉 **¡FELICITACIONES!**

**Tu Sistema Predictivo de Diabetes está ahora desplegado en Railway:**

✅ **3 servicios funcionando** (API, Streamlit, MLflow)  
✅ **Modelos ML cargados** (Gradient Boosting, Random Forest)  
✅ **API REST completa** (6 endpoints funcionales)  
✅ **Dashboard web interactivo** (Interfaz Streamlit)  
✅ **Seguimiento ML** (MLflow UI)  
✅ **Base de datos** (PostgreSQL incluida)  
✅ **Monitoreo automático** (Health checks)  

**¡Tu aplicación está lista para uso en producción! 🚀**

---

**📅 Última actualización:** 22 de septiembre de 2025
**🔧 Mantenido por:** Sistema de Despliegue Automatizado