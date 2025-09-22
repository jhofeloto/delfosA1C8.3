# 🏥 Sistema Predictivo de Diabetes Mellitus Tipo 2

Un sistema completo de machine learning para predicción de niveles de glucosa en sangre y clasificación de riesgo de diabetes, desarrollado con Python y scikit-learn.

## 📋 Descripción

Este proyecto implementa un pipeline completo de machine learning para la predicción de diabetes, incluyendo:

- **Generación de datos sintéticos** realistas para entrenamiento
- **Preprocesamiento avanzado** de características médicas
- **Entrenamiento y comparación** de múltiples modelos de ML
- **Sistema de predicción** listo para producción
- **Evaluación y visualización** de resultados

## 🚀 Características

- ✅ **13 modelos de ML** diferentes (lineales, ensemble, boosting, redes neuronales)
- ✅ **Pipeline completo** desde datos crudos hasta predicciones
- ✅ **Sistema modular** y reutilizable
- ✅ **Compatible con entornos locales** (no requiere Google Colab)
- ✅ **Exportación de modelos** en múltiples formatos
- ✅ **API de predicción** fácil de usar

## 📁 Estructura del Proyecto

### Archivos Principales
```
diabetes_prediction_system/
├── 📄 config.py                    # Configuración centralizada
├── 📄 data_generator.py            # Generación de datos sintéticos
├── 📄 data_preprocessor.py         # Preprocesamiento de datos
├── 📄 model_trainer.py             # Entrenamiento de modelos
├── 📄 predictor.py                 # Sistema de predicción
├── 📄 main.py                     # Script principal ML
├── 📄 api.py                      # API REST (FastAPI)
├── 📄 web_app.py                  # Interfaz web (Streamlit)
├── 📄 hyperparameter_optimizer.py  # Optimización (Optuna)
├── 📄 model_monitoring.py          # Monitoreo (MLflow)
├── 📄 database_manager.py          # Base de datos (SQLAlchemy)
├── 📄 test_system.py              # Pruebas del sistema
├── 📄 requirements.txt            # Dependencias
├── 📄 README.md                   # Documentación
└── 📄 .gitignore                  # Git ignore
```

### Directorios Generados
```
diabetes_prediction_system/
├── 📁 models/                     # Modelos entrenados
│   ├── best_model.joblib         # Mejor modelo
│   ├── scaler.joblib             # Scaler para preprocesamiento
│   └── model_metadata.json       # Metadatos del modelo
├── 📁 outputs/                    # Resultados y análisis
│   ├── mlruns/                   # MLflow tracking
│   ├── model_comparison.csv      # Comparación de modelos
│   ├── optimization_results.json # Resultados de optimización
│   └── api_predictions.log       # Log de predicciones API
├── 📁 data/                       # Datos generados
│   ├── diabetes_dataset_*.csv    # Datasets sintéticos
│   └── diabetes_medical.db       # Base de datos SQLite
└── 📁 temp_artifacts/             # Artefactos temporales
```

## 🛠️ Instalación

### 1. Clonar el repositorio
```bash
git clone <url-del-repositorio>
cd diabetes_prediction_system
```

### 2. Crear entorno virtual (recomendado)
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

## 🎯 Uso

### 1. Pipeline Original (Machine Learning)
```bash
# Ejecución completa del pipeline
python main.py

# Con opciones personalizadas
python main.py --samples 2000     # 2000 muestras
python main.py --analyze          # Solo análisis
python main.py --predict          # Solo predicción
python main.py --no-save          # No guardar datos
```

### 2. API REST (FastAPI)
```bash
# Iniciar servidor API
python api.py --host 0.0.0.0 --port 8000

# Documentación disponible en:
# http://localhost:8000/docs
# http://localhost:8000/redoc
```

### 3. Interfaz Web (Streamlit)
```bash
# Iniciar interfaz web
python web_app.py

# O con configuración personalizada
streamlit run web_app.py --server.port 8501
```

### 4. Optimización de Hiperparámetros
```bash
# Optimizar modelos específicos
python -c "
from hyperparameter_optimizer import optimize_diabetes_models
from data_generator import create_sample_dataset
from data_preprocessor import preprocess_diabetes_data
from sklearn.model_selection import train_test_split

# Preparar datos
df = create_sample_dataset(500)
df_processed, preprocessor = preprocess_diabetes_data(df)
X = df_processed.drop('Resultado', axis=1)
y = df_processed['Resultado']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Escalar
X_train_scaled, X_test_scaled = preprocessor.scale_features(X_train, X_test)

# Optimizar
results = optimize_diabetes_models(
    X_train_scaled, y_train, X_test_scaled, y_test,
    models_to_optimize=['Random Forest', 'XGBoost'],
    n_trials=30
)
print(f'Mejor modelo: {results[\"optimization_results\"][\"best_model\"]}')
"
```

