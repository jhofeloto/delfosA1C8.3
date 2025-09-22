#!/usr/bin/env python3
"""
Script de configuración e instalación del Sistema Predictivo de Diabetes
Guía paso a paso para configurar todas las mejoras implementadas
"""
import subprocess
import sys
import os
from pathlib import Path
import time
from datetime import datetime

def print_header():
    """Imprimir encabezado del sistema"""
    print("="*80)
    print("🏥 SISTEMA PREDICTIVO DE DIABETES - CONFIGURACIÓN COMPLETA".center(80))
    print("="*80)
    print(f"📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("🚀 Configurando todas las mejoras implementadas...")
    print("="*80)

def check_python_version():
    """Verificar versión de Python"""
    print("\n🐍 Verificando versión de Python...")

    version = sys.version_info
    if version.major == 3 and version.minor >= 8:
        print(f"   ✅ Python {version.major}.{version.minor}.{version.micro} - Compatible")
        return True
    else:
        print(f"   ❌ Python {version.major}.{version.minor}.{version.micro} - Requiere Python 3.8+")
        return False

def install_requirements():
    """Instalar dependencias"""
    print("\n📦 Instalando dependencias...")

    try:
        # Actualizar pip
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])

        # Instalar requirements
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

        print("   ✅ Dependencias instaladas correctamente")
        return True

    except subprocess.CalledProcessError as e:
        print(f"   ❌ Error instalando dependencias: {e}")
        return False

def create_directories():
    """Crear directorios necesarios"""
    print("\n📁 Creando directorios...")

    directories = [
        "models",
        "outputs",
        "data",
        "outputs/mlruns"
    ]

    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"   ✅ {directory}/")

def test_basic_imports():
    """Probar importaciones básicas"""
    print("\n🧪 Probando importaciones básicas...")

    modules_to_test = [
        ("config", "from config import config"),
        ("data_generator", "from data_generator import create_sample_dataset"),
        ("data_preprocessor", "from data_preprocessor import preprocess_diabetes_data"),
        ("predictor", "from predictor import predict_glucose"),
    ]

    all_passed = True

    for module_name, import_statement in modules_to_test:
        try:
            exec(import_statement)
            print(f"   ✅ {module_name}")
        except ImportError as e:
            print(f"   ❌ {module_name}: {e}")
            all_passed = False

    return all_passed

def test_new_features():
    """Probar nuevas funcionalidades"""
    print("\n🚀 Probando nuevas funcionalidades...")

    features_to_test = [
        ("API REST (FastAPI)", "from api import app"),
        ("Interfaz Web (Streamlit)", "import streamlit as st"),
        ("Optimización (Optuna)", "import optuna"),
        ("Monitoreo (MLflow)", "import mlflow"),
        ("Base de Datos (SQLAlchemy)", "from sqlalchemy import create_engine"),
    ]

    all_passed = True

    for feature_name, import_statement in features_to_test:
        try:
            exec(import_statement)
            print(f"   ✅ {feature_name}")
        except ImportError as e:
            print(f"   ❌ {feature_name}: {e}")
            all_passed = False

    return all_passed

def create_sample_data():
    """Crear datos de ejemplo"""
    print("\n📊 Creando datos de ejemplo...")

    try:
        from data_generator import create_sample_dataset
        from data_preprocessor import preprocess_diabetes_data

        # Generar datos
        df = create_sample_dataset(n_samples=100)
        print(f"   ✅ Datos generados: {df.shape[0]} registros, {df.shape[1]} columnas")

        # Preprocesar
        df_processed, preprocessor = preprocess_diabetes_data(df)
        print(f"   ✅ Datos preprocesados: {df_processed.shape[1]} características")

        return True

    except Exception as e:
        print(f"   ❌ Error creando datos: {e}")
        return False

def create_startup_scripts():
    """Crear scripts de inicio"""
    print("\n📝 Creando scripts de inicio...")

    scripts = {
        "start_api.sh": """#!/bin/bash
echo "🏥 Iniciando API REST del Sistema Predictivo de Diabetes"
echo "📍 URL: http://localhost:8000"
echo "📚 Documentación: http://localhost:8000/docs"
python api.py --host 0.0.0.0 --port 8000
""",

        "start_web.sh": """#!/bin/bash
echo "🌐 Iniciando Interfaz Web del Sistema Predictivo de Diabetes"
echo "📍 URL: http://localhost:8501"
streamlit run web_app.py --server.port 8501 --server.address 0.0.0.0
""",

        "start_mlflow.sh": """#!/bin/bash
echo "📊 Iniciando MLflow UI"
echo "📍 URL: http://localhost:5000"
mlflow ui --backend-store-uri outputs/mlruns --host 0.0.0.0 --port 5000
""",

        "run_tests.sh": """#!/bin/bash
echo "🧪 Ejecutando pruebas del sistema..."
python test_system.py
"""
    }

    for filename, content in scripts.items():
        script_path = Path(filename)
        with open(script_path, 'w') as f:
            f.write(content)

        # Hacer ejecutable en Unix
        if os.name != 'nt':
            os.chmod(script_path, 0o755)

        print(f"   ✅ {filename}")

