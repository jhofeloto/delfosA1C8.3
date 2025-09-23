# 🔍 Verificación de Despliegue en Render

## 🏥 Sistema Predictivo de Diabetes Mellitus Tipo 2

Este documento contiene scripts y comandos para verificar el correcto funcionamiento del despliegue en Render.

---

## 📋 Scripts de Verificación

### 1. Verificación Básica de Servicios

```bash
#!/bin/bash
# Script: verify_basic_services.sh

echo "🔍 Verificando servicios básicos..."

# Variables (ajustar según URLs de Render)
API_URL="https://diabetes-api-xxxx.onrender.com"
STREAMLIT_URL="https://diabetes-streamlit-xxxx.onrender.com"
MLFLOW_URL="https://diabetes-mlflow-xxxx.onrender.com"

echo "🌐 Verificando API REST..."
if curl -f -s "$API_URL/health" > /dev/null; then
    echo "✅ API REST funcionando"
    # Obtener información del health check
    curl -s "$API_URL/health" | jq '.'
else
    echo "❌ API REST no responde"
fi

echo ""
echo "🌐 Verificando Streamlit..."
if curl -f -s -I "$STREAMLIT_URL" | grep -q "200"; then
    echo "✅ Streamlit funcionando"
else
    echo "❌ Streamlit no responde"
fi

echo ""
echo "🌐 Verificando MLflow..."
if curl -f -s -I "$MLFLOW_URL" | grep -q "200"; then
    echo "✅ MLflow funcionando"
else
    echo "❌ MLflow no responde"
fi
```

### 2. Verificación de Funcionalidad de API

```bash
#!/bin/bash
# Script: verify_api_functionality.sh

API_URL="https://diabetes-api-xxxx.onrender.com"

echo "🔍 Verificando funcionalidad de API..."

# Health Check
echo "🏥 Health Check:"
curl -s "$API_URL/health" | jq '.'

echo ""
echo "🤖 Información del Modelo:"
curl -s "$API_URL/model/info" | jq '.'

echo ""
echo "📊 Categorías disponibles:"
curl -s "$API_URL/categories" | jq '.'

echo ""
echo "🔧 Características requeridas:"
curl -s "$API_URL/features" | jq '.'

echo ""
echo "📋 Modelos disponibles:"
curl -s "$API_URL/models" | jq '.'
```

### 3. Prueba de Predicción

```bash
#!/bin/bash
# Script: test_prediction.sh

API_URL="https://diabetes-api-xxxx.onrender.com"

echo "🔮 Probando predicción..."

# Datos de prueba
TEST_DATA='{
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
  "medicamentos_hta": "Si",
  "historia_familiar_dm": "Si",
  "diabetes_gestacional": "No",
  "puntaje_findrisc": 12,
  "riesgo_cardiovascular": 0.4
}'

echo "📤 Enviando datos de predicción..."
echo "Datos: $TEST_DATA"

RESPONSE=$(curl -s -X POST "$API_URL/predict" \
  -H "Content-Type: application/json" \
  -d "$TEST_DATA")

echo ""
echo "📥 Respuesta de predicción:"
echo "$RESPONSE" | jq '.'

# Verificar si la respuesta es válida
if echo "$RESPONSE" | jq -e '.glucose_mg_dl' > /dev/null 2>&1; then
    GLUCOSE=$(echo "$RESPONSE" | jq -r '.glucose_mg_dl')
    CATEGORY=$(echo "$RESPONSE" | jq -r '.category')
    echo ""
    echo "✅ Predicción exitosa:"
    echo "   🩸 Glucosa: $GLUCOSE mg/dL"
    echo "   📊 Categoría: $CATEGORY"
else
    echo ""
    echo "❌ Error en la predicción"
    echo "Respuesta: $RESPONSE"
fi
```

### 4. Verificación de Rendimiento

