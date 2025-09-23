# 📋 Documentación de APIs y Endpoints Médicos

## 🏥 Sistema Predictivo de Diabetes Mellitus Tipo 2

Esta documentación describe todos los endpoints y APIs disponibles en el Sistema Predictivo de Diabetes, incluyendo la API REST principal y la interfaz web.

---

## 🔌 API REST Principal (FastAPI)

### 📍 Información General
- **Base URL:** `http://localhost:8000` (desarrollo) / URL de producción
- **Documentación Swagger:** `/docs`
- **Documentación ReDoc:** `/redoc`
- **Versión:** 2.0.0

### 🏥 Endpoints Disponibles

#### 1. Health Check
**GET** `/health`

Verifica el estado del servicio y carga del modelo.

**Respuesta:**
```json
{
  "status": "healthy",
  "timestamp": "2025-09-23T00:57:26.481Z",
  "version": "2.0.0",
  "model_loaded": true,
  "total_predictions": 150
}
```

**Códigos de estado:**
- `200`: Servicio funcionando correctamente
- `503`: Servicio degradado (modelo no cargado)

---

#### 2. Información del Modelo
**GET** `/model/info`

Obtiene información detallada del modelo de machine learning cargado.

**Respuesta:**
```json
{
  "model_name": "Gradient Boosting",
  "r2_score": 0.85,
  "training_date": "2025-09-22",
  "n_features": 29,
  "feature_columns": [
    "edad", "sexo", "zona_residencia", "estrato", "talla", "peso", "imc",
    "perimetro_abdominal", "tas", "tad", "frecuencia_cardiaca",
    "realiza_ejercicio", "fuma", "medicamentos_hta",
    "historia_familiar_dm", "diabetes_gestacional", "puntaje_findrisc",
    "riesgo_cardiovascular", "presion_arterial_media", "presion_pulso",
    "ratio_cintura_altura", "imc_categoria", "edad_categoria",
    "edad_squared", "score_cv", "indice_salud", "consume_alcohol_Frecuente",
    "consume_alcohol_Nunca", "consume_alcohol_Ocasional"
  ],
  "status": "loaded"
}
```

---

#### 3. Predicción Individual
**POST** `/predict`

Realiza una predicción de diabetes para un paciente individual.

**Body (JSON):**
```json
{
  "edad": 55,
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
}
```

**Respuesta:**
```json
{
  "glucose_mg_dl": 142.5,
  "category": "Prediabetes",
  "risk_level": "Moderado",
  "confidence": "Alto",
  "interpretation": "Los niveles de glucosa indican prediabetes. Se recomienda consultar con un médico y mejorar los hábitos de vida.",
  "timestamp": "2025-09-23T00:57:26.481Z",
  "model_version": "2.0.0",
  "processing_time_ms": 45.2
}
```

**Validaciones:**
- `edad`: 0-120 años
- `sexo`: "M" o "F"
- `imc`: 10-60
- `tas`: 60-250 mmHg
- `tad`: 40-150 mmHg
- `perimetro_abdominal`: 40-200 cm
- Variables categóricas: valores específicos según campo

---

#### 4. Predicción Batch
**POST** `/predict/batch`

Realiza predicciones para múltiples pacientes simultáneamente.

**Body (JSON):**
```json
[
  {
    "edad": 45,
    "sexo": "F",
    "imc": 25.5,
    "tas": 120,
    "tad": 80,
    "perimetro_abdominal": 85,
    "frecuencia_cardiaca": 70,
    "realiza_ejercicio": "Si",
    "consume_alcohol": "Nunca",
    "fuma": "No",
    "medicamentos_hta": "No",
    "historia_familiar_dm": "No",
    "diabetes_gestacional": "No",
    "puntaje_findrisc": 5,
    "riesgo_cardiovascular": 0.2
  },
  {
    "edad": 65,
    "sexo": "M",
    "imc": 30.2,
    "tas": 140,
    "tad": 90,
    "perimetro_abdominal": 105,
    "frecuencia_cardiaca": 80,
    "realiza_ejercicio": "No",
    "consume_alcohol": "Frecuente",
    "fuma": "Si",
    "medicamentos_hta": "Si",
    "historia_familiar_dm": "Si",
    "diabetes_gestacional": "No",
    "puntaje_findrisc": 15,
    "riesgo_cardiovascular": 0.6
  }
]
```

**Respuesta:**
```json
{
  "results": [
    {
      "glucose_mg_dl": 95.2,
      "category": "Normal",
      "risk_level": "Bajo",
      "confidence": "Alto",
      "interpretation": "Los niveles de glucosa están dentro del rango normal..."
    },
    {
      "glucose_mg_dl": 168.7,
      "category": "Diabetes",
      "risk_level": "Alto",
      "confidence": "Alto",
      "interpretation": "Los niveles de glucosa sugieren diabetes..."
    }
  ],
  "total_patients": 2,
  "processing_time_ms": 89.5,
  "timestamp": "2025-09-23T00:57:26.481Z"
}
```

---

#### 5. Predicción con Modelo Específico
**POST** `/models/{model_name}/predict`

