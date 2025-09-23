# 🏗️ Arquitectura del Sistema Predictivo de Diabetes

## 📋 Visión General

**Sistema integral para predicción de diabetes tipo 2** con enfoque especial en poblaciones femeninas, implementado como una arquitectura de microservicios en la nube.

### **Componentes Principales:**

```
┌─────────────────────────────────────────────────────────────┐
│                    USUARIOS                                  │
├─────────────────────────────────────────────────────────────┤
│  • Profesionales de la Salud                               │
│  • Pacientes                                                │
│  • Investigadores                                           │
│  • Administradores                                          │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                 INTERFACES DE USUARIO                       │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐    ┌──────────────────┐                 │
│  │   Dashboard     │    │   API REST       │                 │
│  │   Streamlit     │    │   FastAPI        │                 │
│  │                 │    │                  │                 │
│  │ • Interfaz web  │    │ • Endpoints      │                 │
│  │ • Visualizaciones│    │ • Predicciones   │                 │
│  │ • Análisis batch│    │ • Documentación  │                 │
│  └─────────────────┘    └──────────────────┘                 │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                  SERVICIOS CORE                             │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐    ┌──────────────────┐                 │
│  │   Motor de      │    │   Sistema de     │                 │
│  │   Predicciones  │    │   MLflow         │                 │
│  │                 │    │                  │                 │
│  │ • Modelos ML    │    │ • Tracking       │                 │
│  │ • Preprocesamiento│   │ • Model Registry │                 │
│  │ • Validación    │    │ • Experimentación│                 │
│  └─────────────────┘    └──────────────────┘                 │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                  BASES DE DATOS                             │
├─────────────────────────────────────────────────────────────┘
│  ┌─────────────────┐    ┌──────────────────┐                 │
│  │   PostgreSQL    │    │   Modelos ML     │                 │
│  │                 │    │                  │                 │
│  │ • Datos clínicos│    │ • Modelos       │                 │
│  │ • Configuraciones│   │   entrenados    │                 │
│  │ • Logs          │    │ • Artefactos     │                 │
│  └─────────────────┘    └──────────────────┘                 │
└─────────────────────────────────────────────────────────────┘
```

---

## 🏛️ Arquitectura Detallada

### **1. Capa de Presentación**

#### **Dashboard Streamlit**
```python
# Características principales:
- Interfaz responsiva con Plotly
- Formulario de predicción individual
- Análisis batch con archivos CSV
- Visualizaciones interactivas
- Información del sistema y modelos
```

**Tecnologías:**
- Streamlit 1.20+
- Plotly/Dash
- Pandas/Numpy
- Requests para API calls

#### **API REST (FastAPI)**
```python
# Endpoints principales:
- GET  /health          # Health check del sistema
- GET  /docs            # Documentación automática
- GET  /model/info      # Información del modelo
- POST /predict         # Predicciones individuales
- GET  /models          # Lista de modelos disponibles
- GET  /features        # Características del modelo
```

**Características:**
- Documentación automática con Swagger
- Validación automática con Pydantic
- Manejo robusto de errores
- Logging estructurado

### **2. Capa de Lógica de Negocio**

#### **Motor de Predicciones**
```python
# predictor.py - Core del sistema
class DiabetesPredictor:
    def __init__(self, model_name="random_forest"):
        self.model_name = model_name
        self.model = None
        self.scaler = None

    def predict(self, patient_data):
        """Realizar predicción con datos del paciente"""
        # Preprocesamiento
        # Normalización
        # Predicción
        # Post-procesamiento
        # Retorno de resultados
```

**Modelos de ML:**
- Random Forest (baseline)
- Gradient Boosting
- XGBoost
- LightGBM
- Redes Neuronales (futuro)

#### **Sistema de Preprocesamiento**
```python
# data_preprocessor.py
class DataPreprocessor:
    def __init__(self):
        self.scaler = StandardScaler()
        self.categorical_encoders = {}

    def preprocess_patient_data(self, data):
        """Preprocesar datos de paciente"""
        # Manejo de valores faltantes
        # Codificación de variables categóricas
        # Normalización de variables numéricas
        # Validación de rangos
```