```bash
#!/bin/bash
# Script: performance_test.sh

API_URL="https://diabetes-api-xxxx.onrender.com"

echo "⚡ Probando rendimiento..."

# Función para medir tiempo de respuesta
measure_time() {
    local start_time=$(date +%s%N)
    curl -s -o /dev/null -w "%{time_total}" "$API_URL/health"
    local end_time=$(date +%s%N)
    local duration=$(( (end_time - start_time) / 1000000 ))
    echo "$duration"
}

echo "📊 Midiendo tiempos de respuesta..."

TIMES=()
for i in {1..5}; do
    TIME=$(measure_time)
    TIMES+=($TIME)
    echo "Prueba $i: ${TIME}ms"
    sleep 1
done

# Calcular estadísticas
SUM=0
for time in "${TIMES[@]}"; do
    SUM=$((SUM + time))
done

AVG=$((SUM / ${#TIMES[@]}))
MIN=${TIMES[0]}
MAX=${TIMES[0]}

for time in "${TIMES[@]}"; do
    if (( time < MIN )); then MIN=$time; fi
    if (( time > MAX )); then MAX=$time; fi
done

echo ""
echo "📈 Estadísticas de rendimiento:"
echo "   Promedio: ${AVG}ms"
echo "   Mínimo: ${MIN}ms"
echo "   Máximo: ${MAX}ms"
```

### 5. Verificación de Logs y Estado

```bash
#!/bin/bash
# Script: check_logs_status.sh

API_URL="https://diabetes-api-xxxx.onrender.com"

echo "📋 Verificando estado del sistema..."

# Health check detallado
echo "🏥 Estado del servicio:"
HEALTH_RESPONSE=$(curl -s "$API_URL/health")
echo "$HEALTH_RESPONSE" | jq '.'

# Extraer información importante
STATUS=$(echo "$HEALTH_RESPONSE" | jq -r '.status')
MODEL_LOADED=$(echo "$HEALTH_RESPONSE" | jq -r '.model_loaded')
TOTAL_PREDICTIONS=$(echo "$HEALTH_RESPONSE" | jq -r '.total_predictions')

echo ""
echo "📊 Resumen del estado:"
echo "   Estado: $STATUS"
echo "   Modelo cargado: $MODEL_LOADED"
echo "   Predicciones totales: $TOTAL_PREDICTIONS"

# Verificar si hay problemas
if [[ "$STATUS" != "healthy" ]]; then
    echo ""
    echo "⚠️ El servicio no está completamente saludable"
fi

if [[ "$MODEL_LOADED" != "true" ]]; then
    echo ""
    echo "❌ El modelo no está cargado correctamente"
fi
```

### 6. Script de Verificación Completa

```bash
#!/bin/bash
# Script: complete_verification.sh

echo "🚀 Iniciando verificación completa del despliegue..."
echo "⏰ $(date)"
echo "=" | tr -d '\n' | head -c 50
echo ""

# Ejecutar todas las verificaciones
echo ""
echo "1️⃣ Verificando servicios básicos..."
bash verify_basic_services.sh

echo ""
echo "2️⃣ Verificando funcionalidad de API..."
bash verify_api_functionality.sh

echo ""
echo "3️⃣ Probando predicción..."
bash test_prediction.sh

echo ""
echo "4️⃣ Verificando rendimiento..."
bash performance_test.sh

echo ""
echo "5️⃣ Verificando logs y estado..."
bash check_logs_status.sh

echo ""
echo "=" | tr -d '\n' | head -c 50
echo ""
echo "✅ Verificación completa finalizada: $(date)"
```

---

## 🖥️ Comandos Manuales de Verificación

### Verificación Rápida:
```bash
# Health check
curl -s https://diabetes-api-xxxx.onrender.com/health | jq '.'

# Información del modelo
curl -s https://diabetes-api-xxxx.onrender.com/model/info | jq '.'

# Prueba de predicción
curl -X POST https://diabetes-api-xxxx.onrender.com/predict \
  -H "Content-Type: application/json" \
  -d '{"edad": 45, "sexo": "M", "imc": 25.5, "tas": 120, "tad": 80, "perimetro_abdominal": 90, "frecuencia_cardiaca": 70, "realiza_ejercicio": "Si", "consume_alcohol": "Nunca", "fuma": "No", "medicamentos_hta": "No", "historia_familiar_dm": "No", "diabetes_gestacional": "No", "puntaje_findrisc": 5, "riesgo_cardiovascular": 0.2}'
```

