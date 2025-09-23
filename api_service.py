
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mlflow.pyfunc
import pandas as pd
import os
import logging

logger = logging.getLogger(__name__)

app = FastAPI(title="Diabetes Prediction API", version="1.0")

class PredictionRequest(BaseModel):
    edad: int
    sexo: int
    imc: float
    tas: int
    tad: int
    perimetro_abdominal: float
    frecuencia_cardiaca: int
    realiza_ejercicio: int
    consume_alcohol: int
    fuma: int
    medicamentos_hta: int
    historia_familiar_dm: int
    diabetes_gestacional: int
    puntaje_findrisc: int
    riesgo_cardiovascular: float

    class Config:
        schema_extra = {
            "example": {
                "edad": 45,
                "sexo": 1,
                "imc": 28.5,
                "tas": 135,
                "tad": 85,
                "perimetro_abdominal": 95,
                "frecuencia_cardiaca": 75,
                "realiza_ejercicio": 1,
                "consume_alcohol": 1,
                "fuma": 0,
                "medicamentos_hta": 1,
                "historia_familiar_dm": 1,
                "diabetes_gestacional": 0,
                "puntaje_findrisc": 12,
                "riesgo_cardiovascular": 0.4
            }
        }

# Cargar modelo desde MLflow
MODEL_PATH = "mlruns/0/m-cdec1ae8d2c0473ead69f634473a4956/artifacts/model"
try:
    model = mlflow.pyfunc.load_model(MODEL_PATH)
    logger.info("✅ Modelo cargado desde MLflow")
except Exception as e:
    logger.error(f"Error cargando modelo: {e}")
    # Fallback a modelo local si existe
    try:
        model = mlflow.pyfunc.load_model("mlruns/0/model")
        logger.warning("⚠️ Usando modelo fallback")
    except:
        raise Exception("No se pudo cargar ningún modelo")

@app.post("/predict")
async def predict(request: PredictionRequest):
    try:
        # Preparar datos para predicción
        data = pd.DataFrame([request.dict()])

        # Hacer predicción
        prediction = model.predict(data)
        probability = model.predict_proba(data)

        return {
            "prediction": int(prediction[0]),
            "probability": float(probability[0][1]),
            "risk_level": "High" if probability[0][1] > 0.7 else "Medium" if probability[0][1] > 0.3 else "Low"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy", "model_version": "1.0"}

@app.get("/")
async def root():
    return {"message": "Diabetes Prediction API", "version": "1.0"}