### 5. Base de Datos Médica
```bash
# Usar gestor de base de datos
python -c "
from database_manager import create_database_manager

# Crear gestor
db_manager = create_database_manager()

# Guardar paciente
patient_data = {
    'edad': 45, 'sexo': 'M', 'imc': 25.5,
    'tas': 120, 'tad': 80, 'perimetro_abdominal': 90,
    'realiza_ejercicio': 'Si', 'fuma': 'No'
}
patient_id = db_manager.save_patient(patient_data)

# Guardar predicción
prediction_data = {
    'glucose_mg_dl': 95.5,
    'category': 'Normal',
    'risk_level': 'Bajo'
}
db_manager.save_prediction(patient_id, prediction_data, patient_data)

# Obtener estadísticas
stats = db_manager.get_database_stats()
print(f'Total pacientes: {stats[\"total_patients\"]}')
"
```

### 6. Monitoreo con MLflow
```bash
# Ver interfaz web de MLflow
mlflow ui --backend-store-uri outputs/mlruns

# En otra terminal, ejecutar experimentos
python -c "
from model_monitoring import log_training_session
from model_trainer import train_diabetes_models

# Entrenar y monitorear
trainer = train_diabetes_models(df_processed, preprocessor)
monitor = log_training_session(X_train_scaled, y_train, X_test_scaled, y_test, trainer.results)
"
```

### 7. Uso Programático

#### Predicción básica
```python
from predictor import predict_glucose

patient_data = {
    'edad': 55, 'sexo': 'M', 'imc': 28.5,
    'tas': 135, 'tad': 85, 'perimetro_abdominal': 95,
    'realiza_ejercicio': 'No', 'fuma': 'No',
    'historia_familiar_dm': 'Si'
}

result = predict_glucose(patient_data)
print(f"Glucosa: {result['glucose_mg_dl']} mg/dL")
print(f"Categoría: {result['category']}")
print(f"Riesgo: {result['risk_level']}")
```

#### Sistema completo
```python
from data_generator import create_sample_dataset
from data_preprocessor import preprocess_diabetes_data
from model_trainer import train_diabetes_models
from predictor import predict_glucose
from database_manager import create_database_manager

# 1. Generar datos
df = create_sample_dataset(1000)

# 2. Preprocesar
df_processed, preprocessor = preprocess_diabetes_data(df)

# 3. Entrenar modelos
trainer = train_diabetes_models(df_processed, preprocessor)

# 4. Hacer predicción
patient_data = df.iloc[0].drop('Resultado').to_dict()
result = predict_glucose(patient_data)

# 5. Guardar en BD
db_manager = create_database_manager()
patient_id = db_manager.save_patient(patient_data)
db_manager.save_prediction(patient_id, result, patient_data)
```

## 📊 Modelos Implementados

| Modelo | Tipo | Descripción |
|--------|------|-------------|
| **Linear Regression** | Lineal | Modelo base de regresión lineal |
| **Ridge Regression** | Regularizado | Regresión con regularización L2 |
| **Lasso Regression** | Regularizado | Regresión con regularización L1 |
| **Elastic Net** | Regularizado | Combinación de L1 y L2 |
| **Random Forest** | Ensemble | Bosques aleatorios optimizados |
| **Extra Trees** | Ensemble | Árboles extremadamente aleatorios |
| **Gradient Boosting** | Boosting | Gradient Boosting optimizado |
| **XGBoost** | Boosting | Extreme Gradient Boosting |
| **LightGBM** | Boosting | Light Gradient Boosting Machine |
| **AdaBoost** | Boosting | Adaptive Boosting |
| **SVM** | Kernel | Support Vector Machine con RBF |
| **KNN** | Instancia | K-Nearest Neighbors con pesos |
| **Neural Network** | Red Neuronal | Multi-layer Perceptron |

## 🔧 Configuración

### Variables de entorno
```python
# En config.py se pueden modificar:
RANDOM_SEED = 42          # Semilla para reproducibilidad
TEST_SIZE = 0.2          # Proporción de datos de prueba
CROSS_VAL_FOLDS = 5      # Número de folds para validación cruzada
DEFAULT_N_SAMPLES = 1000 # Número de muestras por defecto
```

