# 🚀 Despliegue en Render - Sistema de Biomarcadores Digitales

Este documento describe el proceso completo de despliegue del Sistema de Biomarcadores Digitales en **Render**.

## 📋 Resumen del Despliegue

Render es una plataforma de despliegue moderna que ofrece:
- ✅ **Despliegue automático** desde GitHub
- ✅ **Escalado automático** según demanda
- ✅ **Base de datos PostgreSQL** integrada
- ✅ **Caché Redis** opcional
- ✅ **SSL automático** y gratuito
- ✅ **Logs en tiempo real**
- ✅ **Variables de entorno** seguras

## 🏗️ Arquitectura en Render

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Render App    │    │   PostgreSQL    │    │     Redis       │
│                 │    │   Database      │    │     Cache       │
│ • API Service   │    │                 │    │                 │
│ • MLflow UI     │    │ • Patient Data  │    │ • Session Cache │
│ • Dashboard     │    │ • Model Metrics │    │ • API Responses │
│ • Model Server  │    │ • Audit Logs    │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │   External      │
                    │   Services      │
                    │                 │
                    │ • HL7 FHIR      │
                    │ • Dify.ai       │
                    │ • Medical APIs  │
                    └─────────────────┘
```

## 📁 Archivos de Configuración

### `render.yaml`
Configuración principal de Render con servicios y variables de entorno.

### `Dockerfile`
Imagen Docker optimizada para Render con usuario no-root y health checks.

### `start_services.sh`
Script de orquestación de servicios optimizado para Render.

### `deploy_render.sh`
Script de preparación para despliegue en Render.

### `verify_render_deployment.sh`
Script de verificación y pruebas del despliegue.

## 🚀 Proceso de Despliegue

### Paso 1: Preparación Local

```bash
# Ejecutar script de preparación
./deploy_render.sh
```

Este script:
- ✅ Verifica archivos necesarios
- ✅ Hace commit de cambios
- ✅ Sube cambios a GitHub
- ✅ Proporciona instrucciones detalladas

### Paso 2: Configuración en Render Dashboard

#### 1. Crear Nuevo Servicio
1. Ve a [Render Dashboard](https://dashboard.render.com)
2. Click en **"New"** > **"Blueprint"**
3. Selecciona **"Docker"** como runtime
4. Conecta tu repositorio de **GitHub**

#### 2. Configurar Servicio Web
```
Nombre: delfos-biomarkers
Runtime: Docker
Dockerfile Path: ./Dockerfile
Build Command: (dejar vacío)
Start Command: ./start_services.sh
```

#### 3. Variables de Entorno
```bash
PYTHON_VERSION=3.12
PORT=8000
MLFLOW_TRACKING_URI=https://delfos-biomarkers.onrender.com/mlflow
RENDER=true
```

#### 4. Configuración de Disco Persistente
```
Mount Path: /app
Size: 10 GB
```

#### 5. Health Check
```
Path: /health
Interval: 30 seconds
```

### Paso 3: Desplegar

1. Click en **"Create Web Service"**
2. Espera a que termine el despliegue (5-10 minutos)
3. Verifica que el servicio esté **"Live"**

## 🔧 Configuración Avanzada

### Base de Datos PostgreSQL

#### Crear Base de Datos
1. En Render Dashboard: **"New"** > **"PostgreSQL"**
2. Nombre: `delfos-postgres`
3. Database Name: `delfos_medical`

#### Variables de Entorno
```bash
DATABASE_URL=postgresql://user:pass@host:5432/delfos_medical
```

### Caché Redis (Opcional)

#### Crear Redis
1. En Render Dashboard: **"New"** > **"Redis"**
2. Nombre: `delfos-redis`

#### Variables de Entorno
```bash
REDIS_URL=redis://host:port
```

## 📊 URLs de Acceso

Después del despliegue exitoso:

- **🌐 Aplicación Principal**: `https://delfos-biomarkers.onrender.com`
- **🔬 MLflow UI**: `https://delfos-biomarkers.onrender.com`
- **🔌 API Documentation**: `https://delfos-biomarkers.onrender.com/docs`
- **📱 Dashboard**: `https://delfos-biomarkers.onrender.com`

## 🔍 Verificación del Despliegue

### Verificación Automática
```bash
./verify_render_deployment.sh https://delfos-biomarkers.onrender.com
```

### Verificación Manual

#### Health Check
```bash
curl https://delfos-biomarkers.onrender.com/health
```

#### API Documentation
```bash
curl https://delfos-biomarkers.onrender.com/docs
```

#### Prueba de Predicción
```bash
curl -X POST https://delfos-biomarkers.onrender.com/predict \
  -H "Content-Type: application/json" \
  -d '{
    "edad": 45,
    "sexo": "F",
    "peso": 70.5,
    "altura": 165,
    "presion_sistolica": 120,
    "presion_diastolica": 80,
    "glucosa": 95,
    "colesterol_total": 180,
    "colesterol_hdl": 50,
    "colesterol_ldl": 110,
    "trigliceridos": 150,
    "imc": 25.8,
    "perimetro_abdominal": 85,
    "actividad_fisica": "moderada",
    "historial_familiar": "si",
    "tabaquismo": "no",
    "consumo_alcohol": "ocasional"
  }'
```

