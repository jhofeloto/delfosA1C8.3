#!/usr/bin/env python3
"""
Workflow Completo del Sistema de Biomarcadores Digitales
Ejecuta todo el pipeline desde entrenamiento hasta despliegue
"""
import os
import sys
import time
import subprocess
import pandas as pd
import numpy as np
import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report
from sklearn.preprocessing import StandardScaler
import requests
import json
from datetime import datetime
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DiabetesBiomarkerWorkflow:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.mlflow_tracking_uri = os.path.join(self.base_dir, "mlruns")
        self.models_dir = os.path.join(self.base_dir, "models")
        self.data_dir = os.path.join(self.base_dir, "data")

        # Configurar MLflow
        mlflow.set_tracking_uri(f"file://{self.mlflow_tracking_uri}")
        self.experiment_name = "Diabetes_Prediction_Complete"

        # Crear directorios necesarios
        os.makedirs(self.models_dir, exist_ok=True)
        os.makedirs(self.data_dir, exist_ok=True)

        logger.info("🚀 Iniciando Workflow Completo del Sistema de Biomarcadores Digitales")

    def generate_synthetic_data(self):
        """Generar datos sintéticos para entrenamiento"""
        logger.info("📊 Generando datos sintéticos médicos...")

        np.random.seed(42)
        n_samples = 2000

        # Generar características médicas realistas
        data = {
            'edad': np.random.randint(29, 70, n_samples),
            'sexo': np.random.randint(0, 2, n_samples),  # 0: Hombre, 1: Mujer
            'imc': np.random.normal(27, 5, n_samples).clip(18, 45),
            'tas': np.random.normal(125, 15, n_samples).clip(90, 180),
            'tad': np.random.normal(80, 10, n_samples).clip(60, 110),
            'perimetro_abdominal': np.random.normal(90, 15, n_samples).clip(60, 130),
            'frecuencia_cardiaca': np.random.normal(75, 12, n_samples).clip(50, 120),
            'realiza_ejercicio': np.random.randint(0, 2, n_samples),
            'consume_alcohol': np.random.randint(0, 3, n_samples),  # 0: Nunca, 1: Ocasional, 2: Frecuente
            'fuma': np.random.randint(0, 2, n_samples),
            'medicamentos_hta': np.random.randint(0, 2, n_samples),
            'historia_familiar_dm': np.random.randint(0, 2, n_samples),
            'diabetes_gestacional': np.random.randint(0, 2, n_samples),
            'puntaje_findrisc': np.random.randint(0, 27, n_samples),
            'riesgo_cardiovascular': np.random.beta(2, 5, n_samples)  # Distribución sesgada hacia valores bajos
        }

        # Crear DataFrame
        df = pd.DataFrame(data)

        # Generar variable objetivo basada en factores de riesgo
        # Probabilidad de diabetes basada en factores de riesgo
        prob_diabetes = (
            (df['edad'] > 45) * 0.15 +
            (df['imc'] > 30) * 0.20 +
            (df['tas'] > 140) * 0.15 +
            (df['tad'] > 90) * 0.10 +
            (df['perimetro_abdominal'] > 100) * 0.15 +
            (df['fuma'] == 1) * 0.10 +
            (df['historia_familiar_dm'] == 1) * 0.15 +
            (df['diabetes_gestacional'] == 1) * 0.20 +
            (df['puntaje_findrisc'] > 15) * 0.25 +
            (df['riesgo_cardiovascular'] > 0.3) * 0.10
        )

        # Normalizar probabilidades
        prob_diabetes = prob_diabetes / prob_diabetes.max()

        # Generar variable objetivo
        df['target_diabetes'] = np.random.binomial(1, prob_diabetes)

        # Asegurar balance de clases (aprox 20% positivos)
        n_positives = int(0.2 * n_samples)
        positive_indices = df[df['target_diabetes'] == 1].index[:n_positives]
        negative_indices = df[df['target_diabetes'] == 0].index

        # Balancear dataset
        balanced_indices = list(positive_indices) + list(np.random.choice(negative_indices, n_positives, replace=False))
        df_balanced = df.loc[balanced_indices].reset_index(drop=True)

        # Guardar datos
        data_path = os.path.join(self.data_dir, "medical_data.csv")
        df_balanced.to_csv(data_path, index=False)

        logger.info(f"✅ Datos generados y guardados en {data_path}")
        logger.info(f"   - Total de muestras: {len(df_balanced)}")
        logger.info(f"   - Casos positivos: {df_balanced['target_diabetes'].sum()}")
        logger.info(f"   - Casos negativos: {len(df_balanced) - df_balanced['target_diabetes'].sum()}")

        return df_balanced

    def preprocess_data(self, data):
        """Preprocesar datos para entrenamiento"""
        logger.info("🔧 Preprocesando datos...")

        # Separar características y objetivo
        feature_cols = [
            'edad', 'sexo', 'imc', 'tas', 'tad', 'perimetro_abdominal',
            'frecuencia_cardiaca', 'realiza_ejercicio', 'consume_alcohol',
            'fuma', 'medicamentos_hta', 'historia_familiar_dm',
            'diabetes_gestacional', 'puntaje_findrisc', 'riesgo_cardiovascular'
        ]

        X = data[feature_cols]
        y = data['target_diabetes']

        # Dividir datos
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )

        # Escalar características numéricas
        numeric_features = ['edad', 'imc', 'tas', 'tad', 'perimetro_abdominal',
                          'frecuencia_cardiaca', 'puntaje_findrisc', 'riesgo_cardiovascular']

        scaler = StandardScaler()
        X_train_scaled = X_train.copy()
        X_test_scaled = X_test.copy()

        X_train_scaled[numeric_features] = scaler.fit_transform(X_train[numeric_features])
        X_test_scaled[numeric_features] = scaler.transform(X_test[numeric_features])

        logger.info("✅ Datos preprocesados exitosamente")
        return X_train_scaled, X_test_scaled, y_train, y_test, scaler

    def train_models(self, X_train, X_test, y_train, y_test):
        """Entrenar múltiples modelos y seleccionar el mejor"""
        logger.info("🤖 Entrenando modelos...")

        # Configurar experimento
        experiment = mlflow.get_experiment_by_name(self.experiment_name)
        if experiment is None:
            experiment_id = mlflow.create_experiment(self.experiment_name)
        else:
            experiment_id = experiment.experiment_id

        models = {
            'RandomForest': RandomForestClassifier(
                n_estimators=100,
                max_depth=10,
                min_samples_split=5,
                random_state=42
            ),
            'GradientBoosting': GradientBoostingClassifier(
                n_estimators=100,
                learning_rate=0.1,
                max_depth=5,
                random_state=42
            )
        }

        best_model = None
        best_score = 0
        best_model_name = ""

        for name, model in models.items():
            logger.info(f"   Entrenando {name}...")

            with mlflow.start_run(experiment_id=experiment_id, run_name=f"{name}_Complete"):
                # Entrenar modelo
                model.fit(X_train, y_train)

                # Hacer predicciones
                predictions = model.predict(X_test)
                probabilities = model.predict_proba(X_test)[:, 1]

                # Calcular métricas
                accuracy = accuracy_score(y_test, predictions)
                precision = precision_score(y_test, predictions)
                recall = recall_score(y_test, predictions)
                f1 = f1_score(y_test, predictions)

                # Validación cruzada
                cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='accuracy')

                # Log de parámetros
                mlflow.log_params(model.get_params())

                # Log de métricas
                mlflow.log_metric("accuracy", accuracy)
                mlflow.log_metric("precision", precision)
                mlflow.log_metric("recall", recall)
                mlflow.log_metric("f1_score", f1)
                mlflow.log_metric("cv_accuracy_mean", cv_scores.mean())
                mlflow.log_metric("cv_accuracy_std", cv_scores.std())

                # Log del modelo
                mlflow.sklearn.log_model(model, "model")

                # Log de artefactos
                report = classification_report(y_test, predictions, output_dict=True)
                with open("classification_report.json", "w") as f:
                    json.dump(report, f, indent=2)
                mlflow.log_artifact("classification_report.json")

                logger.info(f"   ✅ {name}: Accuracy = {accuracy:.4f}, Precision = {precision:.4f}, Recall = {recall:.4f}, F1 = {f1:.4f}")
                # Seleccionar mejor modelo
                if accuracy > best_score:
                    best_score = accuracy
                    best_model = model
                    best_model_name = name

        logger.info(f"🏆 Mejor modelo: {best_model_name} (Accuracy: {best_score:.4f})")
        return best_model, best_model_name

    def register_model(self, model, model_name):
        """Registrar modelo en MLflow Model Registry"""
        logger.info(f"📦 Registrando modelo {model_name}...")

        try:
            # Crear nombre del modelo registrado
            registered_name = "diabetes_predictor"

            with mlflow.start_run(run_name=f"{registered_name}_registration"):
                # Log del modelo
                mlflow.sklearn.log_model(
                    model,
                    "model",
                    registered_model_name=registered_name
                )

                # Log de metadatos
                mlflow.set_tag("model_type", "ensemble")
                mlflow.set_tag("algorithm", model_name)
                mlflow.set_tag("version", "1.0")
                mlflow.set_tag("status", "production_ready")

                logger.info(f"✅ Modelo {registered_name} registrado exitosamente")
                return registered_name

        except Exception as e:
            logger.warning(f"⚠️ Error registrando modelo: {e}")
            logger.info("   Continuando sin registro formal...")
            return None

    def create_api_service(self):
        """Crear servicio API REST"""
        logger.info("🔌 Creando servicio API...")

        api_content = '''
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mlflow.pyfunc
import pandas as pd
import os

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

# Cargar modelo desde MLflow
MODEL_PATH = "models:/diabetes_predictor/Production"
try:
    model = mlflow.pyfunc.load_model(MODEL_PATH)
    logger.info("✅ Modelo cargado desde MLflow")
except:
    # Fallback a modelo local
    model = mlflow.pyfunc.load_model("mlruns/0/model")
    logger.warning("⚠️ Usando modelo fallback")

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
'''

        with open("api_service.py", "w") as f:
            f.write(api_content)

        logger.info("✅ Servicio API creado: api_service.py")

    def create_dashboard_service(self):
        """Crear servicio dashboard"""
        logger.info("📱 Creando servicio dashboard...")

        dashboard_content = '''
import streamlit as st
import requests
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Diabetes Prediction Dashboard", layout="wide")

def main():
    st.title("🏥 Sistema de Biomarcadores Digitales")

    st.sidebar.title("Navegación")
    page = st.sidebar.radio("Ir a", ["Predicción", "Análisis Batch", "Información"])

    if page == "Predicción":
        show_prediction_page()
    elif page == "Análisis Batch":
        show_batch_analysis_page()
    else:
        show_info_page()

def show_prediction_page():
    st.header("🔮 Predicción Individual")

    with st.form("prediction_form"):
        col1, col2, col3 = st.columns(3)

        with col1:
            edad = st.number_input("Edad", 18, 100, 45)
            sexo = st.selectbox("Sexo", ["Masculino", "Femenino"])
            imc = st.number_input("IMC", 15.0, 50.0, 25.0)

        with col2:
            tas = st.number_input("TAS (mmHg)", 80, 200, 120)
            tad = st.number_input("TAD (mmHg)", 50, 130, 80)
            perimetro_abdominal = st.number_input("Perímetro Abdominal (cm)", 50, 150, 85)

        with col3:
            frecuencia_cardiaca = st.number_input("Frecuencia Cardíaca", 40, 200, 70)
            puntaje_findrisc = st.number_input("Puntaje FINDRISC", 0, 26, 8)
            riesgo_cardiovascular = st.number_input("Riesgo Cardiovascular", 0.0, 1.0, 0.2)

        st.subheader("Factores de Riesgo")
        col1, col2, col3 = st.columns(3)

        with col1:
            realiza_ejercicio = st.selectbox("Realiza Ejercicio", ["Sí", "No"])
            consume_alcohol = st.selectbox("Consume Alcohol", ["Nunca", "Ocasional", "Frecuente"])

        with col2:
            fuma = st.selectbox("Fuma", ["No", "Sí"])
            medicamentos_hta = st.selectbox("Medicamentos HTA", ["No", "Sí"])

        with col3:
            historia_familiar_dm = st.selectbox("Historia Familiar DM", ["No", "Sí"])
            diabetes_gestacional = st.selectbox("Diabetes Gestacional", ["No", "Sí"])

        submitted = st.form_submit_button("🔮 Realizar Predicción")

        if submitted:
            data = {
                "edad": edad,
                "sexo": 0 if sexo == "Masculino" else 1,
                "imc": imc,
                "tas": tas,
                "tad": tad,
                "perimetro_abdominal": perimetro_abdominal,
                "frecuencia_cardiaca": frecuencia_cardiaca,
                "realiza_ejercicio": 1 if realiza_ejercicio == "Sí" else 0,
                "consume_alcohol": 0 if consume_alcohol == "Nunca" else 1 if consume_alcohol == "Ocasional" else 2,
                "fuma": 1 if fuma == "Sí" else 0,
                "medicamentos_hta": 1 if medicamentos_hta == "Sí" else 0,
                "historia_familiar_dm": 1 if historia_familiar_dm == "Sí" else 0,
                "diabetes_gestacional": 1 if diabetes_gestacional == "Sí" else 0,
                "puntaje_findrisc": puntaje_findrisc,
                "riesgo_cardiovascular": riesgo_cardiovascular
            }

            response = requests.post("http://localhost:8000/predict", json=data)

            if response.status_code == 200:
                result = response.json()

                st.success("✅ Predicción completada")

                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Predicción", "Diabetes" if result["prediction"] == 1 else "Sin Diabetes")
                with col2:
                    st.metric("Probabilidad", f"{result['probability']:.2%}")
                with col3:
                    st.metric("Nivel de Riesgo", result["risk_level"])

                if result["prediction"] == 1:
                    st.warning("⚠️ **Riesgo Alto de Diabetes** - Se recomienda evaluación médica inmediata")
                else:
                    st.info("✅ **Riesgo Bajo** - Mantener hábitos saludables")

            else:
                st.error(f"❌ Error en la predicción: {response.text}")

def show_batch_analysis_page():
    st.header("📊 Análisis Batch")
    st.info("Funcionalidad de análisis batch - Próximamente")

def show_info_page():
    st.header("ℹ️ Información del Sistema")
    st.write("Sistema de Biomarcadores Digitales para predicción de diabetes")
    st.write("Versión: 1.0")
    st.write("Modelos: Random Forest, Gradient Boosting")
    st.write("Framework: MLflow, FastAPI, Streamlit")

if __name__ == "__main__":
    main()
'''

        with open("dashboard_service.py", "w") as f:
            f.write(dashboard_content)

        logger.info("✅ Servicio dashboard creado: dashboard_service.py")

    def create_startup_script(self):
        """Crear script de inicio de servicios"""
        logger.info("🚀 Creando script de inicio...")

        startup_content = '''#!/bin/bash
# Script de inicio de servicios
echo "🚀 Iniciando Sistema de Biomarcadores Digitales..."

# 1. Iniciar MLflow UI
echo "📊 Iniciando MLflow UI..."
python -m mlflow ui --backend-store-uri mlruns --host 0.0.0.0 --port 5004 &

# 2. Iniciar API
echo "🔌 Iniciando API..."
uvicorn api_service:app --host 0.0.0.0 --port 8000 --workers 4 &

# 3. Iniciar Dashboard
echo "📱 Iniciando Dashboard..."
streamlit run dashboard_service.py --server.port 8501 --server.address 0.0.0.0 --server.headless true &

echo "✅ Todos los servicios iniciados"
echo "🌐 URLs de acceso:"
echo "   - MLflow UI: http://localhost:5004"
echo "   - API: http://localhost:8000/docs"
echo "   - Dashboard: http://localhost:8501"
echo ""
echo "Presiona Ctrl+C para detener todos los servicios"
'''

        with open("start_services.sh", "w") as f:
            f.write(startup_content)

        # Hacer ejecutable
        os.chmod("start_services.sh", 0o755)
        logger.info("✅ Script de inicio creado: start_services.sh")

    def validate_deployment(self):
        """Validar que todos los servicios estén funcionando"""
        logger.info("🔍 Validando despliegue...")

        services = {
            "mlflow": "http://localhost:5004",
            "api": "http://localhost:8000/health",
            "dashboard": "http://localhost:8501"
        }

        for service, url in services.items():
            max_retries = 10
            for i in range(max_retries):
                try:
                    response = requests.get(url, timeout=5)
                    if response.status_code == 200:
                        logger.info(f"✅ {service} está funcionando")
                        break
                    else:
                        logger.warning(f"⚠️ {service} respondió con código {response.status_code}")
                except:
                    logger.info(f"⏳ Esperando {service}... (intento {i+1}/{max_retries})")
                    time.sleep(5)

                if i == max_retries - 1:
                    logger.error(f"❌ {service} no está disponible después de {max_retries} intentos")
                    return False

        logger.info("🎉 ¡Todos los servicios están funcionando correctamente!")
        return True

    def run_workflow(self):
        """Ejecutar workflow completo"""
        logger.info("🚀 Iniciando Workflow Completo...")

        try:
            # 1. Generar datos
            data = self.generate_synthetic_data()

            # 2. Preprocesar datos
            X_train, X_test, y_train, y_test, scaler = self.preprocess_data(data)

            # 3. Entrenar modelos
            best_model, best_model_name = self.train_models(X_train, X_test, y_train, y_test)

            # 4. Registrar modelo
            registered_name = self.register_model(best_model, best_model_name)

            # 5. Crear servicios
            self.create_api_service()
            self.create_dashboard_service()
            self.create_startup_script()

            # 6. Validar despliegue
            if self.validate_deployment():
                logger.info("🎉 ¡Workflow completado exitosamente!")
                logger.info("")
                logger.info("📋 Resumen del Sistema:")
                logger.info(f"   - Modelo entrenado: {best_model_name}")
                logger.info(f"   - Modelo registrado: {registered_name}")
                logger.info("   - Servicios creados: API, Dashboard, MLflow UI")
                logger.info("   - Estado: ✅ Listo para producción")
                logger.info("")
                logger.info("🌐 Para iniciar los servicios:")
                logger.info("   ./start_services.sh")
                logger.info("")
                logger.info("📊 URLs de acceso:")
                logger.info("   - MLflow UI: http://localhost:5004")
                logger.info("   - API: http://localhost:8000/docs")
                logger.info("   - Dashboard: http://localhost:8501")
            else:
                logger.error("❌ Error en la validación del despliegue")
                return False

        except Exception as e:
            logger.error(f"❌ Error en el workflow: {e}")
            return False

        return True

def main():
    """Función principal"""
    workflow = DiabetesBiomarkerWorkflow()
    success = workflow.run_workflow()

    if success:
        print("\n🎉 ¡Workflow completado exitosamente!")
        print("\n📋 Servicios disponibles:")
        print("   🌐 MLflow UI: http://localhost:5004")
        print("   🔌 API REST: http://localhost:8000/docs")
        print("   📱 Dashboard: http://localhost:8501")
        print("\n🚀 Para iniciar todos los servicios:")
        print("   ./start_services.sh")
    else:
        print("\n❌ Error en el workflow")
        sys.exit(1)

if __name__ == "__main__":
    main()