### Rutas de archivos
- `models/` : Modelos entrenados (.joblib, .pkl)
- `outputs/` : Resultados y análisis (.csv, .json)
- `data/` : Datos generados (.csv)

## 📈 Resultados Esperados

### Métricas de rendimiento
- **R² Score**: > 0.85 (coeficiente de determinación)
- **RMSE**: < 10 mg/dL (error cuadrático medio)
- **MAE**: < 8 mg/dL (error absoluto medio)

### Categorías de predicción
- **Normal**: < 100 mg/dL
- **Prediabetes**: 100-126 mg/dL
- **Diabetes**: > 126 mg/dL

## 🔍 Análisis Exploratorio

El sistema incluye análisis exploratorio automático:
- Distribución de glucosa por categorías
- Correlaciones entre variables
- Análisis de características importantes
- Visualizaciones de rendimiento de modelos

## 💾 Archivos Generados

### Modelos
- `models/best_model.joblib` : Mejor modelo entrenado
- `models/scaler.joblib` : Scaler para preprocesamiento
- `models/model_metadata.json` : Metadatos del entrenamiento

### Resultados
- `outputs/model_comparison_results.csv` : Comparación de modelos
- `outputs/data_analysis.csv` : Análisis exploratorio
- `data/diabetes_dataset_*.csv` : Datos sintéticos generados

## 🧪 Pruebas

### Ejecutar pruebas básicas
```bash
python -c "
from data_generator import create_sample_dataset
from predictor import predict_glucose

# Generar datos de prueba
df = create_sample_dataset(100)
print(f'Datos generados: {df.shape}')

# Probar predicción
patient = {'edad': 45, 'imc': 25, 'tas': 120, 'tad': 80}
result = predict_glucose(patient)
print(f'Predicción: {result}')
"
```

## 🚨 Requisitos del Sistema

- **Python**: 3.8 o superior
- **RAM**: 4GB mínimo (8GB recomendado)
- **Espacio**: 500MB libre para modelos y datos

## 📚 Dependencias Principales

### Core (Originales)
- **numpy, pandas, scipy**: Computación científica
- **scikit-learn**: Machine learning
- **xgboost, lightgbm**: Modelos de boosting
- **matplotlib, seaborn**: Visualización
- **joblib**: Serialización de modelos

### Nuevas (Mejoras Implementadas)
- **fastapi, uvicorn**: API REST
- **streamlit**: Interfaz web
- **optuna**: Optimización de hiperparámetros
- **mlflow**: Monitoreo de modelos
- **sqlalchemy**: Base de datos
- **pydantic**: Validación de datos
- **pytest**: Testing
- **structlog**: Logging avanzado

**Instalación:**
```bash
pip install -r requirements.txt
```

## 🤝 Contribución

1. Fork el proyecto
2. Crear rama para nueva funcionalidad
3. Commit cambios
4. Push a la rama
5. Crear Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 🆘 Soporte

Para soporte técnico o preguntas:
- Crear un issue en GitHub
- Revisar la documentación
- Verificar los ejemplos de uso

## 🔧 Solución de Problemas

### ✅ Problema: "Modelo no cargado" en interfaz web
**Solución implementada:** Se corrigió el sistema de carga de modelos en `predictor.py`

**Problema identificado:**
- El método `_load_model_from_mlflow()` intentaba cargar modelos desde MLflow primero
- Al fallar, el fallback a archivos locales usaba nombres incorrectos
- `model_name.replace('_', ' ')` convertía "random_forest" a "random forest.joblib"
- Los archivos reales son "random_forest.joblib" y "gradient_boosting.joblib"

**Solución aplicada:**
```python
# ❌ Antes (incorrecto)
model_filename = f"{self.model_name.replace('_', ' ')}.joblib"

# ✅ Después (corregido)
model_filename = f"{self.model_name}.joblib"
```

**Sistema de fallback mejorado:**
1. **Primero:** Intenta cargar desde MLflow
2. **Fallback:** Si falla, carga desde archivos locales
3. **Logging:** Registra el proceso completo para debugging
4. **Error handling:** Manejo robusto de excepciones

**Verificación:**
- ✅ Ambos modelos (Random Forest y Gradient Boosting) cargan correctamente
- ✅ Predicciones funcionan en API y interfaz web
- ✅ Sistema de fallback opera sin problemas

