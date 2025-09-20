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

```
diabetes_prediction_system/
├── config.py              # Configuración centralizada
├── data_generator.py      # Generación de datos sintéticos
├── data_preprocessor.py   # Preprocesamiento de datos
├── model_trainer.py       # Entrenamiento de modelos
├── predictor.py           # Sistema de predicción
├── main.py               # Script principal
├── requirements.txt      # Dependencias
├── README.md            # Documentación
├── models/              # Modelos entrenados (generado)
├── outputs/             # Resultados y análisis (generado)
└── data/               # Datos generados (generado)
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

### Ejecución completa del pipeline
```bash
python main.py
```

### Con opciones personalizadas
```bash
# Pipeline con 2000 muestras
python main.py --samples 2000

# Solo análisis de datos
python main.py --analyze

# Solo ejemplo de predicción
python main.py --predict

# No guardar datos generados
python main.py --no-save
```

### Uso programático

```python
from predictor import predict_glucose

# Datos del paciente
patient_data = {
    'edad': 55,
    'sexo': 'M',
    'imc': 28.5,
    'tas': 135,
    'tad': 85,
    'perimetro_abdominal': 95,
    'realiza_ejercicio': 'No',
    'fuma': 'No',
    'historia_familiar_dm': 'Si'
}

# Hacer predicción
result = predict_glucose(patient_data)
print(f"Glucosa estimada: {result['glucose_mg_dl']} mg/dL")
print(f"Categoría: {result['category']}")
print(f"Riesgo: {result['risk_level']}")
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

- **numpy, pandas, scipy**: Computación científica
- **scikit-learn**: Machine learning
- **xgboost, lightgbm**: Modelos de boosting
- **matplotlib, seaborn**: Visualización
- **joblib**: Serialización de modelos

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

## 🔮 Próximas Mejoras

- [ ] Implementación de API REST
- [ ] Interfaz web para predicciones
- [ ] Validación con datos reales
- [ ] Sistema de monitoreo de modelos
- [ ] Optimización automática de hiperparámetros
- [ ] Integración con bases de datos médicas

---

**Desarrollado con ❤️ para la comunidad médica y científica**