# 🚀 Despliegue en Render - Sistema de Biomarcadores Digitales

## 📋 Resumen del Despliegue

El **Sistema de Biomarcadores Digitales** está completamente configurado para desplegarse en **Render** con una arquitectura optimizada que incluye:

- **🔌 API Service** (FastAPI) - Puerto 8000
- **🔬 MLflow UI** - Puerto 5004
- **📱 Dashboard** (Streamlit) - Puerto 8501

## 🗂️ Archivos de Configuración

### `render.yaml`
Configuración principal de Render con servicios integrados y variables de entorno.

### `Dockerfile`
Imagen Docker optimizada para Render con usuario no-root y health checks integrados.

### `start_services.sh`
Script de orquestación de servicios optimizado para el entorno de Render.

### `deploy_render.sh`
Script de preparación y subida automática a GitHub para despliegue en Render.

### `verify_render_deployment.sh`
Script de verificación y pruebas automatizadas del despliegue.

### `RENDER_DEPLOYMENT.md`
Documentación completa del proceso de despliegue en Render.

## 🚀 Despliegue Rápido

### Paso 1: Preparación Automática
```bash
./deploy_render.sh
```

### Paso 2: Configuración en Render Dashboard

1. **Crear Servicio Web**:
   - Ve a [Render Dashboard](https://dashboard.render.com)
   - **New** > **Blueprint** > **Docker**
   - Conecta tu repositorio de GitHub

2. **Configurar Servicio**:
   ```
   Nombre: delfos-biomarkers
   Runtime: Docker
   Dockerfile Path: ./Dockerfile
   Start Command: ./start_services.sh
   ```

3. **Variables de Entorno**:
   ```bash
   PYTHON_VERSION=3.12
   PORT=8000
   MLFLOW_TRACKING_URI=https://delfos-biomarkers.onrender.com/mlflow
   RENDER=true
   ```

4. **Disco Persistente**:
   ```
   Mount Path: /app
   Size: 10 GB
   ```

5. **Desplegar**: Click en **"Create Web Service"**

## 📊 URLs de Acceso

Después del despliegue exitoso:

- **🌐 Aplicación**: `https://delfos-biomarkers.onrender.com`
- **🔬 MLflow UI**: `https://delfos-biomarkers.onrender.com`
- **🔌 API Docs**: `https://delfos-biomarkers.onrender.com/docs`
- **📱 Dashboard**: `https://delfos-biomarkers.onrender.com`

## 🔍 Verificación del Despliegue

### Verificación Automática
```bash
./verify_render_deployment.sh https://delfos-biomarkers.onrender.com
```

### Verificación Manual
```bash
# Health check
curl https://delfos-biomarkers.onrender.com/health

# API documentation
curl https://delfos-biomarkers.onrender.com/docs

# Test prediction
curl -X POST https://delfos-biomarkers.onrender.com/predict \
  -H "Content-Type: application/json" \
  -d '{"edad": 45, "sexo": "F", ...}'
```

## 🛠️ Gestión del Servicio

### Comandos CLI
```bash
render logs                    # Ver logs en tiempo real
render open                    # Abrir aplicación en navegador
render restart                 # Reiniciar servicio
render env                     # Ver variables de entorno
render scale 2                 # Escalar a 2 instancias
```

### Dashboard de Render
- **Logs**: Tiempo real con filtros
- **Metrics**: CPU, memoria, red, response time
- **Settings**: Configuración y variables de entorno
- **Activity**: Historial de despliegues

## 🔧 Características de Render

✅ **Despliegue automático** desde GitHub
✅ **SSL automático** y gratuito
✅ **Escalado automático** según demanda
✅ **Disco persistente** de 10 GB
✅ **Base de datos PostgreSQL** integrada opcional
✅ **Caché Redis** opcional
✅ **Logs en tiempo real**
✅ **Zero-downtime deployments**
✅ **Variables de entorno** encriptadas

## 📋 Checklist de Despliegue

- [x] Configuración de `render.yaml`
- [x] Dockerfile optimizado para Render
- [x] Script de inicio de servicios
- [x] Variables de entorno configuradas
- [x] Health checks implementados
- [x] Disco persistente configurado
- [x] Scripts de verificación y pruebas
- [x] Documentación completa

## 🔐 Seguridad

- ✅ **HTTPS automático** con Let's Encrypt
- ✅ **Variables de entorno** encriptadas
- ✅ **Firewall configurado** automáticamente
- ✅ **Acceso restringido** a servicios internos
- ✅ **Logs seguros** sin exposición de secrets

## 💾 Persistencia

- ✅ **10 GB disco persistente** en `/app`
- ✅ **Modelos MLflow** guardados automáticamente
- ✅ **Persistencia** entre despliegues
- ✅ **Backups automáticos** de base de datos

## 📈 Escalado

- ✅ **Auto-scaling** activado por defecto
- ✅ **Escalado horizontal** hasta 100 instancias
- ✅ **Escalado vertical** hasta 8 GB RAM
- ✅ **Load balancing** automático

## 🔄 Actualizaciones

- ✅ **Despliegue automático** al hacer push a GitHub
- ✅ **Zero-downtime** deployments
- ✅ **Rollback automático** en caso de error
- ✅ **Historial completo** de despliegues

## 🐛 Troubleshooting

### Problemas Comunes
```bash
# Ver logs detallados
render logs --tail 100

# Reiniciar servicio
render restart

# Verificar variables de entorno
render env

# Escalar recursos
render scale --cpu 2 --memory 4GB
```

### Problema: Memoria Insuficiente
```bash
# Ver uso de memoria
render logs | grep "memory"

# Escalar en Dashboard o con CLI
render scale --memory 2GB
```

### Problema: Modelos no Cargan
```bash
# Verificar archivos en disco
render shell
ls -la /app/mlruns/

# Verificar permisos
chmod -R 755 /app/mlruns/
```

## 💰 Costos

### Plan Gratuito
- ✅ **512 MB RAM**, **0.5 vCPU**
- ✅ **100 GB ancho de banda/mes**
- ✅ **Despliegues ilimitados**
- ✅ **SSL gratuito**

### Plan Profesional ($7/mes)
- ✅ **2 GB RAM**, **1 vCPU**
- ✅ **25 GB disco persistente**
- ✅ **Soporte prioritario**

## 📞 Soporte

- **Dashboard**: [dashboard.render.com](https://dashboard.render.com)
- **Documentación**: [render.com/docs](https://render.com/docs)
- **Estado**: [status.render.com](https://status.render.com)
- **Comunidad**: [community.render.com](https://community.render.com)

## 🎯 Próximos Pasos

1. **Configurar dominio personalizado**
   ```bash
   render domain add your-domain.com
   ```

2. **Agregar base de datos PostgreSQL**
   ```bash
   # En Render Dashboard: New > PostgreSQL
   ```

3. **Configurar monitoreo avanzado**
   ```bash
   # Integrar con servicios externos
   ```

4. **Configurar CI/CD con GitHub Actions**
   ```bash
   # Despliegue automático en push
   ```

---

**¡Tu Sistema de Biomarcadores Digitales está listo para producción en Render! 🚀**

Para más detalles, consulta `RENDER_DEPLOYMENT.md`.