**Para verificar la solución:**
```bash
python -c "
from predictor import DiabetesPredictor
predictor = DiabetesPredictor('random_forest')
print('Modelo cargado:', predictor.model is not None)
result = predictor.predict({'edad': 45, 'sexo': 'M', 'imc': 25.5})
print('Predicción:', result)
"
```

## 🚀 Mejoras Implementadas

### ✅ API REST (FastAPI)
- **Endpoint:** `http://localhost:8000`
- **Documentación:** `http://localhost:8000/docs`
- **Funcionalidades:**
  - Predicción individual: `POST /predict`
  - Predicción batch: `POST /predict/batch`
  - Información del modelo: `GET /model/info`
  - Health check: `GET /health`
  - Categorías: `GET /categories`
  - Características: `GET /features`

**Ejemplo de uso:**
```bash
# Iniciar API
python api.py --host 0.0.0.0 --port 8000

# Hacer predicción
curl -X POST "http://localhost:8000/predict" \
     -H "Content-Type: application/json" \
     -d '{
       "edad": 45,
       "sexo": "M",
       "imc": 25.5,
       "tas": 120,
       "tad": 80,
       "perimetro_abdominal": 90,
       "realiza_ejercicio": "Si",
       "fuma": "No",
       "consume_alcohol": "Nunca",
       "medicamentos_hta": "No",
       "historia_familiar_dm": "Si",
       "diabetes_gestacional": "No",
       "puntaje_findrisc": 8,
       "riesgo_cardiovascular": 0.3
     }'
```

### ✅ Interfaz Web (Streamlit)
- **Aplicación:** `http://localhost:8501`
- **Funcionalidades:**
  - Predicción individual interactiva
  - Análisis batch con upload de CSV
  - Visualizaciones avanzadas
  - Información del sistema

**Ejemplo de uso:**
```bash
# Iniciar interfaz web
python web_app.py

# O con configuración personalizada
streamlit run web_app.py --server.port 8501 --server.address 0.0.0.0
```

### ✅ Optimización Automática de Hiperparámetros (Optuna)
- **Modelos optimizados:** Random Forest, XGBoost, LightGBM, Gradient Boosting, Ridge, Lasso, SVR, Neural Network
- **Métricas:** R², RMSE, MAE
- **Validación cruzada:** 5-fold
- **Funcionalidades:**
  - Optimización bayesiana
  - Logging de experimentos
  - Guardado de resultados

**Ejemplo de uso:**
```python
from hyperparameter_optimizer import optimize_diabetes_models

# Optimizar modelos
results = optimize_diabetes_models(
    X_train_scaled, y_train, X_test_scaled, y_test,
    models_to_optimize=["Random Forest", "XGBoost"],
    n_trials=50
)
```

### ✅ Sistema de Monitoreo (MLflow)
- **Tracking:** Métricas, parámetros, artefactos
- **Modelos:** Registro automático de modelos
- **Visualizaciones:** Gráficos de rendimiento
- **Comparación:** Múltiples experimentos

**Ejemplo de uso:**
```python
from model_monitoring import log_training_session

# Registrar sesión de entrenamiento
monitor = log_training_session(X_train, y_train, X_test, y_test, model_results)

# Ver historial
history = monitor.get_experiment_history()
```

### ✅ Base de Datos Médica (SQLAlchemy)
- **Tablas:** Patients, MedicalData, Predictions, ModelPerformance
- **Funcionalidades:**
  - Guardado de pacientes y datos médicos
  - Registro de predicciones
  - Historial médico completo
  - Estadísticas y reportes
  - Exportación a CSV

**Ejemplo de uso:**
```python
from database_manager import create_database_manager

# Crear gestor de BD
db_manager = create_database_manager()

# Guardar paciente
patient_id = db_manager.save_patient(patient_data)

# Guardar predicción
prediction_id = db_manager.save_prediction(patient_id, prediction_data, input_data)

# Obtener estadísticas
stats = db_manager.get_database_stats()
```

## 🔮 Próximas Mejoras

- [ ] Validación con datos reales de pacientes
- [ ] Sistema de alertas médicas
- [ ] Integración con sistemas hospitalarios (HL7, FHIR)
- [ ] Modelos de deep learning
- [ ] Análisis de tendencias temporales
- [ ] Sistema de recomendaciones médicas

---

**Desarrollado con ❤️ para la comunidad médica y científica**