### Verificación de URLs:
```bash
# API
curl -I https://diabetes-api-xxxx.onrender.com/health

# Streamlit
curl -I https://diabetes-streamlit-xxxx.onrender.com/

# MLflow
curl -I https://diabetes-mlflow-xxxx.onrender.com/
```

### Verificación de Logs:
```bash
# Ver logs recientes (en Render Dashboard)
# 1. Ir a https://dashboard.render.com
# 2. Seleccionar el servicio
# 3. Ir a la pestaña "Logs"
# 4. Buscar errores o warnings
```

---

## 🔧 Solución de Problemas Comunes

### Error 502 Bad Gateway:
```bash
# Verificar si el servicio está iniciando
curl -I https://diabetes-api-xxxx.onrender.com/health

# Ver logs en Render Dashboard
# Buscar errores de carga del modelo
```

### Modelo no Cargado:
```bash
# Verificar información del modelo
curl -s https://diabetes-api-xxxx.onrender.com/model/info | jq '.'

# Verificar que los modelos estén en el repositorio
ls -la models/
ls -la mlruns/
```

### Problemas de Conectividad:
```bash
# Probar conectividad básica
ping diabetes-api-xxxx.onrender.com

# Verificar DNS
nslookup diabetes-api-xxxx.onrender.com

# Probar diferentes endpoints
curl -v https://diabetes-api-xxxx.onrender.com/health
```

---

## 📊 Métricas de Monitoreo

### Comandos para Monitoreo Continuo:

```bash
# Monitoreo básico (ejecutar cada 5 minutos)
while true; do
    echo "$(date): $(curl -s https://diabetes-api-xxxx.onrender.com/health | jq -r '.status')"
    sleep 300
done

# Monitoreo detallado
watch -n 30 'curl -s https://diabetes-api-xxxx.onrender.com/health | jq "."'
```

### Métricas Importantes a Monitorear:
- ✅ Estado del health check
- ✅ Modelo cargado correctamente
- ✅ Tiempo de respuesta < 5 segundos
- ✅ Predicciones funcionando
- ✅ Servicios accesibles

---

## 📋 Checklist de Verificación

### Pre-Verificación:
- [ ] ✅ URLs de servicios identificadas
- [ ] ✅ Scripts de verificación listos
- [ ] ✅ Acceso a Render Dashboard

### Verificación Básica:
- [ ] ✅ API responde a health check
- [ ] ✅ Streamlit es accesible
- [ ] ✅ MLflow UI funciona
- [ ] ✅ Base de datos conectada

### Verificación Funcional:
- [ ] ✅ Predicciones funcionan correctamente
- [ ] ✅ Modelos cargados
- [ ] ✅ Endpoints responden apropiadamente
- [ ] ✅ Datos de entrada validados

### Verificación de Rendimiento:
- [ ] ✅ Tiempo de respuesta < 5 segundos
- [ ] ✅ Servicios estables
- [ ] ✅ Sin errores 5xx
- [ ] ✅ Logs limpios

---

## 🚨 Alertas y Notificaciones

### Configurar Alertas en Render:
1. Ir a Render Dashboard
2. Seleccionar servicio
3. Configurar "Alerts"
4. Establecer:
   - CPU usage > 80%
   - Memory usage > 80%
   - Response time > 5 seconds
   - Error rate > 5%

### Notificaciones Personalizadas:
```bash
# Script para alertas por email
#!/bin/bash
if ! curl -f -s https://diabetes-api-xxxx.onrender.com/health > /dev/null; then
    echo "ALERTA: API no responde" | mail -s "API Down" admin@example.com
fi
```

---

**📅 Última actualización:** Septiembre 2025
**🏥 Versión del Sistema:** 2.0.0