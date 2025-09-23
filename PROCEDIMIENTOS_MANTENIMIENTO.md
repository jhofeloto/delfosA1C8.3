# 🔧 Procedimientos de Mantenimiento

## 🏥 Sistema Predictivo de Diabetes Mellitus Tipo 2

Este documento describe los procedimientos completos de mantenimiento para el sistema en producción, incluyendo monitoreo, actualizaciones, backups, y resolución de problemas.

---

## 📋 Resumen de Mantenimiento

### 🔄 Frecuencia de Actividades:

| Actividad | Frecuencia | Responsable | Criticidad |
|-----------|------------|-------------|------------|
| Health Checks | Cada 5 min | Sistema | Crítica |
| Monitoreo Logs | Continua | Equipo DevOps | Alta |
| Backup Modelos | Diario | Sistema | Alta |
| Actualización Dependencias | Mensual | Equipo Dev | Media |
| Revisión Seguridad | Trimestral | Equipo Seguridad | Alta |
| Auditoría Rendimiento | Semestral | Equipo DevOps | Media |

### 🏥 Servicios a Mantener:
- ✅ **API REST** (`diabetes-api`) - Puerto 8002
- ✅ **Streamlit Dashboard** (`diabetes-streamlit`) - Puerto 8501
- ✅ **MLflow UI** (`diabetes-mlflow`) - Puerto 5000
- ✅ **PostgreSQL Database** (`diabetes-db`) - Puerto 5432

---

## 🏥 Monitoreo del Sistema

### Health Checks Automáticos

#### 1. Health Check API
```bash
# Comando
curl -s https://diabetes-api-xxxx.onrender.com/health | jq '.'

# Respuesta esperada
{
  "status": "healthy",
  "timestamp": "2025-09-23T00:57:26.481Z",
  "version": "2.0.0",
  "model_loaded": true,
  "total_predictions": 150
}
```

#### 2. Health Check Streamlit
```bash
# Comando
curl -f -I https://diabetes-streamlit-xxxx.onrender.com/

# Respuesta esperada
HTTP/2 200
content-type: text/html; charset=utf-8
```

#### 3. Health Check MLflow
```bash
# Comando
curl -f -I https://diabetes-mlflow-xxxx.onrender.com/

# Respuesta esperada
HTTP/2 200
```

### Métricas Críticas a Monitorear

#### 1. Métricas de Rendimiento:
```bash
# Tiempo de respuesta API
curl -o /dev/null -s -w "%{time_total}\n" https://diabetes-api-xxxx.onrender.com/health

# Uso de CPU y Memoria (Render Dashboard)
# - CPU < 80%
# - Memoria < 80%
# - Response Time < 5 segundos
```

#### 2. Métricas de Calidad:
```bash
# Tasa de éxito de predicciones
# - Error Rate < 1%
# - Model Accuracy > 85%
# - Prediction Consistency > 95%
```

#### 3. Métricas de Disponibilidad:
```bash
# Uptime del sistema
# - API Availability > 99.5%
# - Dashboard Availability > 99%
# - Database Availability > 99.9%
```

---

## 📊 Logs y Alertas

### Configuración de Logs

#### 1. Logs de API:
```bash
# Ubicación: Render Dashboard > Servicio > Logs
# Contenido:
# - Request/Response logs
# - Error logs
# - Model loading logs
# - Prediction logs
```

#### 2. Logs de Streamlit:
```bash
# Ubicación: Render Dashboard > Servicio > Logs
# Contenido:
# - User interactions
# - File upload logs
# - Visualization errors
# - Session management
```

#### 3. Logs de MLflow:
```bash
# Ubicación: Render Dashboard > Servicio > Logs
# Contenido:
# - Model tracking
# - Experiment logs
# - UI access logs
```

### Sistema de Alertas

#### 1. Alertas Automáticas en Render:
```bash
# Configurar en Render Dashboard:
# - CPU Usage > 80% (Warning)
# - Memory Usage > 85% (Critical)
# - Response Time > 5s (Warning)
# - Error Rate > 5% (Critical)
# - Service Down (Critical)
```

