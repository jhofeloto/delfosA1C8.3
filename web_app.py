"""
Interfaz Web para el Sistema Predictivo de Diabetes
Implementación con Streamlit para una interfaz amigable
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import json
from pathlib import Path

# Importar módulos del proyecto
from predictor import predict_glucose, DiabetesPredictor
from config import config

# Configuración de la página
st.set_page_config(
    page_title="🏥 Sistema Predictivo de Diabetes",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 0.25rem solid #1f77b4;
        margin: 0.5rem 0;
    }
    .prediction-result {
        font-size: 1.5rem;
        font-weight: bold;
        text-align: center;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .normal { background-color: #d4edda; color: #155724; }
    .prediabetes { background-color: #fff3cd; color: #856404; }
    .diabetes { background-color: #f8d7da; color: #721c24; }
</style>
""", unsafe_allow_html=True)

def main():
    """Función principal de la aplicación web"""
    st.markdown('<div class="main-header">🏥 Sistema Predictivo de Diabetes Mellitus Tipo 2</div>',
                unsafe_allow_html=True)

    # Sidebar con información
    with st.sidebar:
        st.header("ℹ️ Información del Sistema")

        # Cargar información del modelo
        try:
            predictor = DiabetesPredictor()
            model_info = predictor.get_model_info()

            if "error" not in model_info:
                st.success("✅ Modelo cargado correctamente")

                st.metric("Modelo", model_info["model_name"])
                st.metric("R² Score", f"{model_info['r2_score']:.4f}")
                st.metric("Características", model_info["n_features"])
                st.metric("Entrenamiento", model_info["training_date"][:10])
            else:
                st.error("❌ Error cargando el modelo")
                st.error(model_info["error"])

        except Exception as e:
            st.error(f"❌ Error: {e}")

        st.markdown("---")
        st.markdown("**📊 Métricas objetivo:**")
        st.markdown("- R² Score: > 0.85")
        st.markdown("- RMSE: < 10 mg/dL")
        st.markdown("- MAE: < 8 mg/dL")

        st.markdown("---")
        st.markdown("**🏥 Categorías:**")
        st.markdown("- **Normal:** < 100 mg/dL")
        st.markdown("- **Prediabetes:** 100-126 mg/dL")
        st.markdown("- **Diabetes:** > 126 mg/dL")

    # Tabs principales
    tab1, tab2, tab3, tab4 = st.tabs([
        "🔮 Predicción Individual",
        "📊 Análisis Batch",
        "📈 Visualizaciones",
        "ℹ️ Información"
    ])

    with tab1:
        individual_prediction_tab()

    with tab2:
        batch_analysis_tab()

    with tab3:
        visualizations_tab()

    with tab4:
        information_tab()

