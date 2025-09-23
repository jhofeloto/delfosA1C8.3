# 🧪 Pruebas de Integración End-to-End

## 🏥 Sistema Predictivo de Diabetes Mellitus Tipo 2

Este documento describe las pruebas completas de integración end-to-end para validar el funcionamiento completo del sistema, desde la entrada de datos hasta la generación de resultados y reportes.

---

## 📋 Objetivos de las Pruebas

### 🎯 Validar Funcionalidad Completa:
- ✅ Flujo completo de predicción de diabetes
- ✅ Integración entre todos los componentes
- ✅ Interfaces de usuario funcionales
- ✅ APIs respondiendo correctamente
- ✅ Base de datos operando correctamente

### 🔍 Validar Casos de Uso:
- ✅ Predicción individual de pacientes
- ✅ Análisis batch de múltiples pacientes
- ✅ Visualización de resultados médicos
- ✅ Generación de reportes clínicos
- ✅ Monitoreo y alertas del sistema

### 📊 Validar Métricas de Rendimiento:
- ✅ Tiempos de respuesta aceptables
- ✅ Uso de recursos optimizado
- ✅ Escalabilidad del sistema
- ✅ Fiabilidad de predicciones

---

## 🏗️ Arquitectura de Pruebas

### Componentes a Probar:
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Streamlit     │    │   FastAPI       │    │   PostgreSQL    │
│   Dashboard     │◄──►│   REST API      │◄──►│   Database      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   ML Models     │    │   MLflow UI     │    │   File System   │
│   (sklearn)     │    │   (Tracking)    │    │   (models/)     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Flujos de Datos:
1. **Usuario → Streamlit → API → Modelo → Resultado**
2. **Usuario → Streamlit → Batch Processing → API → Resultados**
3. **API → Health Check → Model Loading → Response**
4. **Sistema → Logs → MLflow → Monitoring**

---

## 🧪 Escenarios de Prueba

### Escenario 1: Predicción Individual Básica

**Objetivo:** Validar el flujo completo de predicción para un paciente individual.

**Pasos:**
1. **Preparación:**
   ```bash
   # Verificar que todos los servicios estén funcionando
   curl -f https://diabetes-api-xxxx.onrender.com/health
   curl -f -I https://diabetes-streamlit-xxxx.onrender.com/
   ```

2. **Ejecutar Prueba:**
   ```bash
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

   # Ejecutar predicción
   curl -X POST https://diabetes-api-xxxx.onrender.com/predict \
     -H "Content-Type: application/json" \
     -d "$TEST_DATA"
   ```

3. **Validaciones:**
   - ✅ Respuesta HTTP 200
   - ✅ JSON válido con todos los campos
   - ✅ `glucose_mg_dl` entre 50-400
   - ✅ `category` es "Normal", "Prediabetes", o "Diabetes"
   - ✅ `risk_level` es "Bajo", "Moderado", o "Alto"
   - ✅ `confidence` es "Alto", "Moderado", o "Bajo"
   - ✅ `processing_time_ms` < 5000ms

**Resultado Esperado:**
```json
{
  "glucose_mg_dl": 142.5,
  "category": "Prediabetes",
  "risk_level": "Moderado",
  "confidence": "Alto",
  "interpretation": "Los niveles de glucosa indican prediabetes...",
  "timestamp": "2025-09-23T00:57:26.481Z",
  "model_version": "2.0.0",
  "processing_time_ms": 45.2
}
```

---

### Escenario 2: Análisis Batch de Pacientes

**Objetivo:** Validar el procesamiento de múltiples pacientes simultáneamente.

**Pasos:**
1. **Preparar Datos de Prueba:**
   ```bash
   # Crear archivo CSV con datos de prueba
   cat > test_batch.csv << EOF
   edad,sexo,imc,tas,tad,perimetro_abdominal,frecuencia_cardiaca,realiza_ejercicio,consume_alcohol,fuma,medicamentos_hta,historia_familiar_dm,diabetes_gestacional,puntaje_findrisc,riesgo_cardiovascular
   45,M,28.5,135,85,95,75,Si,Ocasional,No,Si,Si,No,12,0.4
   35,F,22.1,110,70,75,65,Si,Nunca,No,No,No,No,3,0.1
   65,M,32.8,150,95,110,85,No,Frecuente,Si,Si,Si,No,18,0.7
   55,F,26.4,125,80,88,72,Si,Ocasional,No,No,Si,No,8,0.3
   40,M,24.2,118,75,82,68,Si,Nunca,No,No,No,No,4,0.15
   EOF
   ```

