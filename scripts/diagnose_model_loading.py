#!/usr/bin/env python3
"""
Script para diagnosticar problemas de carga de modelos en Render
"""
import os
import sys
from pathlib import Path
import joblib
import json
import traceback

def diagnose_model_loading():
    """Diagnosticar problemas de carga de modelos"""
    print("🔍 DIAGNÓSTICO DE CARGA DE MODELOS")
    print("=" * 50)

    # Verificar directorio de modelos
    models_dir = Path("models")
    if not models_dir.exists():
        print(f"❌ Directorio de modelos no existe: {models_dir}")
        return False

    print(f"✅ Directorio de modelos encontrado: {models_dir}")

    # Listar archivos en models
    model_files = list(models_dir.glob("*.joblib"))
    print(f"📁 Archivos .joblib encontrados: {len(model_files)}")
    for file in model_files:
        size_mb = file.stat().st_size / (1024 * 1024)
        print(f"   • {file.name} ({size_mb:.2f} MB)")

    # Verificar best_model.joblib específicamente
    best_model_path = models_dir / "best_model.joblib"
    if not best_model_path.exists():
        print(f"❌ best_model.joblib no encontrado en: {best_model_path}")
        return False

    print(f"✅ best_model.joblib encontrado: {best_model_path}")

    # Verificar scaler
    scaler_path = models_dir / "scaler.joblib"
    if not scaler_path.exists():
        print(f"⚠️ scaler.joblib no encontrado: {scaler_path}")
    else:
        print(f"✅ scaler.joblib encontrado: {scaler_path}")

    # Verificar metadata
    metadata_path = models_dir / "model_metadata.json"
    if not metadata_path.exists():
        print(f"⚠️ model_metadata.json no encontrado: {metadata_path}")
    else:
        print(f"✅ model_metadata.json encontrado: {metadata_path}")

    # Intentar cargar el modelo
    print("\n🔄 INTENTANDO CARGAR EL MODELO...")
    try:
        print(f"   Cargando: {best_model_path}")
        model = joblib.load(best_model_path)
        print("✅ Modelo cargado exitosamente")
        print(f"   Tipo: {type(model)}")

        # Verificar que sea un modelo válido
        if hasattr(model, 'predict'):
            print("✅ Modelo tiene método predict")
        else:
            print("❌ Modelo no tiene método predict")
            return False

        # Verificar scaler
        if scaler_path.exists():
            scaler = joblib.load(scaler_path)
            print("✅ Scaler cargado exitosamente")
            print(f"   Tipo: {type(scaler)}")
        else:
            print("⚠️ Scaler no disponible")

        # Verificar metadata
        if metadata_path.exists():
            with open(metadata_path, 'r') as f:
                metadata = json.load(f)
            print("✅ Metadata cargada exitosamente")
            print(f"   Modelo: {metadata.get('best_model', 'N/A')}")
            print(f"   R² Score: {metadata.get('best_r2_score', 'N/A')}")
            print(f"   Características: {len(metadata.get('feature_columns', []))}")

        return True

    except Exception as e:
        print(f"❌ ERROR CARGANDO MODELO: {e}")
        print("\n📋 TRACEBACK COMPLETO:")
        traceback.print_exc()
        return False

def test_prediction():
    """Probar una predicción simple"""
    print("\n🧪 PROBANDO PREDICCIÓN...")
    try:
        from predictor import DiabetesPredictor

        # Datos de prueba simples
        test_data = {
            'edad': 50,
            'sexo': 'M',
            'imc': 25.0,
            'tas': 120,
            'tad': 80,
            'perimetro_abdominal': 90,
            'frecuencia_cardiaca': 70,
            'realiza_ejercicio': 'No',
            'fuma': 'No',
            'historia_familiar_dm': 'No',
            'puntaje_findrisc': 5,
            'riesgo_cardiovascular': 0.2
        }

        predictor = DiabetesPredictor()
        result = predictor.predict(test_data)

        if "error" in result:
            print(f"❌ Error en predicción: {result['error']}")
            return False
        else:
            print("✅ Predicción exitosa:")
            print(f"   Glucosa: {result['glucose_mg_dl']} mg/dL")
            print(f"   Categoría: {result['category']}")
            print(f"   Riesgo: {result['risk_level']}")
            return True

    except Exception as e:
        print(f"❌ Error en predicción: {e}")
        traceback.print_exc()
        return False

def check_environment():
    """Verificar variables de entorno críticas"""
    print("\n🌍 VARIABLES DE ENTORNO:")
    critical_vars = [
        'ENVIRONMENT', 'DEBUG', 'LOG_LEVEL', 'SECRET_KEY', 'JWT_SECRET_KEY',
        'API_HOST', 'API_PORT', 'STREAMLIT_SERVER_ADDRESS', 'STREAMLIT_SERVER_PORT',
        'STREAMLIT_SERVER_HEADLESS', 'MLFLOW_TRACKING_URI', 'MLFLOW_HOST', 'MLFLOW_PORT'
    ]

    for var in critical_vars:
        value = os.getenv(var)
        if value is None:
            print(f"   ❌ {var}: NO DEFINIDA")
        else:
            # No mostrar valores sensibles completos
            if 'SECRET' in var or 'KEY' in var:
                print(f"   ✅ {var}: {'*' * len(value)}")
            else:
                print(f"   ✅ {var}: {value}")

def main():
    """Función principal"""
    print("🚀 DIAGNÓSTICO COMPLETO DEL SISTEMA")
    print("=" * 60)

    # Verificar entorno
    check_environment()

    # Diagnosticar carga de modelos
    model_loaded = diagnose_model_loading()

    if model_loaded:
        # Probar predicción
        prediction_ok = test_prediction()

        if prediction_ok:
            print("\n🎉 DIAGNÓSTICO COMPLETADO: TODO FUNCIONA CORRECTAMENTE")
            return True
        else:
            print("\n⚠️ DIAGNÓSTICO COMPLETADO: PROBLEMA EN PREDICCIÓN")
            return False
    else:
        print("\n❌ DIAGNÓSTICO COMPLETADO: PROBLEMA EN CARGA DE MODELOS")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)