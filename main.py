from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import mlflow.pyfunc
import pandas as pd
import os
import logging
import uvicorn
from pathlib import Path

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Sistema de Biomarcadores Digitales", version="1.0")

# Configurar templates
templates = Jinja2Templates(directory="templates")

# Crear directorio de templates si no existe
Path("templates").mkdir(exist_ok=True)

# Modelos de datos
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

# Cargar modelo desde MLflow
MODEL_PATH = "mlruns/108607450594143967/models/m-730c6a883fbf45328c26ad5142068bf2/artifacts"
model = None

def load_model():
    global model
    if model is None:
        try:
            # Intentar cargar modelo desde ruta específica
            model = mlflow.pyfunc.load_model(MODEL_PATH)
            logger.info("✅ Modelo cargado desde MLflow")
        except Exception as e:
            logger.error(f"Error cargando modelo desde {MODEL_PATH}: {e}")
            try:
                # Fallback a modelo local
                model = mlflow.pyfunc.load_model("mlruns/0/model")
                logger.warning("⚠️ Usando modelo fallback")
            except Exception as e2:
                logger.error(f"Error cargando modelo fallback: {e2}")
                raise Exception("No se pudo cargar ningún modelo")

load_model()

# Página principal - Dashboard
@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

# Endpoint de predicción
@app.post("/predict")
async def predict(request: PredictionRequest):
    try:
        # Preparar datos para predicción
        data = pd.DataFrame([request.dict()])

        # Hacer predicción
        prediction = model.predict(data)

        # Intentar obtener probabilidades si el modelo las soporta
        try:
            probability = model.predict_proba(data)
            prob_value = float(probability[0][1])
        except AttributeError:
            # Si el modelo no soporta predict_proba, usar la predicción como proxy
            prob_value = float(prediction[0])

        return {
            "prediction": int(prediction[0]),
            "probability": prob_value,
            "risk_level": "High" if prob_value > 0.7 else "Medium" if prob_value > 0.3 else "Low"
        }

    except Exception as e:
        logger.error(f"Error en predicción: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Health check para Render
@app.get("/health")
async def health_check():
    return {"status": "healthy", "model_version": "1.0", "service": "delfos-biomarkers"}

# Página de información
@app.get("/info", response_class=HTMLResponse)
async def info(request: Request):
    return templates.TemplateResponse("info.html", {"request": request})

# Configurar host y puerto para Render
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")

    logger.info(f"🚀 Iniciando servidor en {host}:{port}")
    uvicorn.run(app, host=host, port=port)