### **3. Capa de Datos**

#### **PostgreSQL Database**
```sql
-- Estructura principal:
- patients (datos de pacientes)
- predictions (historial de predicciones)
- models (información de modelos)
- configurations (configuraciones del sistema)
- logs (registro de actividades)
```

#### **Model Registry (MLflow)**
```
outputs/mlruns/
├── 0/                          # Experimento default
│   ├── abc123/                 # Run específico
│   │   ├── artifacts/          # Modelos y artefactos
│   │   ├── metrics/            # Métricas de rendimiento
│   │   ├── params/             # Parámetros del modelo
│   │   └── tags/               # Metadatos
│   └── meta.yaml               # Metadatos del experimento
└── 1/                          # Experimento de optimización
    └── def456/                 # Run de optimización
```

### **4. Capa de Infraestructura**

#### **Render Deployment**
```yaml
# render.yaml - Configuración de servicios
services:
  - type: web
    name: diabetes-api
    runtime: python3
    startCommand: python api.py --host 0.0.0.0 --port $PORT

  - type: web
    name: diabetes-streamlit
    runtime: python3
    startCommand: streamlit run web_app.py --server.headless true

  - type: web
    name: diabetes-mlflow
    runtime: python3
    startCommand: python scripts/mlflow_server.py

  - type: pserv
    name: diabetes-db
    # PostgreSQL configuration
```

---

## 🔧 Tecnologías Utilizadas

### **Backend**
- **Python 3.12** - Lenguaje principal
- **FastAPI** - Framework API REST
- **SQLAlchemy** - ORM para base de datos
- **MLflow** - Gestión de ML lifecycle

### **Machine Learning**
- **Scikit-learn** - Modelos tradicionales
- **XGBoost/LightGBM** - Modelos de boosting
- **Joblib** - Serialización de modelos
- **Pandas/Numpy** - Manipulación de datos

### **Frontend**
- **Streamlit** - Dashboard web
- **Plotly** - Visualizaciones interactivas
- **HTML/CSS/JS** - Interfaz de usuario

### **Base de Datos**
- **PostgreSQL** - Base de datos principal
- **SQLite** - Base de datos local (desarrollo)

### **DevOps**
- **Render** - Plataforma de despliegue
- **Git** - Control de versiones
- **GitHub** - Repositorio remoto

---

## 📊 Flujos de Datos

### **Flujo de Predicción Individual**
```
Usuario → Dashboard Streamlit → API REST → Motor de Predicciones
                                      ↓
                                 Preprocesamiento → Modelo ML → Post-procesamiento
                                      ↓
                                 Resultados → API REST → Dashboard → Usuario
```

### **Flujo de Análisis Batch**
```
Usuario → Subida de CSV → Dashboard → API REST → Procesamiento Batch
                                                    ↓
                                               Validación → Preprocesamiento
                                                    ↓
                                               Predicciones → Agregación
                                                    ↓
                                               Resultados → Dashboard → Usuario
```

### **Flujo de Entrenamiento de Modelos**
```
Investigador → Jupyter/Colab → MLflow Tracking → Entrenamiento
                                                        ↓
                                                   Validación → Registro
                                                        ↓
                                                   Despliegue → API REST
```

---

## 🔒 Seguridad y Cumplimiento

### **Medidas de Seguridad**
- ✅ **Autenticación JWT** para endpoints sensibles
- ✅ **Validación de datos** con Pydantic
- ✅ **Sanitización de inputs** en todos los endpoints
- ✅ **Rate limiting** para prevenir abuso
- ✅ **CORS configurado** para dominios autorizados

### **Cumplimiento Regulatorio**
- ✅ **GDPR** - Protección de datos de pacientes
- ✅ **HIPAA** - Estándares de salud (aplicable)
- ✅ **Logs de auditoría** para todas las operaciones
- ✅ **Anonimización** de datos sensibles

