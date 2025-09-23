# 🚀 Despliegue en Railway - Sistema de Biomarcadores Digitales

## 📋 Resumen del Despliegue

Este proyecto está completamente configurado para desplegarse en **Railway** con una arquitectura de microservicios que incluye:

- **🔌 API Service** (FastAPI) - Puerto 8000
- **🔬 MLflow UI** - Puerto 5004
- **📱 Dashboard** (Streamlit) - Puerto 8501

## 🗂️ Archivos de Configuración

### `railway.toml`
Configuración principal de Railway con definición de servicios y puertos.

### `Dockerfile`
Imagen Docker optimizada para Railway con todas las dependencias necesarias.

### `start_services.sh`
Script de inicio que orquesta todos los servicios con verificación de estado.

### `deploy_railway.sh`
Script automatizado para el despliegue en Railway.

### `verify_deployment.sh`
Script para verificar el estado del despliegue y servicios.

### `test_railway_deployment.py`
Script de pruebas automatizadas para validar el despliegue.

## 🚀 Despliegue Rápido

### Opción 1: Despliegue Automático (Recomendado)
```bash
./deploy_railway.sh
```

### Opción 2: Despliegue Manual
```bash
# 1. Conectar proyecto Railway
railway link

# 2. Configurar variables de entorno
railway variables set PYTHON_VERSION=3.12
railway variables set MLFLOW_TRACKING_URI=https://your-app.railway.app/mlflow

# 3. Desplegar
railway up
```

## 🔍 Verificación del Despliegue

### Verificar Estado
```bash
./verify_deployment.sh
```

### Ejecutar Pruebas
```bash
python test_railway_deployment.py https://your-app.railway.app
```

### Ver Logs
```bash
railway logs --follow
```

## 📊 URLs de Acceso

Después del despliegue exitoso, tendrás acceso a:

- **🌐 Aplicación Principal**: `https://your-app.railway.app`
- **🔬 MLflow UI**: `https://your-app.railway.app`
- **🔌 API Documentation**: `https://your-app.railway.app/docs`
- **📱 Dashboard**: `https://your-app.railway.app`

## 🔧 Servicios Configurados

### API Service (Puerto 8000)
- ✅ Health check en `/health`
- ✅ Predicciones en `/predict`
- ✅ Documentación OpenAPI en `/docs`
- ✅ 4 workers para alta concurrencia

### MLflow UI (Puerto 5004)
- ✅ Interfaz web para gestión de experimentos
- ✅ Backend store: `mlruns/`
- ✅ Model registry integrado
- ✅ Tracking de métricas y parámetros

### Dashboard (Puerto 8501)
- ✅ Interfaz Streamlit para usuarios
- ✅ Formularios de entrada de datos médicos
- ✅ Visualización de resultados de predicción
- ✅ Modo headless para producción

## 🛠️ Comandos Útiles

### Gestión del Proyecto
```bash
railway status        # Estado del proyecto
railway open          # Abrir en navegador
railway logs          # Ver logs
railway variables     # Ver variables de entorno
```

### Gestión de Servicios
```bash
railway service ls    # Listar servicios
railway service logs  # Logs de un servicio específico
railway service restart # Reiniciar servicio
```

### Escalado
```bash
railway service scale api --replicas 3
railway service scale api --cpu 2 --memory 4GB
```

## 🔐 Variables de Entorno

Configura estas variables en Railway Dashboard o con CLI:

```bash
# Configuración básica
PYTHON_VERSION=3.12
PORT=8000

# MLflow
MLFLOW_TRACKING_URI=https://your-app.railway.app/mlflow

# Base de datos (opcional)
DATABASE_URL=postgresql://...

# API Keys (opcional)
OPENAI_API_KEY=your-key
DIFY_API_KEY=your-key

# Seguridad
JWT_SECRET_KEY=your-secret
API_SECRET_KEY=your-secret
```

## 📋 Checklist de Despliegue

- [x] Configuración de `railway.toml`
- [x] Dockerfile optimizado
- [x] Script de inicio de servicios
- [x] Variables de entorno configuradas
- [x] Health checks implementados
- [x] Logs y monitoreo configurados
- [x] Scripts de verificación y pruebas
- [x] Documentación completa

## 🔍 Troubleshooting

### Problema: Servicios no inician
```bash
railway logs --tail 50
railway service restart api
```

### Problema: Puerto ocupado
```bash
railway exec lsof -i :8000
```

### Problema: Memoria insuficiente
```bash
railway service scale api --memory 2GB
```

### Problema: Modelos no cargan
```bash
railway exec ls -la mlruns/
railway exec chmod -R 755 mlruns/
```

## 📞 Soporte

- **Documentación**: [Railway Docs](https://docs.railway.app)
- **Comunidad**: [Railway Discord](https://discord.gg/railway)
- **Logs detallados**: `RAILWAY_DEPLOYMENT.md`

## 🎯 Próximos Pasos

1. **Configurar dominio personalizado**
   ```bash
   railway domain add your-domain.com
   ```

2. **Configurar base de datos PostgreSQL**
   ```bash
   railway add postgresql
   ```

3. **Configurar monitoreo**
   ```bash
   railway add redis
   ```

4. **Configurar CI/CD**
   ```bash
   railway connect --github
   ```

---

**¡Tu Sistema de Biomarcadores Digitales está listo para producción en Railway! 🚀**

Para más detalles, consulta `RAILWAY_DEPLOYMENT.md`.