2. **Ejecutar Prueba:**
   ```bash
   # Usar la interfaz web o API para procesar batch
   curl -X POST https://diabetes-api-xxxx.onrender.com/predict/batch \
     -H "Content-Type: application/json" \
     -d '[
       {"edad": 45, "sexo": "M", "imc": 28.5, "tas": 135, "tad": 85, "perimetro_abdominal": 95, "frecuencia_cardiaca": 75, "realiza_ejercicio": "Si", "consume_alcohol": "Ocasional", "fuma": "No", "medicamentos_hta": "Si", "historia_familiar_dm": "Si", "diabetes_gestacional": "No", "puntaje_findrisc": 12, "riesgo_cardiovascular": 0.4},
       {"edad": 35, "sexo": "F", "imc": 22.1, "tas": 110, "tad": 70, "perimetro_abdominal": 75, "frecuencia_cardiaca": 65, "realiza_ejercicio": "Si", "consume_alcohol": "Nunca", "fuma": "No", "medicamentos_hta": "No", "historia_familiar_dm": "No", "diabetes_gestacional": "No", "puntaje_findrisc": 3, "riesgo_cardiovascular": 0.1}
     ]'
   ```

3. **Validaciones:**
   - ✅ Respuesta HTTP 200
   - ✅ `total_patients` = 5
   - ✅ `results` array con 5 elementos
   - ✅ Cada resultado tiene estructura completa
   - ✅ `processing_time_ms` < 10000ms
   - ✅ Distribución de categorías realista

**Resultado Esperado:**
```json
{
  "results": [
    {
      "glucose_mg_dl": 142.5,
      "category": "Prediabetes",
      "risk_level": "Moderado",
      "confidence": "Alto",
      "interpretation": "..."
    },
    {
      "glucose_mg_dl": 85.2,
      "category": "Normal",
      "risk_level": "Bajo",
      "confidence": "Alto",
      "interpretation": "..."
    }
  ],
  "total_patients": 5,
  "processing_time_ms": 234.5,
  "timestamp": "2025-09-23T00:57:26.481Z"
}
```

---

### Escenario 3: Interfaz Web Completa

**Objetivo:** Validar la funcionalidad completa de la interfaz Streamlit.

**Pasos:**
1. **Acceso a la Interfaz:**
   ```bash
   # Verificar que Streamlit esté accesible
   curl -f -I https://diabetes-streamlit-xxxx.onrender.com/
   ```

2. **Navegación por Tabs:**
   - ✅ Tab "Predicción Individual" carga correctamente
   - ✅ Tab "Análisis Batch" carga correctamente
   - ✅ Tab "Visualizaciones" carga correctamente
   - ✅ Tab "Información" carga correctamente

3. **Funcionalidad de Predicción:**
   - ✅ Formulario acepta datos válidos
   - ✅ Validación de entrada funciona
   - ✅ Predicción se ejecuta correctamente
   - ✅ Resultados se muestran apropiadamente
   - ✅ Gráficos se generan correctamente

4. **Funcionalidad Batch:**
   - ✅ Upload de CSV funciona
   - ✅ Procesamiento batch se ejecuta
   - ✅ Resultados se muestran en tabla
   - ✅ Descarga de CSV funciona
   - ✅ Visualizaciones se generan

**Validaciones:**
- ✅ Interfaz carga en < 10 segundos
- ✅ Todos los elementos interactivos funcionan
- ✅ Predicciones son consistentes con API
- ✅ Manejo de errores apropiado
- ✅ Diseño responsive funciona

---

### Escenario 4: Monitoreo y Health Checks

**Objetivo:** Validar los sistemas de monitoreo y health checks.

**Pasos:**
1. **Health Checks Básicos:**
   ```bash
   # API Health Check
   curl -s https://diabetes-api-xxxx.onrender.com/health | jq '.'

   # Model Info
   curl -s https://diabetes-api-xxxx.onrender.com/model/info | jq '.'

   # Available Models
   curl -s https://diabetes-api-xxxx.onrender.com/models | jq '.'
   ```

2. **Métricas del Sistema:**
   ```bash
   # Categories Info
   curl -s https://diabetes-api-xxxx.onrender.com/categories | jq '.'

   # Features Info
   curl -s https://diabetes-api-xxxx.onrender.com/features | jq '.'
   ```

3. **Logs y Monitoreo:**
   - ✅ Logs accesibles en Render Dashboard
   - ✅ Métricas de CPU/Memoria visibles
   - ✅ Alertas configuradas correctamente