#### 2. Alertas Personalizadas:
```bash
#!/bin/bash
# Script: alert_system.sh

API_URL="https://diabetes-api-xxxx.onrender.com"

# Verificar health check
if ! curl -f -s "$API_URL/health" > /dev/null; then
    echo "$(date): API DOWN - Enviando alerta" | tee -a /var/log/system_alerts.log
    # Enviar email/SMS
    echo "API del Sistema de Diabetes no responde" | mail -s "CRITICAL: API Down" admin@hospital.com
fi

# Verificar modelo cargado
HEALTH_STATUS=$(curl -s "$API_URL/health" | jq -r '.model_loaded')
if [ "$HEALTH_STATUS" != "true" ]; then
    echo "$(date): Model Not Loaded - Enviando alerta" | tee -a /var/log/system_alerts.log
    echo "Modelo de ML no cargado en API" | mail -s "WARNING: Model Loading Issue" admin@hospital.com
fi
```

---

## 🔄 Actualizaciones del Sistema

### Procedimiento de Actualización

#### 1. Preparación:
```bash
# 1. Crear backup del estado actual
git tag "backup-$(date +%Y%m%d-%H%M%S)"

# 2. Crear branch de actualización
git checkout -b "update-$(date +%Y%m%d)"

# 3. Actualizar código
# - Revisar cambios necesarios
# - Actualizar dependencias si es requerido
# - Probar cambios localmente
```

#### 2. Deploy:
```bash
# 1. Commit de cambios
git add .
git commit -m "Actualización del sistema - $(date)"

# 2. Push a GitHub
git push origin main

# 3. Render detectará automáticamente y hará deploy
# - Monitorear logs de deploy
# - Verificar health checks después del deploy
```

#### 3. Verificación Post-Deploy:
```bash
# 1. Verificar servicios
curl -f https://diabetes-api-xxxx.onrender.com/health
curl -f -I https://diabetes-streamlit-xxxx.onrender.com/
curl -f -I https://diabetes-mlflow-xxxx.onrender.com/

# 2. Probar funcionalidad
curl -X POST https://diabetes-api-xxxx.onrender.com/predict \
  -H "Content-Type: application/json" \
  -d '{"edad": 45, "sexo": "M", "imc": 25.5, ...}'

# 3. Verificar logs por errores
```

#### 4. Rollback (si es necesario):
```bash
# 1. Revertir en GitHub
git revert HEAD
git push origin main

# 2. O deploy del tag de backup
git checkout "backup-$(date +%Y%m%d-%H%M%S)"
git push origin main
```

---

## 💾 Backups y Recuperación

### Estrategia de Backups

#### 1. Backups Automáticos (Render):
```bash
# PostgreSQL:
# - Snapshots diarios automáticos (Render)
# - Retención: 7 días
# - Ubicación: Render Dashboard > Database > Backups

# Modelos de ML:
# - Versionados en Git
# - Backup en MLflow
# - Retención: Permanente
```

#### 2. Backup Manual de Modelos:
```bash
#!/bin/bash
# Script: backup_models.sh

BACKUP_DIR="/app/backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Crear directorio de backup
mkdir -p "$BACKUP_DIR/$TIMESTAMP"

# Backup modelos
cp -r /app/models/* "$BACKUP_DIR/$TIMESTAMP/"
cp -r /app/mlruns/* "$BACKUP_DIR/$TIMESTAMP/"

# Backup configuración
cp /app/requirements.txt "$BACKUP_DIR/$TIMESTAMP/"
cp /app/config.py "$BACKUP_DIR/$TIMESTAMP/"

# Comprimir
cd "$BACKUP_DIR"
tar -czf "backup_$TIMESTAMP.tar.gz" "$TIMESTAMP/"

# Limpiar backups antiguos (mantener 7 días)
find "$BACKUP_DIR" -name "backup_*.tar.gz" -mtime +7 -delete

echo "Backup completado: $BACKUP_DIR/backup_$TIMESTAMP.tar.gz"
```

#### 3. Recuperación de Backup:
```bash
#!/bin/bash
# Script: restore_backup.sh

BACKUP_FILE="/app/backups/backup_20250923_120000.tar.gz"

# Extraer backup
cd /app
tar -xzf "$BACKUP_FILE"

# Restaurar modelos
cp -r /app/20250923_120000/models/* /app/models/
cp -r /app/20250923_120000/mlruns/* /app/mlruns/

# Reiniciar servicios
# (Render lo hará automáticamente con el próximo deploy)

echo "Restauración completada desde: $BACKUP_FILE"
```

---

## 🔧 Mantenimiento de Base de Datos

### Optimización de PostgreSQL