Realiza predicción usando un modelo específico.

**Parámetros de URL:**
- `model_name`: "random_forest" o "gradient_boosting"

**Body:** Mismo que `/predict`

**Ejemplo:** `POST /models/gradient_boosting/predict`

**Respuesta:** Similar a `/predict` con `model_version` incluyendo el nombre del modelo.

---

#### 6. Lista de Modelos Disponibles
**GET** `/models`

Obtiene información sobre todos los modelos disponibles.

**Respuesta:**
```json
{
  "models": [
    {
      "name": "random_forest",
      "display_name": "Random Forest",
      "description": "Modelo de ensemble basado en árboles de decisión",
      "run_id": "2b0bc40a5809462582fe4827a85d0567",
      "experiment_id": "108607450594143967"
    },
    {
      "name": "gradient_boosting",
      "display_name": "Gradient Boosting",
      "description": "Modelo de boosting con alto rendimiento predictivo",
      "run_id": "7d8e8b5c65244e488b1a1431d11b4688",
      "experiment_id": "108607450594143967"
    }
  ],
  "total_models": 2,
  "experiment_name": "Diabetes_Prediction_Complete",
  "timestamp": "2025-09-23T00:57:26.481Z"
}
```

---

#### 7. Información de Categorías
**GET** `/categories`

Obtiene información detallada sobre las categorías de predicción.

**Respuesta:**
```json
{
  "categories": {
    "Normal": {
      "range": "< 100 mg/dL",
      "risk_level": "Bajo",
      "description": "Niveles normales de glucosa",
      "recommendation": "Mantener estilo de vida saludable"
    },
    "Prediabetes": {
      "range": "100-126 mg/dL",
      "risk_level": "Moderado",
      "description": "Niveles elevados de glucosa",
      "recommendation": "Consultar médico y mejorar hábitos"
    },
    "Diabetes": {
      "range": "> 126 mg/dL",
      "risk_level": "Alto",
      "description": "Niveles compatibles con diabetes",
      "recommendation": "Consultar inmediatamente con médico"
    }
  },
  "metrics": {
    "target_r2": "> 0.85",
    "target_rmse": "< 10 mg/dL",
    "target_mae": "< 8 mg/dL"
  }
}
```

---

#### 8. Información de Características
**GET** `/features`

Obtiene información sobre las características requeridas por el modelo.

**Respuesta:**
```json
{
  "required_features": [
    "edad", "sexo", "zona_residencia", "estrato", "talla", "peso", "imc",
    "perimetro_abdominal", "tas", "tad", "frecuencia_cardiaca",
    "realiza_ejercicio", "fuma", "medicamentos_hta",
    "historia_familiar_dm", "diabetes_gestacional", "puntaje_findrisc",
    "riesgo_cardiovascular", "presion_arterial_media", "presion_pulso",
    "ratio_cintura_altura", "imc_categoria", "edad_categoria",
    "edad_squared", "score_cv", "indice_salud", "consume_alcohol_Frecuente",
    "consume_alcohol_Nunca", "consume_alcohol_Ocasional"
  ],
  "total_features": 29,
  "feature_types": {
    "numeric": [
      "edad", "imc", "tas", "tad", "perimetro_abdominal",
      "frecuencia_cardiaca", "puntaje_findrisc", "riesgo_cardiovascular"
    ],
    "categorical": [
      "sexo", "realiza_ejercicio", "consume_alcohol", "fuma",
      "medicamentos_hta", "historia_familiar_dm", "diabetes_gestacional"
    ],
    "derived": [
      "presion_arterial_media", "presion_pulso", "ratio_cintura_altura",
      "imc_categoria", "edad_categoria", "edad_squared", "score_cv", "indice_salud"
    ]
  }
}
```

---

## 🌐 Interfaz Web (Streamlit)

### 📍 Información General
- **URL:** `http://localhost:8501` (desarrollo)
- **Framework:** Streamlit
- **Funcionalidades:** Interfaz gráfica completa para predicciones

### 🏥 Funcionalidades Disponibles

#### 1. Predicción Individual
- Formulario completo con todos los campos médicos
- Validación en tiempo real
- Visualización de resultados con gráficos
- Interpretación médica automática

#### 2. Análisis Batch
- Carga de archivos CSV con múltiples pacientes
- Procesamiento masivo de predicciones
- Descarga de resultados
- Visualizaciones estadísticas

#### 3. Visualizaciones
- Gráficos interactivos de datos médicos
- Análisis de correlaciones
- Distribuciones por categorías

#### 4. Información del Sistema
- Detalles de modelos disponibles
- Métricas de rendimiento
- Guías de uso

---

## 🔧 Funciones del Predictor

### 📍 Clase `DiabetesPredictor`

#### Métodos Principales:

1. **`__init__(model_path=None, scaler_path=None, model_name=None)`**
   - Inicializa el predictor
   - Carga modelo desde MLflow o archivos locales

2. **`predict(patient_data: Dict[str, Any]) -> Dict[str, Any]`**
   - Realiza predicción para un paciente
   - Aplica preprocesamiento completo
   - Retorna resultado categorizado

