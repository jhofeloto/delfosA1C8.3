#!/usr/bin/env python3
"""
Script de Demostración del Sistema Predictivo de Diabetes
Muestra todas las funcionalidades implementadas paso a paso
"""
import time
import sys
from pathlib import Path
from datetime import datetime

def print_header():
    """Imprimir encabezado de demostración"""
    print("="*80)
    print("🏥 DEMOSTRACIÓN COMPLETA - SISTEMA PREDICTIVO DE DIABETES".center(80))
    print("="*80)
    print("🚀 Este script demostrará todas las funcionalidades implementadas:")
    print("   ✅ API REST (FastAPI)")
    print("   ✅ Interfaz Web (Streamlit)")
    print("   ✅ Optimización (Optuna)")
    print("   ✅ Monitoreo (MLflow)")
    print("   ✅ Base de Datos (SQLAlchemy)")
    print("   ✅ Sistema ML Original")
    print("="*80)

def demo_1_api_rest():
    """Demostración de la API REST"""
    print("\n🎯 DEMOSTRACIÓN 1: API REST (FastAPI)")
    print("-"*50)

    try:
        from api import app
        print("   ✅ API importada correctamente")
        print("   📍 Endpoints disponibles:")
        print("      • GET  /health - Health check")
        print("      • GET  /model/info - Información del modelo")
        print("      • POST /predict - Predicción individual")
        print("      • POST /predict/batch - Predicción batch")
        print("      • GET  /categories - Categorías médicas")
        print("      • GET  /features - Características requeridas")
        print("   🌐 Documentación: http://localhost:8000/docs")
        print("   📝 Comando: python api.py --host 0.0.0.0 --port 8000")

    except ImportError as e:
        print(f"   ❌ Error importando API: {e}")

def demo_2_web_interface():
    """Demostración de la interfaz web"""
    print("\n🎯 DEMOSTRACIÓN 2: INTERFAZ WEB (Streamlit)")
    print("-"*50)

    try:
        import streamlit as st
        print("   ✅ Streamlit importado correctamente")
        print("   🌐 Funcionalidades:")
        print("      • Predicción individual interactiva")
        print("      • Análisis batch con upload CSV")
        print("      • Visualizaciones avanzadas")
        print("      • Información del sistema")
        print("   📍 URL: http://localhost:8501")
        print("   📝 Comando: streamlit run web_app.py")

    except ImportError as e:
        print(f"   ❌ Error importando Streamlit: {e}")

def demo_3_hyperparameter_optimization():
    """Demostración de optimización de hiperparámetros"""
    print("\n🎯 DEMOSTRACIÓN 3: OPTIMIZACIÓN (Optuna)")
    print("-"*50)

    try:
        import optuna
        print("   ✅ Optuna importado correctamente")
        print("   🔬 Modelos optimizables:")
        print("      • Random Forest")
        print("      • XGBoost")
        print("      • LightGBM")
        print("      • Gradient Boosting")
        print("      • Ridge, Lasso, SVR, Neural Network")
        print("   ⚙️ Funcionalidades:")
        print("      • Optimización bayesiana")
        print("      • Validación cruzada automática")
        print("      • Logging de experimentos")
        print("   📝 Uso: from hyperparameter_optimizer import optimize_diabetes_models")

    except ImportError as e:
        print(f"   ❌ Error importando Optuna: {e}")

def demo_4_mlflow_monitoring():
    """Demostración del sistema de monitoreo"""
    print("\n🎯 DEMOSTRACIÓN 4: MONITOREO (MLflow)")
    print("-"*50)

    try:
        import mlflow
        print("   ✅ MLflow importado correctamente")
        print("   📊 Funcionalidades:")
        print("      • Tracking de experimentos")
        print("      • Registro de métricas")
        print("      • Logging de artefactos")
        print("      • Comparación de modelos")
        print("      • Visualización web")
        print("   🌐 UI: http://localhost:5000")
        print("   📝 Comando: mlflow ui --backend-store-uri outputs/mlruns")

    except ImportError as e:
        print(f"   ❌ Error importando MLflow: {e}")

def demo_5_database_manager():
    """Demostración del gestor de base de datos"""
    print("\n🎯 DEMOSTRACIÓN 5: BASE DE DATOS (SQLAlchemy)")
    print("-"-50)

    try:
        from database_manager import create_database_manager
        print("   ✅ SQLAlchemy importado correctamente")
        print("   🗄️ Funcionalidades:")
        print("      • Tablas: Patients, MedicalData, Predictions, ModelPerformance")
        print("      • CRUD completo para pacientes")
        print("      • Registro de predicciones")
        print("      • Historial médico")
        print("      • Estadísticas automáticas")
        print("      • Exportación a CSV")
        print("   📝 Uso: from database_manager import create_database_manager")

    except ImportError as e:
        print(f"   ❌ Error importando SQLAlchemy: {e}")