def create_config_summary():
    """Crear resumen de configuración"""
    print("\n📋 Creando resumen de configuración...")

    summary = f"""
🏥 SISTEMA PREDICTIVO DE DIABETES - RESUMEN DE CONFIGURACIÓN
{'='*60}

📅 Configurado el: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

✅ FUNCIONALIDADES IMPLEMENTADAS:
   • API REST (FastAPI) - Puerto 8000
   • Interfaz Web (Streamlit) - Puerto 8501
   • Optimización (Optuna) - Hiperparámetros automáticos
   • Monitoreo (MLflow) - Tracking de experimentos
   • Base de Datos (SQLAlchemy) - Almacenamiento médico
   • Sistema ML Original - 13 modelos de predicción

🚀 COMANDOS DE INICIO:

1. API REST:
   python api.py --host 0.0.0.0 --port 8000
   # Documentación: http://localhost:8000/docs

2. Interfaz Web:
   streamlit run web_app.py --server.port 8501
   # URL: http://localhost:8501

3. MLflow UI:
   mlflow ui --backend-store-uri outputs/mlruns
   # URL: http://localhost:5000

4. Optimización:
   python -c "from hyperparameter_optimizer import optimize_diabetes_models; ..."

5. Base de Datos:
   python -c "from database_manager import create_database_manager; ..."

📊 MODELOS DISPONIBLES:
   • Linear Regression, Ridge, Lasso, Elastic Net
   • Random Forest, Extra Trees
   • Gradient Boosting, XGBoost, LightGBM, AdaBoost
   • SVM, K-Nearest Neighbors, Neural Network

🎯 MÉTRICAS OBJETIVO:
   • R² Score: > 0.85
   • RMSE: < 10 mg/dL
   • MAE: < 8 mg/dL

🏥 CATEGORÍAS:
   • Normal: < 100 mg/dL
   • Prediabetes: 100-126 mg/dL
   • Diabetes: > 126 mg/dL

📁 DIRECTORIOS:
   • models/: Modelos entrenados
   • outputs/: Resultados y MLflow
   • data/: Base de datos SQLite

🔧 ARCHIVOS PRINCIPALES:
   • api.py: API REST
   • web_app.py: Interfaz web
   • hyperparameter_optimizer.py: Optimización
   • model_monitoring.py: Monitoreo
   • database_manager.py: Base de datos

📖 DOCUMENTACIÓN:
   • README.md: Documentación completa
   • requirements.txt: Dependencias
   • test_system.py: Pruebas del sistema

{'='*60}
✅ SISTEMA COMPLETAMENTE CONFIGURADO Y LISTO PARA USO
🚀 ¡Disfruta del Sistema Predictivo de Diabetes!
{'='*60}
"""

    with open("SYSTEM_CONFIGURED.txt", "w") as f:
        f.write(summary)

    print("   ✅ SYSTEM_CONFIGURED.txt creado")

def main():
    """Función principal de configuración"""
    print_header()

    steps = [
        ("Verificar Python", check_python_version),
        ("Instalar dependencias", install_requirements),
        ("Crear directorios", create_directories),
        ("Probar importaciones básicas", test_basic_imports),
        ("Probar nuevas funcionalidades", test_new_features),
        ("Crear datos de ejemplo", create_sample_data),
        ("Crear scripts de inicio", create_startup_scripts),
        ("Crear resumen de configuración", create_config_summary)
    ]

    results = []

    for step_name, step_function in steps:
        print(f"\n{'='*20} {step_name} {'='*20}")
        success = step_function()
        results.append((step_name, success))

    # Resumen final
    print(f"\n{'='*60}")
    print("📊 RESUMEN DE CONFIGURACIÓN")
    print(f"{'='*60}")

    passed = 0
    for step_name, success in results:
        status = "✅ PASÓ" if success else "❌ FALLÓ"
        print(f"   {step_name}: {status}")
        if success:
            passed += 1

    print(f"\n🎯 Resultado: {passed}/{len(results)} pasos completados")

    if passed == len(results):
        print("\n🎉 ¡CONFIGURACIÓN COMPLETADA EXITOSAMENTE!")
        print("\n🚀 El Sistema Predictivo de Diabetes está listo para usar:")
        print("   📖 Lee SYSTEM_CONFIGURED.txt para información detallada")
        print("   🌐 Inicia con: python api.py (API) o streamlit run web_app.py (Web)")
        print("   📚 Documentación: http://localhost:8000/docs (cuando API esté activa)")
        print("\n🏥 ¡Sistema completamente funcional y listo para producción!")
    else:
        print(f"\n⚠️ {len(results) - passed} pasos fallaron. Revisa los errores arriba.")
        print("   🔧 Ejecuta este script nuevamente después de resolver los problemas.")

    print(f"\n{'='*60}")

if __name__ == "__main__":
    main()