**Validaciones:**
- ✅ `/health` responde en < 2 segundos
- ✅ `model_loaded` = true
- ✅ `status` = "healthy"
- ✅ Información de modelo completa
- ✅ Logs sin errores críticos

---

### Escenario 5: Diferentes Modelos de ML

**Objetivo:** Validar el funcionamiento con diferentes modelos.

**Pasos:**
1. **Probar Random Forest:**
   ```bash
   curl -X POST https://diabetes-api-xxxx.onrender.com/models/random_forest/predict \
     -H "Content-Type: application/json" \
     -d '{"edad": 45, "sexo": "M", "imc": 28.5, "tas": 135, "tad": 85, "perimetro_abdominal": 95, "frecuencia_cardiaca": 75, "realiza_ejercicio": "Si", "consume_alcohol": "Ocasional", "fuma": "No", "medicamentos_hta": "Si", "historia_familiar_dm": "Si", "diabetes_gestacional": "No", "puntaje_findrisc": 12, "riesgo_cardiovascular": 0.4}'
   ```

2. **Probar Gradient Boosting:**
   ```bash
   curl -X POST https://diabetes-api-xxxx.onrender.com/models/gradient_boosting/predict \
     -H "Content-Type: application/json" \
     -d '{"edad": 45, "sexo": "M", "imc": 28.5, "tas": 135, "tad": 85, "perimetro_abdominal": 95, "frecuencia_cardiaca": 75, "realiza_ejercicio": "Si", "consume_alcohol": "Ocasional", "fuma": "No", "medicamentos_hta": "Si", "historia_familiar_dm": "Si", "diabetes_gestacional": "No", "puntaje_findrisc": 12, "riesgo_cardiovascular": 0.4}'
   ```

3. **Comparar Resultados:**
   - ✅ Ambos modelos responden correctamente
   - ✅ Predicciones son consistentes (±10% variación)
   - ✅ Categorías son las mismas o similares
   - ✅ Tiempos de respuesta similares

---

### Escenario 6: Casos Edge y Manejo de Errores

**Objetivo:** Validar el comportamiento con datos problemáticos.

**Pasos:**
1. **Datos Inválidos:**
   ```bash
   # Edad fuera de rango
   curl -X POST https://diabetes-api-xxxx.onrender.com/predict \
     -H "Content-Type: application/json" \
     -d '{"edad": 150, "sexo": "M", "imc": 28.5, "tas": 135, "tad": 85, "perimetro_abdominal": 95, "frecuencia_cardiaca": 75, "realiza_ejercicio": "Si", "consume_alcohol": "Ocasional", "fuma": "No", "medicamentos_hta": "Si", "historia_familiar_dm": "Si", "diabetes_gestacional": "No", "puntaje_findrisc": 12, "riesgo_cardiovascular": 0.4}'

   # Sexo inválido
   curl -X POST https://diabetes-api-xxxx.onrender.com/predict \
     -H "Content-Type: application/json" \
     -d '{"edad": 45, "sexo": "X", "imc": 28.5, "tas": 135, "tad": 85, "perimetro_abdominal": 95, "frecuencia_cardiaca": 75, "realiza_ejercicio": "Si", "consume_alcohol": "Ocasional", "fuma": "No", "medicamentos_hta": "Si", "historia_familiar_dm": "Si", "diabetes_gestacional": "No", "puntaje_findrisc": 12, "riesgo_cardiovascular": 0.4}'
   ```

2. **Datos Faltantes:**
   ```bash
   # Sin algunos campos
   curl -X POST https://diabetes-api-xxxx.onrender.com/predict \
     -H "Content-Type: application/json" \
     -d '{"edad": 45, "sexo": "M", "imc": 28.5}'
   ```

3. **Validaciones:**
   - ✅ Respuestas de error HTTP apropiadas (400, 422)
   - ✅ Mensajes de error descriptivos
   - ✅ Sistema no se cae con datos inválidos
   - ✅ Logs de errores generados correctamente

---

### Escenario 7: Pruebas de Rendimiento

**Objetivo:** Validar el rendimiento bajo carga.

**Pasos:**
1. **Carga Moderada:**
   ```bash
   # 10 predicciones simultáneas
   for i in {1..10}; do
     curl -X POST https://diabetes-api-xxxx.onrender.com/predict \
       -H "Content-Type: application/json" \
       -d '{"edad": 45, "sexo": "M", "imc": 28.5, "tas": 135, "tad": 85, "perimetro_abdominal": 95, "frecuencia_cardiaca": 75, "realiza_ejercicio": "Si", "consume_alcohol": "Ocasional", "fuma": "No", "medicamentos_hta": "Si", "historia_familiar_dm": "Si", "diabetes_gestacional": "No", "puntaje_findrisc": 12, "riesgo_cardiovascular": 0.4}' &
   done
   wait
   ```

