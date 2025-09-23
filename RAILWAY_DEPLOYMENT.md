# 🚀 Despliegue en Railway - Sistema de Biomarcadores Digitales

Este documento describe el proceso de despliegue del Sistema de Biomarcadores Digitales en Railway.

## 📋 Requisitos Previos

### 1. Railway CLI
```bash
npm install -g @railway/cli
```

### 2. Cuenta Railway
- Crear cuenta en [Railway](https://railway.app)
- Instalar Railway CLI y autenticarse

### 3. Repositorio Git
- El proyecto debe estar en un repositorio Git
- Hacer commit de todos los cambios

## 🏗️ Arquitectura del Despliegue

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Railway App   │    │   PostgreSQL    │    │     Redis       │
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

## 🔧 Configuración

### 1. Variables de Entorno
```bash
# Configuración de Railway
RAILWAY_ENVIRONMENT=production
PORT=8000

# MLflow
MLFLOW_TRACKING_URI=https://your-app.railway.app/mlflow
MLFLOW_S3_ENDPOINT_URL=https://your-app.railway.app/mlflow-artifacts

# Base de Datos
DATABASE_URL=postgresql://user:pass@host:5432/dbname

# Redis
REDIS_URL=redis://host:port

# API Keys
OPENAI_API_KEY=your-openai-key
DIFY_API_KEY=your-dify-key

# Seguridad
JWT_SECRET_KEY=your-jwt-secret
API_SECRET_KEY=your-api-secret
```

### 2. Servicios Configurados

#### API Service (Puerto 8000)
- **Framework**: FastAPI
- **Funcionalidad**: Endpoints de predicción y gestión de pacientes
- **Workers**: 4 (escalable)
- **Health Check**: `/health`

#### MLflow UI (Puerto 5004)
- **Funcionalidad**: Interfaz de gestión de experimentos ML
- **Backend Store**: Local (mlruns/)
- **Artifact Store**: S3 compatible
- **Health Check**: `/`

#### Dashboard (Puerto 8501)
- **Framework**: Streamlit
- **Funcionalidad**: Interfaz de usuario para predicciones
- **Modo**: Headless
- **Health Check**: `/`

## 🚀 Proceso de Despliegue

### Opción 1: Despliegue Automático (Recomendado)

```bash
# Ejecutar script de despliegue
./deploy_railway.sh
```

### Opción 2: Despliegue Manual

```bash
# 1. Conectar proyecto Railway
railway link

# 2. Configurar variables de entorno
railway variables set PYTHON_VERSION=3.12
railway variables set MLFLOW_TRACKING_URI=https://your-app.railway.app/mlflow

# 3. Desplegar aplicación
railway up

# 4. Ver logs
railway logs

# 5. Abrir aplicación
railway open
```

## 📊 Monitoreo y Logs

### Ver Logs en Tiempo Real
```bash
railway logs --follow
```

### Ver Logs de Servicios Específicos
```bash
railway logs --service api
railway logs --service mlflow
railway logs --service dashboard
```

### Estado de la Aplicación
```bash
railway status
```

## 🔍 Health Checks

### API Service
```bash
curl https://your-app.railway.app/health
```

### MLflow UI
```bash
curl https://your-app.railway.app/
```

### Dashboard
```bash
curl https://your-app.railway.app/
```

## 🛠️ Troubleshooting

### Problema: Servicios no inician
```bash
# Ver logs detallados
railway logs --tail 100

# Reiniciar servicios
railway service restart api
railway service restart mlflow
railway service restart dashboard
```

### Problema: Puerto ocupado
```bash
# Ver puertos en uso
railway exec lsof -i :8000
railway exec lsof -i :5004
railway exec lsof -i :8501
```

### Problema: Memoria insuficiente
```bash
# Ver uso de memoria
railway exec free -h

# Escalar recursos
railway service scale api --cpu 2 --memory 2GB
```

### Problema: Modelos no cargan
```bash
# Verificar archivos de modelos
railway exec ls -la mlruns/

# Verificar permisos
railway exec chmod -R 755 mlruns/
```

## 📈 Escalado

### Escalar Horizontalmente
```bash
# Escalar API service
railway service scale api --replicas 3

# Escalar Dashboard
railway service scale dashboard --replicas 2
```

### Escalar Verticalmente
```bash
# Aumentar recursos de API
railway service scale api --cpu 2 --memory 4GB

# Aumentar recursos de MLflow
railway service scale mlflow --cpu 1 --memory 2GB
```

## 🔄 Actualizaciones

### Despliegue de Nuevas Versiones
```bash
# Hacer commit de cambios
git add .
git commit -m "Nueva versión del modelo"
git push

# Railway detectará cambios automáticamente y redeployará
```

### Rollback
```bash
# Ver historial de despliegues
railway releases

# Hacer rollback a versión anterior
railway rollback <release-id>
```

## 🔒 Seguridad

### Configuración de Firewall
```bash
# Configurar reglas de firewall en Railway Dashboard
# Permitir solo puertos necesarios: 8000, 5004, 8501
```

### SSL/TLS
```bash
# Railway proporciona SSL automático
# Todos los endpoints usan HTTPS por defecto
```

### Autenticación
```bash
# Configurar API keys
railway variables set API_SECRET_KEY=your-secret-key

# Configurar JWT
railway variables set JWT_SECRET_KEY=your-jwt-secret
```

## 💾 Backup y Recuperación

### Backup Automático
```bash
# Railway hace backups automáticos de la base de datos
# Configurar en Railway Dashboard > Database > Backups
```

### Backup Manual
```bash
# Backup de modelos MLflow
railway exec tar -czf mlruns_backup.tar.gz mlruns/

# Descargar backup
railway exec cat mlruns_backup.tar.gz | base64 -d > mlruns_backup.tar.gz
```

## 📞 Soporte

### Contacto Railway
- **Documentación**: [Railway Docs](https://docs.railway.app)
- **Soporte**: [Railway Support](https://railway.app/support)
- **Comunidad**: [Railway Discord](https://discord.gg/railway)

### Logs de Error
```bash
# Capturar logs de error
railway logs --level error > error_logs.txt

# Enviar a soporte
cat error_logs.txt | railway support
```

## 🎯 Próximos Pasos

1. **Configurar dominio personalizado**
   ```bash
   railway domain add your-domain.com
   ```

2. **Configurar monitoreo avanzado**
   ```bash
   # Integrar con servicios de monitoreo externos
   railway variables set MONITORING_URL=https://your-monitoring-service.com
   ```

3. **Configurar CI/CD**
   ```bash
   # Configurar GitHub Actions para despliegue automático
   railway connect --github
   ```

4. **Configurar alertas**
   ```bash
   # Configurar notificaciones por email/Slack
   railway alerts add --email your-email@domain.com
   ```

---

**¡Feliz despliegue! 🚀**

Para más información, consulta la [documentación oficial de Railway](https://docs.railway.app).