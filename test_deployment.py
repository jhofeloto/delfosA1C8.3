#!/usr/bin/env python3
"""
Script de prueba para verificar la configuración de deployment en Render
"""

import os
import sys
import requests
import time
import logging
from pathlib import Path

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_model_loading():
    """Probar carga del modelo MLflow"""
    try:
        import mlflow.pyfunc
        import pandas as pd

        MODEL_PATH = "mlruns/108607450594143967/models/m-730c6a883fbf45328c26ad5142068bf2/artifacts"

        logger.info("🔄 Probando carga del modelo...")
        model = mlflow.pyfunc.load_model(MODEL_PATH)

        # Probar predicción con datos de ejemplo
        test_data = pd.DataFrame([{
            'edad': 45,
            'sexo': 1,
            'imc': 28.5,
            'tas': 135,
            'tad': 85,
            'perimetro_abdominal': 95,
            'frecuencia_cardiaca': 75,
            'realiza_ejercicio': 1,
            'consume_alcohol': 1,
            'fuma': 0,
            'medicamentos_hta': 1,
            'historia_familiar_dm': 1,
            'diabetes_gestacional': 0,
            'puntaje_findrisc': 12,
            'riesgo_cardiovascular': 0.4
        }])

        prediction = model.predict(test_data)

        # Intentar obtener probabilidades si el modelo las soporta
        try:
            probability = model.predict_proba(test_data)
            prob_value = float(probability[0][1])
        except AttributeError:
            # Si el modelo no soporta predict_proba, usar la predicción como proxy
            prob_value = float(prediction[0])

        logger.info(f"✅ Modelo cargado exitosamente")
        logger.info(f"✅ Predicción de prueba: {prediction[0]}")
        logger.info(f"✅ Probabilidad: {prob_value:.3f}")
        return True

    except Exception as e:
        logger.error(f"❌ Error cargando modelo: {e}")
        return False

def test_fastapi_app():
    """Probar la aplicación FastAPI"""
    try:
        # Cambiar al directorio del proyecto
        os.chdir(Path(__file__).parent)

        # Importar la aplicación
        from main import app
        logger.info("✅ Aplicación FastAPI importada correctamente")
        return True

    except Exception as e:
        logger.error(f"❌ Error importando aplicación FastAPI: {e}")
        return False

def test_health_check():
    """Probar el endpoint de health check"""
    try:
        # Simular una petición al health check
        from main import health_check
        result = health_check()
        logger.info(f"✅ Health check funcionando: {result}")
        return True

    except Exception as e:
        logger.error(f"❌ Error en health check: {e}")
        return False

def test_environment_variables():
    """Verificar variables de entorno necesarias"""
    required_vars = ['PORT', 'PYTHON_VERSION']
    optional_vars = ['MLFLOW_TRACKING_URI', 'RENDER']

    logger.info("🔧 Verificando variables de entorno...")

    for var in required_vars:
        value = os.getenv(var)
        if value:
            logger.info(f"✅ {var}={value}")
        else:
            logger.warning(f"⚠️ {var} no está configurada")

    for var in optional_vars:
        value = os.getenv(var)
        if value:
            logger.info(f"✅ {var}={value}")
        else:
            logger.info(f"ℹ️ {var} no está configurada (opcional)")

    return True

def test_file_structure():
    """Verificar estructura de archivos necesaria"""
    required_files = [
        'main.py',
        'requirements.txt',
        'start_services.sh',
        'render.yaml',
        'Dockerfile',
        'templates/dashboard.html',
        'templates/info.html'
    ]

    required_dirs = [
        'mlruns',
        'templates'
    ]

    logger.info("📁 Verificando estructura de archivos...")

    all_files_ok = True
    for file_path in required_files:
        if Path(file_path).exists():
            logger.info(f"✅ {file_path}")
        else:
            logger.error(f"❌ {file_path} no encontrado")
            all_files_ok = False

    for dir_path in required_dirs:
        if Path(dir_path).exists() and Path(dir_path).is_dir():
            logger.info(f"✅ {dir_path}/")
        else:
            logger.error(f"❌ {dir_path}/ no encontrado")
            all_files_ok = False

    return all_files_ok

def main():
    """Función principal de prueba"""
    logger.info("🚀 Iniciando pruebas de deployment para Render")
    logger.info("=" * 50)

    tests = [
        ("Estructura de archivos", test_file_structure),
        ("Variables de entorno", test_environment_variables),
        ("Carga del modelo", test_model_loading),
        ("Aplicación FastAPI", test_fastapi_app),
        ("Health check", test_health_check),
    ]

    passed = 0
    total = len(tests)

    for test_name, test_func in tests:
        logger.info(f"\n🔍 Probando: {test_name}")
        logger.info("-" * 30)

        if test_func():
            passed += 1
            logger.info(f"✅ {test_name}: PASSED")
        else:
            logger.error(f"❌ {test_name}: FAILED")

    logger.info("\n" + "=" * 50)
    logger.info(f"📊 Resultados: {passed}/{total} pruebas pasaron")

    if passed == total:
        logger.info("🎉 ¡Todas las pruebas pasaron! El deployment debería funcionar correctamente.")
        logger.info("\n📋 Siguientes pasos:")
        logger.info("1. Confirmar que el servicio está configurado en Render")
        logger.info("2. Verificar que las variables de entorno estén configuradas")
        logger.info("3. Hacer push a la rama principal para trigger el deployment")
        logger.info("4. Monitorear los logs en Render dashboard")
        return 0
    else:
        logger.error("⚠️ Algunas pruebas fallaron. Revisa los errores antes del deployment.")
        return 1

if __name__ == "__main__":
    sys.exit(main())