2. **Métricas de Rendimiento:**
   - ✅ Tiempo promedio de respuesta < 5 segundos
   - ✅ Todas las respuestas exitosas
   - ✅ CPU < 80%
   - ✅ Memoria < 80%

---

### Escenario 8: Integración con Base de Datos

**Objetivo:** Validar la integración con PostgreSQL.

**Pasos:**
1. **Configuración de Base de Datos:**
   ```bash
   # Verificar conexión a base de datos
   # (Configurar variables de entorno si es necesario)
   export DATABASE_URL="postgresql://..."
   ```

2. **Pruebas de Persistencia:**
   - ✅ Configuración de conexión funciona
   - ✅ Consultas básicas responden
   - ✅ Esquemas médicos están disponibles

---

## 📊 Métricas de Éxito

### Criterios de Aprobación:

#### Funcionalidad (80% mínimo):
- ✅ Todas las predicciones funcionan correctamente
- ✅ Interfaz web completamente operativa
- ✅ APIs responden apropiadamente
- ✅ Manejo de errores robusto

#### Rendimiento (90% mínimo):
- ✅ Tiempo de respuesta promedio < 5 segundos
- ✅ Throughput > 10 predicciones/segundo
- ✅ Disponibilidad > 99%

#### Fiabilidad (95% mínimo):
- ✅ Sin errores 5xx en pruebas
- ✅ Health checks consistentes
- ✅ Modelos cargados correctamente

---

## 🛠️ Herramientas de Prueba

### Scripts Automatizados:
```bash
# Ejecutar todas las pruebas
./run_all_tests.sh

# Pruebas específicas
./test_api_endpoints.sh
./test_streamlit_ui.sh
./test_performance.sh
./test_error_handling.sh
```

### Monitoreo en Tiempo Real:
```bash
# Monitoreo continuo
watch -n 5 'curl -s https://diabetes-api-xxxx.onrender.com/health | jq "."'

# Logs en tiempo real (Render Dashboard)
# Métricas de sistema (Render Dashboard)
```

---

## 📋 Checklist de Pruebas E2E

### Pre-Pruebas:
- [ ] ✅ Todos los servicios desplegados
- [ ] ✅ URLs de servicios identificadas
- [ ] ✅ Herramientas de prueba preparadas
- [ ] ✅ Datos de prueba listos

### Pruebas Funcionales:
- [ ] ✅ Predicción individual funciona
- [ ] ✅ Análisis batch funciona
- [ ] ✅ Interfaz web operativa
- [ ] ✅ Health checks responden
- [ ] ✅ Manejo de errores correcto

### Pruebas de Rendimiento:
- [ ] ✅ Tiempos de respuesta aceptables
- [ ] ✅ Carga moderada manejada
- [ ] ✅ Recursos del sistema estables

### Pruebas de Integración:
- [ ] ✅ Servicios se comunican correctamente
- [ ] ✅ Base de datos integrada
- [ ] ✅ Logs y monitoreo funcionando

---

## 🚨 Reporte de Incidentes

### Si alguna prueba falla:

1. **Documentar el fallo:**
   - Captura de pantalla/error
   - Datos de entrada utilizados
   - Respuesta del sistema
   - Timestamp del incidente

2. **Investigar causa raíz:**
   - Revisar logs en Render
   - Verificar estado de servicios
   - Probar componentes individuales

3. **Implementar solución:**
   - Corregir código si es necesario
   - Ajustar configuración
   - Reiniciar servicios si es requerido

4. **Reprobar:**
   - Ejecutar pruebas nuevamente
   - Verificar que el problema esté resuelto

---

## 📞 Soporte y Contacto

### Durante las Pruebas:
- 📧 Email: testing@sistemadiabetes.com
- 📚 Documentación: `/docs` en API
- 🔄 Estado: `/health` endpoint

### Reporte de Problemas:
- 🐛 GitHub Issues: Crear issue detallado
- 📋 Logs: Render Dashboard logs
- 📊 Métricas: Render monitoring

---

**📅 Última actualización:** Septiembre 2025
**🏥 Versión del Sistema:** 2.0.0
**✅ Estado de Pruebas:** En Progreso