3. **`predict_batch(patients_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]`**
   - Predicciones para múltiples pacientes
   - Optimizado para rendimiento

4. **`get_model_info() -> Dict[str, Any]`**
   - Información del modelo cargado
   - Métricas de rendimiento

#### Funciones de Utilidad:

1. **`predict_glucose(patient_data, model_path=None, model_name=None)`**
   - Función de conveniencia para predicciones
   - Crea predictor automáticamente

---

## 📊 Características del Modelo

### 🏥 Variables de Entrada (29 características)

#### Variables Básicas:
- `edad`: Edad en años
- `sexo`: M (0) o F (1)
- `imc`: Índice de Masa Corporal
- `tas`: Tensión Arterial Sistólica (mmHg)
- `tad`: Tensión Arterial Diastólica (mmHg)
- `perimetro_abdominal`: Circunferencia de cintura (cm)

#### Variables Clínicas:
- `frecuencia_cardiaca`: Pulsaciones por minuto
- `puntaje_findrisc`: Puntuación FINDRISC (0-26)
- `riesgo_cardiovascular`: Riesgo CV (0-1)

#### Variables Categóricas:
- `realiza_ejercicio`: Si/No
- `fuma`: Si/No
- `consume_alcohol`: Nunca/Ocasional/Frecuente
- `medicamentos_hta`: Si/No
- `historia_familiar_dm`: Si/No
- `diabetes_gestacional`: Si/No (solo mujeres)

#### Variables Derivadas:
- `presion_arterial_media`: (TAS + 2*TAD)/3
- `presion_pulso`: TAS - TAD
- `ratio_cintura_altura`: Perímetro abdominal / talla
- `imc_categoria`: Categorización del IMC
- `edad_categoria`: Categorización por edad
- `edad_squared`: Edad al cuadrado
- `score_cv`: Score de riesgo cardiovascular
- `indice_salud`: Índice compuesto de salud

---

## 📈 Categorías de Predicción

### 🟢 Normal (< 100 mg/dL)
- **Riesgo:** Bajo
- **Interpretación:** Niveles normales de glucosa
- **Recomendación:** Mantener estilo de vida saludable

### 🟡 Prediabetes (100-126 mg/dL)
- **Riesgo:** Moderado
- **Interpretación:** Niveles elevados de glucosa
- **Recomendación:** Consultar médico y mejorar hábitos

### 🔴 Diabetes (> 126 mg/dL)
- **Riesgo:** Alto
- **Interpretación:** Niveles compatibles con diabetes
- **Recomendación:** Consultar inmediatamente con médico

---

## 🔄 Manejo de Errores

### Códigos de Estado HTTP:
- `200`: Operación exitosa
- `400`: Datos de entrada inválidos
- `500`: Error interno del servidor
- `503`: Servicio no disponible

### Mensajes de Error Comunes:
- `"Modelo no cargado"`: Error de carga del modelo ML
- `"Error en predicción: [detalle]"`: Error durante el procesamiento
- `"Error interno: [detalle]"`: Error inesperado del sistema

---

## 🚀 Ejemplos de Uso

### Python con requests:
```python
import requests

# Predicción individual
url = "http://localhost:8000/predict"
data = {
    "edad": 55,
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
}

response = requests.post(url, json=data)
result = response.json()
print(f"Glucosa: {result['glucose_mg_dl']} mg/dL")
print(f"Categoría: {result['category']}")
```

### cURL:
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "edad": 55,
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
```

---

## 📋 Requisitos del Sistema

### Variables de Entorno:
```bash
MLFLOW_TRACKING_URI=./mlruns
MODELS_DIR=./models
OUTPUTS_DIR=./outputs
METADATA_FILENAME=metadata.json
```

### Dependencias Principales:
- **FastAPI:** Framework web
- **Streamlit:** Interfaz web
- **scikit-learn:** Machine learning
- **MLflow:** Gestión de modelos
- **pandas:** Procesamiento de datos
- **numpy:** Cálculos numéricos
- **plotly:** Visualizaciones

---

## 🔒 Consideraciones de Seguridad

### Producción:
- Configurar CORS para dominios específicos
- Implementar autenticación (OAuth2, JWT)
- Usar HTTPS en producción
- Validar y sanitizar todas las entradas
- Monitoreo y logging de seguridad

### Privacidad:
- No almacenar datos sensibles de pacientes
- Logs anónimos sin información identificable
- Cumplimiento con regulaciones médicas (HIPAA, GDPR)

---

## 📞 Soporte y Contacto

Para soporte técnico o preguntas sobre la API:
- 📧 Email: soporte@sistemadiabetes.com
- 📚 Documentación: `/docs` (Swagger UI)
- 🔄 Estado del servicio: `/health`

---

**⚠️ Descargo de Responsabilidad:** Este sistema es una herramienta de apoyo para profesionales de la salud. No sustituye el juicio médico profesional ni los análisis de laboratorio. Siempre consultar con un médico para diagnósticos y tratamientos.