## 🛠️ Gestión del Servicio

### Comandos CLI de Render
```bash
# Ver logs
render logs

# Abrir aplicación
render open

# Reiniciar servicio
render restart

# Ver variables de entorno
render env

# Escalar servicio
render scale 2
```

### Monitoreo en Dashboard
1. Ve a [Render Dashboard](https://dashboard.render.com)
2. Selecciona tu servicio `delfos-biomarkers`
3. Revisa las pestañas:
   - **Logs**: Logs en tiempo real
   - **Metrics**: Uso de CPU, memoria, etc.
   - **Settings**: Configuración del servicio

## 🔐 Seguridad

### SSL/TLS
- ✅ **Automático y gratuito** por Render
- ✅ **Certificados Let's Encrypt**
- ✅ **HTTPS por defecto** en todos los endpoints

### Variables de Entorno
- ✅ **Encriptadas** en Render
- ✅ **No visibles** en logs
- ✅ **Acceso restringido** por roles

### Firewall
- ✅ **Configurado automáticamente** por Render
- ✅ **Solo puertos necesarios** expuestos
- ✅ **Tráfico interno** entre servicios

## 💾 Persistencia de Datos

### Disco Persistente
- ✅ **10 GB** configurados en `/app`
- ✅ **Persistencia** entre despliegues
- ✅ **Modelos MLflow** guardados automáticamente

### Base de Datos
- ✅ **Backups automáticos** por Render
- ✅ **Point-in-time recovery**
- ✅ **Alta disponibilidad**

## 📈 Escalado

### Escalado Horizontal
```bash
# Escalar a 2 instancias
render scale 2
```

### Escalado Vertical
En Render Dashboard:
- **CPU**: 0.5 - 4 vCPUs
- **Memoria**: 512 MB - 8 GB
- **Configuración automática** según plan

### Auto-scaling
- ✅ **Activado por defecto**
- ✅ **Basado en uso de CPU**
- ✅ **Mínimo 1, máximo según plan**

## 🔄 Actualizaciones

### Despliegue Automático
1. Haz push a la rama conectada en GitHub
2. Render detecta cambios automáticamente
3. Se inicia despliegue automático
4. Zero-downtime deployment

### Rollback
1. En Render Dashboard > **Activity**
2. Selecciona despliegue anterior
3. Click **"Rollback"**

## 🐛 Troubleshooting

### Problema: Despliegue Fallido
```bash
# Ver logs detallados
render logs --tail 100

# Verificar variables de entorno
render env

# Reiniciar servicio
render restart
```

### Problema: Servicios no Inician
```bash
# Verificar logs de construcción
render logs --build

# Verificar configuración de puertos
render env | grep PORT
```

### Problema: Memoria Insuficiente
```bash
# Ver uso de memoria
render logs | grep "memory"

# Escalar verticalmente en Dashboard
# o usar: render scale --cpu 2 --memory 4GB
```

### Problema: Modelos no Cargan
```bash
# Verificar archivos en disco persistente
render shell
ls -la /app/mlruns/

# Verificar permisos
chmod -R 755 /app/mlruns/
```

## 📊 Monitoreo y Alertas

### Métricas Disponibles
- CPU Usage
- Memory Usage
- Network I/O
- Response Time
- Error Rate

### Configurar Alertas
1. Render Dashboard > **Settings** > **Alerts**
2. Configurar notificaciones por email/Slack
3. Umbrales personalizables

## 💰 Costos

### Plan Gratuito
- ✅ **512 MB RAM**
- ✅ **0.5 vCPU**
- ✅ **100 GB ancho de banda**
- ✅ **SSL gratuito**
- ✅ **Despliegues ilimitados**

### Plan Profesional ($7/mes)
- ✅ **2 GB RAM**
- ✅ **1 vCPU**
- ✅ **25 GB disco persistente**
- ✅ **Prioridad en soporte**

### Base de Datos
- ✅ **PostgreSQL gratuito** (512 MB)
- ✅ **Planes pagos** desde $7/mes

## 📞 Soporte

### Documentación
- [Render Docs](https://render.com/docs)
- [Render Community](https://community.render.com)
- [Render Status](https://status.render.com)

### Contacto
- **Soporte**: support@render.com
- **Estado del servicio**: status.render.com
- **Comunidad**: Discord/Forums

## 🎯 Mejores Prácticas

### Optimización de Rendimiento
1. **Usar disco persistente** para modelos ML
2. **Configurar health checks** apropiados
3. **Monitorear uso de recursos**
4. **Optimizar imágenes Docker**

### Seguridad
1. **Usar variables de entorno** para secrets
2. **Configurar HTTPS** obligatorio
3. **Limitar acceso** a servicios internos
4. **Monitorear logs** regularmente

### Mantenimiento
1. **Actualizar dependencias** regularmente
2. **Monitorear métricas** de rendimiento
3. **Configurar backups** automáticos
4. **Probar actualizaciones** en staging

---

**¡Tu Sistema de Biomarcadores Digitales está listo para producción en Render! 🚀**

Para más información, consulta la documentación oficial de [Render](https://render.com/docs).