#### 1. Monitoreo de Base de Datos:
```bash
# Verificar conexiones activas
# - Máximo 10 conexiones simultáneas
# - Sin conexiones idle por mucho tiempo

# Verificar tamaño de tablas
# - Logs table < 1GB
# - Predictions table < 5GB

# Verificar índices
# - Índices en columnas de búsqueda
# - Índices optimizados
```

#### 2. Limpieza de Datos:
```bash
#!/bin/bash
# Script: clean_database.sh

# Eliminar logs antiguos (> 30 días)
# Eliminar predicciones anónimas (> 90 días)
# Optimizar tablas
# Recrear índices si es necesario

echo "Limpieza de base de datos completada"
```

#### 3. Backup de Base de Datos:
```bash
# Render hace backups automáticos
# Para backup manual:
pg_dump $DATABASE_URL > diabetes_backup_$(date +%Y%m%d).sql

# Para restaurar:
psql $DATABASE_URL < diabetes_backup_20250923.sql
```

---

## 🤖 Mantenimiento de Modelos de ML

### Actualización de Modelos

#### 1. Entrenamiento de Nuevos Modelos:
```bash
# 1. Preparar nuevos datos
python data_generator.py --n_samples 10000

# 2. Entrenar modelos
python model_trainer.py --experiment_name "Production_Update"

# 3. Evaluar rendimiento
python test_models.py --model_path models/new_model.joblib

# 4. Si es mejor, reemplazar modelo actual
cp models/new_model.joblib models/best_model.joblib
```

#### 2. Validación de Modelos:
```bash
# 1. Verificar métricas
python -c "
from predictor import DiabetesPredictor
p = DiabetesPredictor()
info = p.get_model_info()
print(f'R2 Score: {info[\"r2_score\"]}')
print(f'Features: {info[\"n_features\"]}')
"

# 2. Probar con datos conocidos
# - Usar dataset de validación
# - Verificar consistencia de predicciones
# - Validar categorías de salida
```

#### 3. Deploy de Nuevos Modelos:
```bash
# 1. Subir modelo a repositorio
git add models/new_model.joblib
git commit -m "Nuevo modelo de producción - $(date)"
git push origin main

# 2. Render hará deploy automático
# 3. Verificar que el modelo cargue correctamente
curl -s https://diabetes-api-xxxx.onrender.com/model/info | jq '.'
```

---

## 🔒 Mantenimiento de Seguridad

### Actualizaciones de Seguridad

#### 1. Dependencias:
```bash
# Verificar vulnerabilidades
pip install safety
safety check

# Actualizar dependencias críticas
pip install --upgrade fastapi uvicorn streamlit

# Verificar después de actualización
safety check
```

#### 2. Configuración de Seguridad:
```bash
# Verificar variables de entorno
# - SECRET_KEY configurada
# - JWT_SECRET_KEY configurada
# - No credenciales en código

# Verificar CORS
# - Solo dominios autorizados
# - Headers de seguridad

# Verificar HTTPS
# - Certificados válidos
# - Redirección HTTP -> HTTPS
```

#### 3. Auditoría de Seguridad:
```bash
# Revisar logs de acceso
# - IPs sospechosas
# - Intentos de acceso no autorizado
# - Patrones de uso inusuales

# Verificar permisos
# - Archivos con permisos correctos
# - Variables de entorno seguras
```

---

## 📈 Optimización de Rendimiento

### Monitoreo de Rendimiento

#### 1. Métricas de API:
```bash
# Tiempo de respuesta
curl -o /dev/null -s -w "Response Time: %{time_total}s\n" \
  https://diabetes-api-xxxx.onrender.com/health

# Throughput
# - Predicciones por minuto
# - Requests por segundo
```

#### 2. Uso de Recursos:
```bash
# CPU y Memoria (Render Dashboard)
# - Promedio < 70%
# - Picos < 90%

# Base de datos
# - Conexiones < 10
# - Queries lentas < 1%
```

#### 3. Optimizaciones:
```bash
# Si hay problemas de rendimiento:

# 1. Optimizar carga de modelos
# - Lazy loading
# - Model caching

# 2. Optimizar consultas DB
# - Índices apropiados
# - Queries eficientes

# 3. Escalar recursos si es necesario
# - Aumentar CPU/Memoria en Render
# - Optimizar configuración
```

---

## 🚨 Resolución de Problemas

### Procedimiento de Troubleshooting

