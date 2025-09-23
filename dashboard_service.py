
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