def individual_prediction_tab():
    """Tab para predicción individual"""
    st.header("🔮 Predicción para Paciente Individual")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📋 Datos Demográficos")
        edad = st.slider("Edad (años)", 18, 90, 45, help="Edad del paciente")
        sexo = st.selectbox("Sexo", ["M", "F"], help="Sexo del paciente")
        zona_residencia = st.selectbox("Zona de residencia", ["Urbana", "Rural"])

    with col2:
        st.subheader("🏥 Datos Clínicos")
        imc = st.slider("IMC", 15.0, 50.0, 25.0, 0.1, help="Índice de Masa Corporal")
        tas = st.slider("TAS (mmHg)", 90, 200, 120, help="Tensión Arterial Sistólica")
        tad = st.slider("TAD (mmHg)", 60, 120, 80, help="Tensión Arterial Diastólica")

    col3, col4 = st.columns(2)

    with col3:
        st.subheader("📏 Medidas Antropométricas")
        talla = st.slider("Talla (cm)", 140, 200, 165, help="Altura en centímetros")
        peso = st.slider("Peso (kg)", 40, 150, 70, help="Peso en kilogramos")
        perimetro_abdominal = st.slider("Perímetro abdominal (cm)", 60, 150, 90,
                                       help="Circunferencia de cintura")

    with col4:
        st.subheader("❤️ Factores de Riesgo")
        frecuencia_cardiaca = st.slider("Frecuencia cardíaca", 50, 110, 70)
        realiza_ejercicio = st.selectbox("¿Realiza ejercicio?", ["Si", "No"])
        fuma = st.selectbox("¿Fuma?", ["Si", "No"])
        consume_alcohol = st.selectbox("Consumo de alcohol",
                                      ["Nunca", "Ocasional", "Frecuente"])

    col5, col6 = st.columns(2)

    with col5:
        st.subheader("💊 Antecedentes Médicos")
        medicamentos_hta = st.selectbox("¿Toma medicamentos para hipertensión?", ["Si", "No"])
        historia_familiar_dm = st.selectbox("Historia familiar de diabetes", ["Si", "No"])
        diabetes_gestacional = st.selectbox("Diabetes gestacional",
                                           ["No", "Si"] if sexo == "F" else ["No"])

    with col6:
        st.subheader("📊 Scores de Riesgo")
        puntaje_findrisc = st.slider("Puntaje FINDRISC", 0, 26, 5,
                                    help="Puntuación FINDRISC (0-26)")
        riesgo_cardiovascular = st.slider("Riesgo cardiovascular", 0.0, 1.0, 0.2, 0.01,
                                         help="Riesgo cardiovascular (0-1)")

    # Botón de predicción
    if st.button("🔮 Realizar Predicción", type="primary", use_container_width=True):
        # Crear diccionario con datos del paciente
        patient_data = {
            "edad": edad,
            "sexo": sexo,
            "imc": imc,
            "tas": tas,
            "tad": tad,
            "perimetro_abdominal": perimetro_abdominal,
            "frecuencia_cardiaca": frecuencia_cardiaca,
            "realiza_ejercicio": realiza_ejercicio,
            "fuma": fuma,
            "consume_alcohol": consume_alcohol,
            "medicamentos_hta": medicamentos_hta,
            "historia_familiar_dm": historia_familiar_dm,
            "diabetes_gestacional": diabetes_gestacional,
            "puntaje_findrisc": puntaje_findrisc,
            "riesgo_cardiovascular": riesgo_cardiovascular
        }

        # Realizar predicción
        with st.spinner("Analizando datos del paciente..."):
            try:
                result = predict_glucose(patient_data)

                if "error" not in result:
                    display_prediction_result(result)
                else:
                    st.error(f"❌ Error en la predicción: {result['error']}")

            except Exception as e:
                st.error(f"❌ Error inesperado: {e}")

def display_prediction_result(result):
    """Mostrar resultado de predicción"""
    glucose = result["glucose_mg_dl"]
    category = result["category"]
    risk_level = result["risk_level"]
    confidence = result["confidence"]
    interpretation = result["interpretation"]

    # Determinar clase CSS según categoría
    css_class = {
        "Normal": "normal",
        "Prediabetes": "prediabetes",
        "Diabetes": "diabetes"
    }.get(category, "")

    # Mostrar resultado principal
    st.markdown(f'''
    <div class="prediction-result {css_class}">
        🩸 Glucosa estimada: {glucose:.1f} mg/dL<br>
        📊 Categoría: {category}<br>
        ⚠️ Nivel de riesgo: {risk_level}<br>
        🎯 Confianza: {confidence}
    </div>
    ''', unsafe_allow_html=True)

    # Métricas detalladas
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Glucosa", f"{glucose:.1f} mg/dL")

    with col2:
        st.metric("Categoría", category)

    with col3:
        st.metric("Riesgo", risk_level)

    # Interpretación
    st.info(f"💡 **Interpretación:** {interpretation}")

    # Gráfico de glucosa
    fig = go.Figure()

    # Líneas de referencia
    fig.add_hline(y=100, line_dash="dash", line_color="orange",
                  annotation_text="Prediabetes (100 mg/dL)")
    fig.add_hline(y=126, line_dash="dash", line_color="red",
                  annotation_text="Diabetes (126 mg/dL)")

    # Punto de predicción
    fig.add_trace(go.Scatter(
        x=["Paciente"],
        y=[glucose],
        mode='markers+text',
        marker=dict(size=15, color='blue'),
        text=[f"{glucose:.1f}"],
        textposition="top center",
        name="Predicción"
    ))

    fig.update_layout(
        title="Nivel de Glucosa Predicho",
        yaxis_title="Glucosa (mg/dL)",
        showlegend=False,
        height=300
    )

    st.plotly_chart(fig, use_container_width=True)