### **Privacidad**
- ✅ **Encriptación** de datos en tránsito (HTTPS)
- ✅ **Hashing** de información sensible
- ✅ **Control de acceso** basado en roles
- ✅ **Logs mínimos** para datos de pacientes

---

## 📈 Métricas y Monitoreo

### **Métricas de Rendimiento**
- **Latencia de API**: <2 segundos para predicciones
- **Disponibilidad**: 99.9% uptime objetivo
- **Throughput**: 1000+ predicciones por hora
- **Uso de recursos**: <70% CPU promedio

### **Métricas de ML**
- **Accuracy**: >85% en validación
- **Precision/Recall**: Balanceado para casos clínicos
- **F1-Score**: >0.80 en todos los modelos
- **AUC-ROC**: >0.85 para clasificación

### **Monitoreo**
- **Health checks** automáticos cada 5 minutos
- **Logs estructurados** con niveles apropiados
- **Alertas** para métricas críticas
- **Dashboards** de métricas en tiempo real

---

## 🚀 Escalabilidad

### **Estrategia de Escalado**
- **Horizontal**: Múltiples instancias en Render
- **Vertical**: Recursos asignados dinámicamente
- **Base de datos**: PostgreSQL con read replicas
- **Cache**: Implementación futura con Redis

### **Límites de Carga**
- **API**: 1000 requests/minuto por instancia
- **Dashboard**: 100 usuarios concurrentes
- **MLflow**: 500 experimentos activos
- **Base de datos**: Optimizada para 1M+ registros

---

## 🔄 Mantenimiento y Operaciones

### **Despliegue**
- **CI/CD**: Automático desde GitHub
- **Blue-Green**: Estrategia de despliegue
- **Rollback**: Capacidad de reversión rápida
- **Backups**: Diarios automáticos

### **Monitoreo**
- **Logs centralizados** en Render
- **Métricas** en dashboards personalizados
- **Alertas** configuradas para fallos críticos
- **Reportes** semanales de rendimiento

### **Mantenimiento**
- **Actualizaciones** de dependencias mensuales
- **Re-entrenamiento** de modelos trimestral
- **Optimización** de consultas regular
- **Limpieza** de datos antiguos

---

## 🎯 Roadmap de Mejoras

### **Corto Plazo (1-3 meses)**
- [ ] **Solucionar MLflow** en Render
- [ ] **Incorporar variables hormonales** en modelos
- [ ] **Implementar autenticación** robusta
- [ ] **Agregar más visualizaciones** en dashboard

### **Mediano Plazo (3-6 meses)**
- [ ] **Desarrollar API v2** con más endpoints
- [ ] **Implementar modelos específicos** para mujeres
- [ ] **Agregar soporte multi-idioma**
- [ ] **Integración con EHR** sistemas

### **Largo Plazo (6-12 meses)**
- [ ] **Biomarcador específico** para mujeres
- [ ] **Estudios clínicos** para validación
- [ ] **Expansión internacional**
- [ ] **Plataforma enterprise**

---

## 💡 Puntos Clave de la Arquitectura

### **Fortalezas**
1. **Modularidad**: Servicios independientes y escalables
2. **Robustez**: Manejo de errores y validaciones comprehensivas
3. **Escalabilidad**: Arquitectura preparada para crecimiento
4. **Mantenibilidad**: Código limpio y bien documentado
5. **Seguridad**: Cumplimiento con estándares de salud

### **Áreas de Mejora**
1. **MLflow**: Requiere optimización para Render
2. **Monitoreo avanzado**: Implementar logging más sofisticado
3. **Testing**: Cobertura de pruebas más amplia
4. **Documentación**: API docs más detallados

### **Innovaciones**
1. **Enfoque en mujeres**: Consideración de factores hormonales
2. **IA explicable**: Modelos interpretables para uso clínico
3. **Integración seamless**: Entre componentes del sistema
4. **Despliegue moderno**: En la nube con CI/CD

---

**Esta arquitectura representa un sistema robusto, escalable y clínicamente relevante para la predicción de diabetes, con un enfoque especial en las necesidades únicas de las poblaciones femeninas.**