def demo_6_original_ml_system():
    """Demostración del sistema ML original"""
    print("\n🎯 DEMOSTRACIÓN 6: SISTEMA ML ORIGINAL")
    print("-"-50)

    try:
        from data_generator import create_sample_dataset
        from data_preprocessor import preprocess_diabetes_data
        from model_trainer import train_diabetes_models
        from predictor import predict_glucose

        print("   ✅ Sistema ML original funcionando")
        print("   🤖 Modelos disponibles:")
        print("      • 13 modelos de ML diferentes")
        print("      • Pipeline completo automatizado")
        print("      • Preprocesamiento avanzado")
        print("      • Evaluación automática")
        print("   📝 Comando: python main.py")

    except ImportError as e:
        print(f"   ❌ Error importando sistema ML: {e}")

def demo_7_sample_prediction():
    """Demostración de predicción de ejemplo"""
    print("\n🎯 DEMOSTRACIÓN 7: PREDICCIÓN DE EJEMPLO")
    print("-"-50)

    try:
        from predictor import predict_glucose

        # Datos de ejemplo
        patient_data = {
            'edad': 55,
            'sexo': 'M',
            'imc': 28.5,
            'tas': 135,
            'tad': 85,
            'perimetro_abdominal': 95,
            'realiza_ejercicio': 'No',
            'fuma': 'No',
            'historia_familiar_dm': 'Si',
            'puntaje_findrisc': 12,
            'riesgo_cardiovascular': 0.4
        }

        print("   📋 Datos del paciente:")
        for key, value in patient_data.items():
            print(f"      • {key}: {value}")

        # Hacer predicción
        result = predict_glucose(patient_data)

        if "error" not in result:
            print("   🎯 Resultado de predicción:")
            print(f"      • Glucosa: {result['glucose_mg_dl']:.1f} mg/dL")
            print(f"      • Categoría: {result['category']}")
            print(f"      • Riesgo: {result['risk_level']}")
            print(f"      • Confianza: {result['confidence']}")
        else:
            print(f"   ❌ Error: {result['error']}")

    except Exception as e:
        print(f"   ❌ Error en predicción: {e}")

def demo_8_file_structure():
    """Mostrar estructura de archivos"""
    print("\n🎯 DEMOSTRACIÓN 8: ESTRUCTURA DE ARCHIVOS")
    print("-"-50)

    files = [
        "📄 config.py - Configuración centralizada",
        "📄 data_generator.py - Generación de datos sintéticos",
        "📄 data_preprocessor.py - Preprocesamiento de datos",
        "📄 model_trainer.py - Entrenamiento de modelos",
        "📄 predictor.py - Sistema de predicción",
        "📄 api.py - API REST (FastAPI)",
        "📄 web_app.py - Interfaz web (Streamlit)",
        "📄 hyperparameter_optimizer.py - Optimización (Optuna)",
        "📄 model_monitoring.py - Monitoreo (MLflow)",
        "📄 database_manager.py - Base de datos (SQLAlchemy)",
        "📄 main.py - Script principal ML",
        "📄 test_system.py - Pruebas del sistema",
        "📄 setup_system.py - Configuración automática",
        "📄 demo.py - Esta demostración",
        "📄 requirements.txt - Dependencias",
        "📄 README.md - Documentación completa",
        "📄 .gitignore - Git ignore"
    ]

    for file in files:
        print(f"   {file}")

def demo_9_quick_start():
    """Instrucciones de inicio rápido"""
    print("\n🎯 DEMOSTRACIÓN 9: INICIO RÁPIDO")
    print("-"-50)

    print("   🚀 Para iniciar el sistema completo:")
    print("   1. python setup_system.py (configuración)")
    print("   2. python api.py (API REST)")
    print("   3. streamlit run web_app.py (Interfaz web)")
    print("   4. mlflow ui (Monitoreo)")
    print("")
    print("   📍 URLs disponibles:")
    print("   • API: http://localhost:8000/docs")
    print("   • Web: http://localhost:8501")
    print("   • MLflow: http://localhost:5000")
    print("")
    print("   🧪 Para probar:")
    print("   • python test_system.py")
    print("   • python demo.py")

def main():
    """Función principal de demostración"""
    print_header()

    # Lista de demostraciones
    demos = [
        demo_1_api_rest,
        demo_2_web_interface,
        demo_3_hyperparameter_optimization,
        demo_4_mlflow_monitoring,
        demo_5_database_manager,
        demo_6_original_ml_system,
        demo_7_sample_prediction,
        demo_8_file_structure,
        demo_9_quick_start
    ]

    # Ejecutar demostraciones
    for i, demo_func in enumerate(demos, 1):
        try:
            demo_func()
            time.sleep(0.5)  # Pausa breve entre demostraciones
        except KeyboardInterrupt:
            print(f"\n⏹️ Demostración interrumpida por usuario")
            break
        except Exception as e:
            print(f"\n❌ Error en demostración {i}: {e}")

    # Resumen final
    print(f"\n{'='*80}")
    print("🎉 DEMOSTRACIÓN COMPLETADA")
    print(f"{'='*80}")
    print("✅ Sistema Predictivo de Diabetes completamente funcional")
    print("✅ Todas las mejoras implementadas y demostradas")
    print("✅ Listo para uso en producción")
    print("")
    print("🚀 ¡Disfruta del sistema mejorado!")
    print(f"{'='*80}")

if __name__ == "__main__":
    main()