def batch_analysis_tab():
    """Tab para análisis batch"""
    st.header("📊 Análisis Batch de Pacientes")

    st.markdown("""
    Sube un archivo CSV con datos de múltiples pacientes para realizar predicciones en lote.
    El archivo debe contener las columnas requeridas por el modelo.
    """)

    # Ejemplo de formato
    with st.expander("📋 Formato de archivo requerido"):
        st.markdown("""
        El archivo CSV debe contener las siguientes columnas:

        **Columnas requeridas:**
        - `edad`, `sexo`, `imc`, `tas`, `tad`, `perimetro_abdominal`
        - `realiza_ejercicio`, `fuma`, `consume_alcohol`
        - `medicamentos_hta`, `historia_familiar_dm`, `diabetes_gestacional`
        - `puntaje_findrisc`, `riesgo_cardiovascular`

        **Ejemplo de fila:**
        ```csv
        edad,sexo,imc,tas,tad,perimetro_abdominal,realiza_ejercicio,fuma,...
        45,M,25.5,120,80,90,Si,No,Nunca,Si,No,No,5,0.2
        ```
        """)

    # Upload de archivo
    uploaded_file = st.file_uploader(
        "Subir archivo CSV",
        type=["csv"],
        help="Selecciona un archivo CSV con datos de pacientes"
    )

    if uploaded_file is not None:
        try:
            # Leer archivo
            df = pd.read_csv(uploaded_file)

            st.success(f"✅ Archivo cargado: {len(df)} pacientes")

            # Mostrar preview
            st.subheader("📋 Preview de datos")
            st.dataframe(df.head(), use_container_width=True)

            # Verificar columnas requeridas
            required_columns = [
                'edad', 'sexo', 'imc', 'tas', 'tad', 'perimetro_abdominal',
                'realiza_ejercicio', 'fuma', 'consume_alcohol',
                'medicamentos_hta', 'historia_familiar_dm', 'diabetes_gestacional',
                'puntaje_findrisc', 'riesgo_cardiovascular'
            ]

            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                st.error(f"❌ Columnas faltantes: {missing_columns}")
                return

            # Botón para procesar
            if st.button("🔮 Procesar Predicciones", type="primary"):
                process_batch_predictions(df)

        except Exception as e:
            st.error(f"❌ Error leyendo archivo: {e}")

