"""
API REST para el Sistema Predictivo de Diabetes
Implementación con FastAPI para servir predicciones en producción
"""
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, validator
from typing import Dict, List, Optional, Any
import uvicorn
import logging
from datetime import datetime
import json

# Importar módulos del proyecto
from predictor import DiabetesPredictor, predict_glucose
from config import config

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Crear aplicación FastAPI
app = FastAPI(
    title="🏥 Sistema Predictivo de Diabetes API",
    description="API REST para predicción de diabetes usando machine learning",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelos Pydantic para validación de datos
class PatientData(BaseModel):
    """Modelo para datos del paciente"""
    edad: float = Field(..., ge=0, le=120, description="Edad en años")
    sexo: str = Field(..., regex="^(M|F)$", description="Sexo: M o F")
    imc: float = Field(..., ge=10, le=60, description="Índice de Masa Corporal")
    tas: float = Field(..., ge=60, le=250, description="Tensión Arterial Sistólica")
    tad: float = Field(..., ge=40, le=150, description="Tensión Arterial Diastólica")
    perimetro_abdominal: float = Field(..., ge=40, le=200, description="Perímetro abdominal en cm")
    frecuencia_cardiaca: Optional[float] = Field(None, ge=40, le=200, description="Frecuencia cardíaca")
    realiza_ejercicio: str = Field(..., regex="^(Si|No)$", description="¿Realiza ejercicio?")
    consume_alcohol: str = Field(..., regex="^(Nunca|Ocasional|Frecuente)$", description="Consumo de alcohol")
    fuma: str = Field(..., regex="^(Si|No)$", description="¿Fuma?")
    medicamentos_hta: str = Field(..., regex="^(Si|No)$", description="¿Toma medicamentos para hipertensión?")
    historia_familiar_dm: str = Field(..., regex="^(Si|No)$", description="Historia familiar de diabetes")
    diabetes_gestacional: str = Field(..., regex="^(Si|No)$", description="Diabetes gestacional (solo mujeres)")
    puntaje_findrisc: Optional[float] = Field(None, ge=0, le=26, description="Puntaje FINDRISC")
    riesgo_cardiovascular: Optional[float] = Field(None, ge=0, le=1, description="Riesgo cardiovascular")

    @validator('diabetes_gestacional')
    def validate_gestational_diabetes(cls, v, values):
        """Validar diabetes gestacional solo para mujeres"""
        if 'sexo' in values and values['sexo'] == 'M' and v == 'Si':
            raise ValueError('Los hombres no pueden tener diabetes gestacional')
        return v

class PredictionResponse(BaseModel):
    """Respuesta de predicción"""
    glucose_mg_dl: float
    category: str
    risk_level: str
    confidence: str
    interpretation: str
    timestamp: datetime
    model_version: str
    processing_time_ms: float

class ModelInfoResponse(BaseModel):
    """Información del modelo"""
    model_name: str
    r2_score: float
    training_date: str
    n_features: int
    feature_columns: List[str]
    status: str

class HealthResponse(BaseModel):
    """Respuesta de health check"""
    status: str
    timestamp: datetime
    version: str
    model_loaded: bool
    total_predictions: int

# Variables globales
predictor = None
prediction_counter = 0

def get_predictor() -> DiabetesPredictor:
    """Obtener instancia del predictor"""
    global predictor
    if predictor is None:
        predictor = DiabetesPredictor()
        logger.info("Predictor cargado exitosamente")
    return predictor

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check del servicio"""
    global prediction_counter
    predictor_instance = get_predictor()

    return HealthResponse(
        status="healthy",
        timestamp=datetime.now(),
        version="2.0.0",
        model_loaded=predictor_instance.model is not None,
        total_predictions=prediction_counter
    )

@app.get("/model/info", response_model=ModelInfoResponse)
async def get_model_info():
    """Obtener información del modelo"""
    predictor_instance = get_predictor()

    model_info = predictor_instance.get_model_info()
    if "error" in model_info:
        raise HTTPException(status_code=500, detail=model_info["error"])

    return ModelInfoResponse(
        model_name=model_info["model_name"],
        r2_score=model_info["r2_score"],
        training_date=model_info["training_date"],
        n_features=model_info["n_features"],
        feature_columns=model_info["feature_columns"],
        status="loaded"
    )

@app.post("/predict", response_model=PredictionResponse)
async def predict_diabetes(patient_data: PatientData, background_tasks: BackgroundTasks):
    """Predecir nivel de glucosa para un paciente"""
    import time
    start_time = time.time()

    try:
        global prediction_counter
        prediction_counter += 1

        # Convertir datos Pydantic a diccionario
        data_dict = patient_data.dict()

        # Hacer predicción
        result = predict_glucose(data_dict)

        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])

        processing_time = (time.time() - start_time) * 1000

        # Log de predicción
        logger.info(f"Predicción realizada: {result['glucose_mg_dl']} mg/dL - {result['category']}")

        # Tarea en background para logging
        background_tasks.add_task(log_prediction, patient_data.dict(), result)

        return PredictionResponse(
            glucose_mg_dl=result["glucose_mg_dl"],
            category=result["category"],
            risk_level=result["risk_level"],
            confidence=result["confidence"],
            interpretation=result["interpretation"],
            timestamp=datetime.now(),
            model_version="2.0.0",
            processing_time_ms=round(processing_time, 2)
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error en predicción: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

@app.post("/predict/batch")
async def predict_batch(patients_data: List[PatientData]):
    """Predecir para múltiples pacientes"""
    import time
    start_time = time.time()

    try:
        global prediction_counter
        results = []

        for patient_data in patients_data:
            # Convertir a diccionario
            data_dict = patient_data.dict()

            # Hacer predicción
            result = predict_glucose(data_dict)

            if "error" in result:
                result["error"] = f"Error en paciente: {result['error']}"

            results.append(result)
            prediction_counter += 1

        processing_time = (time.time() - start_time) * 1000
        logger.info(f"Predicción batch completada: {len(patients_data)} pacientes en {processing_time:.2f}ms")

        return {
            "results": results,
            "total_patients": len(patients_data),
            "processing_time_ms": round(processing_time, 2),
            "timestamp": datetime.now().isoformat()
        }

    except Exception as e:
        logger.error(f"Error en predicción batch: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error en batch: {str(e)}")

@app.get("/categories")
async def get_categories_info():
    """Obtener información sobre las categorías de predicción"""
    return {
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

@app.get("/features")
async def get_feature_info():
    """Obtener información sobre las características requeridas"""
    predictor_instance = get_predictor()

    model_info = predictor_instance.get_model_info()
    if "error" in model_info:
        raise HTTPException(status_code=500, detail=model_info["error"])

    features_info = {
        "required_features": model_info["feature_columns"],
        "total_features": len(model_info["feature_columns"]),
        "feature_types": {
            "numeric": ["edad", "imc", "tas", "tad", "perimetro_abdominal",
                       "frecuencia_cardiaca", "puntaje_findrisc", "riesgo_cardiovascular"],
            "categorical": ["sexo", "realiza_ejercicio", "consume_alcohol", "fuma",
                           "medicamentos_hta", "historia_familiar_dm", "diabetes_gestacional"],
            "derived": ["presion_arterial_media", "presion_pulso", "ratio_cintura_altura",
                       "imc_categoria", "edad_categoria", "edad_squared", "score_cv", "indice_salud"]
        }
    }

    return features_info

async def log_prediction(patient_data: dict, result: dict):
    """Log de predicción en background"""
    try:
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "patient_data": patient_data,
            "prediction": result,
            "glucose_value": result["glucose_mg_dl"],
            "category": result["category"]
        }

        # Guardar log en archivo (en producción usar base de datos)
        log_file = config.OUTPUTS_DIR / "api_predictions.log"
        with open(log_file, "a") as f:
            f.write(json.dumps(log_entry) + "\n")

    except Exception as e:
        logger.error(f"Error guardando log: {e}")

@app.on_event("startup")
async def startup_event():
    """Inicialización al arrancar la API"""
    logger.info("🚀 Iniciando API del Sistema Predictivo de Diabetes")
    logger.info(f"📁 Directorio de trabajo: {config.PROJECT_ROOT}")

    # Crear directorios necesarios
    config.OUTPUTS_DIR.mkdir(exist_ok=True)

    # Cargar predictor
    try:
        get_predictor()
        logger.info("✅ Predictor cargado exitosamente")
    except Exception as e:
        logger.error(f"❌ Error cargando predictor: {e}")

@app.on_event("shutdown")
async def shutdown_event():
    """Acciones al apagar la API"""
    logger.info("🛑 Apagando API del Sistema Predictivo de Diabetes")
    logger.info(f"📊 Total de predicciones realizadas: {prediction_counter}")

def main():
    """Función principal para ejecutar la API"""
    import argparse

    parser = argparse.ArgumentParser(description="API REST para Sistema Predictivo de Diabetes")
    parser.add_argument("--host", default="127.0.0.1", help="Host para la API")
    parser.add_argument("--port", type=int, default=8000, help="Puerto para la API")
    parser.add_argument("--reload", action="store_true", help="Recargar automáticamente")

    args = parser.parse_args()

    print("🏥 Sistema Predictivo de Diabetes API")
    print("=" * 50)
    print(f"📍 Host: {args.host}")
    print(f"🔌 Puerto: {args.port}")
    print(f"📚 Documentación: http://{args.host}:{args.port}/docs")
    print(f"🔄 Recarga automática: {'Sí' if args.reload else 'No'}")
    print("=" * 50)

    uvicorn.run(
        "api:app",
        host=args.host,
        port=args.port,
        reload=args.reload,
        log_level="info"
    )

if __name__ == "__main__":
    main()