#### 1. Identificar el Problema:
```bash
# 1. Verificar health checks
curl -s https://diabetes-api-xxxx.onrender.com/health | jq '.'

# 2. Revisar logs recientes
# - Render Dashboard > Logs
# - Buscar errores

# 3. Verificar métricas
# - CPU/Memoria
# - Response times
```

#### 2. Problemas Comunes y Soluciones:

**API no responde:**
```bash
# 1. Verificar si el servicio está corriendo
curl -f -I https://diabetes-api-xxxx.onrender.com/health

# 2. Revisar logs por errores de startup
# 3. Verificar variables de entorno
# 4. Reiniciar servicio si es necesario
```

**Modelo no carga:**
```bash
# 1. Verificar que el modelo existe
ls -la models/

# 2. Verificar integridad del archivo
file models/best_model.joblib

# 3. Revisar logs de carga del modelo
# 4. Re-entrenar modelo si es necesario
```

**Base de datos no conecta:**
```bash
# 1. Verificar variables de entorno
echo $DATABASE_URL

# 2. Probar conexión manual
psql $DATABASE_URL -c "SELECT 1;"

# 3. Verificar estado del servicio de BD
# 4. Revisar logs de conexión
```

**Rendimiento lento:**
```bash
# 1. Verificar uso de recursos
# 2. Identificar bottlenecks
# 3. Optimizar queries lentas
# 4. Considerar escalado
```

#### 3. Escalación de Problemas:
```bash
# Si no se puede resolver:

# 1. Documentar el problema
# - Síntomas
# - Pasos para reproducir
# - Logs relevantes

# 2. Notificar al equipo
# - Equipo de desarrollo
# - Equipo de DevOps
# - Stakeholders

# 3. Implementar solución temporal
# - Workaround
# - Rollback si es necesario
```

---

## 📋 Checklist de Mantenimiento

### Mantenimiento Diario:
- [ ] ✅ Health checks funcionando
- [ ] ✅ Logs revisados por errores
- [ ] ✅ Métricas de rendimiento revisadas
- [ ] ✅ Backups automáticos verificados

### Mantenimiento Semanal:
- [ ] ✅ Pruebas de funcionalidad completas
- [ ] ✅ Revisión de logs de seguridad
- [ ] ✅ Optimización de consultas DB
- [ ] ✅ Verificación de modelos

### Mantenimiento Mensual:
- [ ] ✅ Actualización de dependencias
- [ ] ✅ Revisión de configuración
- [ ] ✅ Pruebas de carga
- [ ] ✅ Auditoría de seguridad

### Mantenimiento Trimestral:
- [ ] ✅ Revisión completa del sistema
- [ ] ✅ Actualización de modelos si es necesario
- [ ] ✅ Optimización de rendimiento
- [ ] ✅ Planificación de mejoras

---

## 📞 Contactos y Soporte

### Equipo de Mantenimiento:
- **DevOps:** devops@hospital.com
- **Desarrollo:** desarrollo@sistemadiabetes.com
- **Seguridad:** seguridad@hospital.com
- **Soporte:** soporte@sistemadiabetes.com

### Recursos de Soporte:
- 📚 Documentación: `/docs` en API
- 🔄 Estado del Sistema: `/health` endpoint
- 📊 Métricas: Render Dashboard
- 🐛 Reportes: GitHub Issues

### Niveles de Severidad:
- 🔴 **Crítico:** Sistema no funcional - Respuesta inmediata
- 🟡 **Alto:** Funcionalidad afectada - Respuesta en 2 horas
- 🟢 **Medio:** Problema menor - Respuesta en 24 horas
- 🔵 **Bajo:** Mejora o consulta - Respuesta en 1 semana

---

## 📈 Mejoras Continuas

### Métricas de Mantenimiento:
```bash
# Tiempo promedio de resolución
# - Incidentes críticos: < 1 hora
# - Incidentes altos: < 4 horas
# - Incidentes medios: < 24 horas

# Disponibilidad del sistema
# - Uptime > 99.5%
# - MTTR < 2 horas
# - MTBF > 30 días
```

### Plan de Mejoras:
```bash
# Próximas mejoras:
# - Automatización de backups
# - Monitoreo avanzado
# - CI/CD mejorado
# - Documentación actualizada
# - Entrenamiento del equipo
```

---

**📅 Última actualización:** Septiembre 2025
**🏥 Versión del Sistema:** 2.0.0
**✅ Estado de Mantenimiento:** Operativo