def process_batch_predictions(df):
    """Procesar predicciones para múltiples pacientes"""
    from predictor import predict_glucose

    results = []

    progress_bar = st.progress(0)
    status_text = st.empty()

    for i, (_, patient) in enumerate(df.iterrows()):
        # Convertir fila a diccionario
        patient_dict = patient.to_dict()

        # Hacer predicción
        result = predict_glucose(patient_dict)

        # Agregar información del paciente
        result["paciente_id"] = i + 1
        result["edad"] = patient_dict.get("edad", 0)
        result["sexo"] = patient_dict.get("sexo", "Desconocido")

        results.append(result)

        # Actualizar progreso
        progress = (i + 1) / len(df)
        progress_bar.progress(progress)
        status_text.text(f"Procesando paciente {i + 1}/{len(df)}...")

    progress_bar.empty()
    status_text.empty()

    # Crear DataFrame con resultados
    results_df = pd.DataFrame(results)

    # Mostrar resultados
    st.success(f"✅ Predicciones completadas para {len(results_df)} pacientes")

    # Métricas generales
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        total_pacientes = len(results_df)
        st.metric("Total Pacientes", total_pacientes)

    with col2:
        normal_count = len(results_df[results_df["category"] == "Normal"])
        st.metric("Normal", normal_count)

    with col3:
        prediabetes_count = len(results_df[results_df["category"] == "Prediabetes"])
        st.metric("Prediabetes", prediabetes_count)

    with col4:
        diabetes_count = len(results_df[results_df["category"] == "Diabetes"])
        st.metric("Diabetes", diabetes_count)

    # Tabla de resultados
    st.subheader("📊 Resultados Detallados")

    # Reordenar columnas para mejor visualización
    display_columns = ["paciente_id", "edad", "sexo", "glucose_mg_dl",
                      "category", "risk_level", "confidence"]

    st.dataframe(
        results_df[display_columns].sort_values("glucose_mg_dl", ascending=False),
        use_container_width=True
    )

    # Descargar resultados
    csv = results_df.to_csv(index=False)
    st.download_button(
        label="📥 Descargar Resultados CSV",
        data=csv,
        file_name=f"predicciones_diabetes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv"
    )

    # Visualizaciones
    st.subheader("📈 Visualizaciones")

    col1, col2 = st.columns(2)

    with col1:
        # Distribución de categorías
        category_counts = results_df["category"].value_counts()
        fig = px.pie(
            values=category_counts.values,
            names=category_counts.index,
            title="Distribución de Categorías"
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Histograma de glucosa
        fig = px.histogram(
            results_df,
            x="glucose_mg_dl",
            nbins=20,
            title="Distribución de Niveles de Glucosa"
        )
        fig.add_vline(x=100, line_dash="dash", line_color="orange")
        fig.add_vline(x=126, line_dash="dash", line_color="red")
        st.plotly_chart(fig, use_container_width=True)

def visualizations_tab():
    """Tab para visualizaciones generales"""
    st.header("📈 Visualizaciones y Análisis")

    try:
        # Generar datos de ejemplo para visualizaciones
        from data_generator import create_sample_dataset

        df = create_sample_dataset(n_samples=200)

        # Agregar categorías
        def categorize_glucose(glucose):
            if glucose < 100:
                return "Normal"
            elif glucose <= 126:
                return "Prediabetes"
            else:
                return "Diabetes"

        df["categoria"] = df["Resultado"].apply(categorize_glucose)

        col1, col2 = st.columns(2)

        with col1:
            # Distribución por sexo
            fig = px.histogram(
                df,
                x="Resultado",
                color="sexo",
                marginal="box",
                title="Distribución de Glucosa por Sexo"
            )
            fig.add_vline(x=100, line_dash="dash", line_color="orange")
            fig.add_vline(x=126, line_dash="dash", line_color="red")
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # Correlación IMC vs Glucosa
            fig = px.scatter(
                df,
                x="imc",
                y="Resultado",
                color="categoria",
                title="IMC vs Nivel de Glucosa",
                labels={"Resultado": "Glucosa (mg/dL)"}
            )
            st.plotly_chart(fig, use_container_width=True)

        # Gráfico adicional
        st.subheader("📊 Análisis por Categoría")

        col3, col4 = st.columns(2)

        with col3:
            # Box plot por categoría
            fig = px.box(
                df,
                x="categoria",
                y="Resultado",
                color="categoria",
                title="Distribución de Glucosa por Categoría"
            )
            st.plotly_chart(fig, use_container_width=True)

        with col4:
            # Edad vs Glucosa
            fig = px.scatter(
                df,
                x="edad",
                y="Resultado",
                color="categoria",
                title="Edad vs Nivel de Glucosa",
                trendline="ols"
            )
            st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"❌ Error generando visualizaciones: {e}")

def information_tab():
    """Tab de información del sistema"""
    st.header("ℹ️ Información del Sistema")

    st.markdown("""
    ## 🏥 Sistema Predictivo de Diabetes Mellitus Tipo 2

    Este sistema utiliza **machine learning avanzado** para predecir niveles de glucosa
    en sangre y clasificar el riesgo de diabetes en pacientes.

    ### 🔬 Modelos Implementados

    El sistema incluye **13 modelos de machine learning** diferentes:
    """)

    models_info = {
        "Lineales": ["Linear Regression", "Ridge Regression", "Lasso Regression", "Elastic Net"],
        "Ensemble": ["Random Forest", "Extra Trees"],
        "Boosting": ["Gradient Boosting", "XGBoost", "LightGBM", "AdaBoost"],
        "Otros": ["SVM", "K-Nearest Neighbors", "Neural Network"]
    }

    for category, models in models_info.items():
        st.markdown(f"**{category}:** {', '.join(models)}")

    st.markdown("""
    ### 📊 Métricas de Rendimiento

    - **R² Score:** > 0.85 (coeficiente de determinación)
    - **RMSE:** < 10 mg/dL (error cuadrático medio)
    - **MAE:** < 8 mg/dL (error absoluto medio)

    ### 🏥 Categorías de Predicción

    - **Normal:** < 100 mg/dL - Bajo riesgo
    - **Prediabetes:** 100-126 mg/dL - Riesgo moderado
    - **Diabetes:** > 126 mg/dL - Alto riesgo

    ### ⚠️ Descargo de Responsabilidad

    Este sistema es una **herramienta de apoyo** para profesionales de la salud.
    **No sustituye** el juicio médico profesional ni los análisis de laboratorio.
    Siempre consultar con un médico para diagnósticos y tratamientos.
    """)

if __name__ == "__main__":
    main()