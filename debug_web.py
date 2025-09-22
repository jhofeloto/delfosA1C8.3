#!/usr/bin/env python3
"""
Script de debug para probar la carga de modelos en la interfaz web
"""
from predictor import DiabetesPredictor
import traceback

def test_model_loading():
    """Probar la carga de diferentes modelos"""
    print("🔍 Probando carga de modelos...")
    print("=" * 50)

    models_to_test = ["random_forest", "gradient_boosting"]

    for model_name in models_to_test:
        print(f"\n🧪 Probando modelo: {model_name}")

        try:
            # Crear predictor
            predictor = DiabetesPredictor(model_name=model_name)

            # Verificar si el modelo se cargó
            if predictor.model is not None:
                print("✅ Modelo cargado exitosamente")

                # Obtener información del modelo
                model_info = predictor.get_model_info()
                print(f"   📊 Información del modelo:")
                print(f"      - Nombre: {model_info.get('model_name', 'N/A')}")
                print(f"      - R² Score: {model_info.get('r2_score', 'N/A')}")
                print(f"      - Características: {model_info.get('n_features', 'N/A')}")

                # Probar una predicción simple
                test_data = {
                    "edad": 45,
                    "sexo": "M",
                    "imc": 25.5,
                    "tas": 120,
                    "tad": 80,
                    "perimetro_abdominal": 90,
                    "frecuencia_cardiaca": 70,
                    "realiza_ejercicio": "Si",
                    "fuma": "No",
                    "consume_alcohol": "Ocasional",
                    "medicamentos_hta": "No",
                    "historia_familiar_dm": "No",
                    "diabetes_gestacional": "No",
                    "puntaje_findrisc": 5,
                    "riesgo_cardiovascular": 0.2
                }

                result = predictor.predict(test_data)

                if "error" not in result:
                    print("✅ Predicción exitosa:")
                    print(f"      - Glucosa: {result['glucose_mg_dl']} mg/dL")
                    print(f"      - Categoría: {result['category']}")
                    print(f"      - Confianza: {result['confidence']}")
                else:
                    print(f"❌ Error en predicción: {result['error']}")

            else:
                print("❌ Modelo no se cargó correctamente")

        except Exception as e:
            print(f"❌ Error cargando modelo {model_name}: {e}")
            print("   Stack trace:")
            traceback.print_exc()

def test_fallback_system():
    """Probar el sistema de fallback"""
    print("\n🔄 Probando sistema de fallback...")
    print("=" * 50)

    try:
        # Probar carga directa desde archivos locales
        from config import config
        from pathlib import Path
        import joblib

        model_path = config.MODELS_DIR / "random_forest.joblib"

        if model_path.exists():
            print(f"✅ Archivo de modelo encontrado: {model_path}")

            # Cargar modelo directamente
            model = joblib.load(model_path)
            print("✅ Modelo cargado directamente desde archivo")

            # Verificar que es un modelo válido
            if hasattr(model, 'predict'):
                print("✅ Modelo tiene método predict")
            else:
                print("❌ Modelo no tiene método predict")

        else:
            print(f"❌ Archivo de modelo no encontrado: {model_path}")

    except Exception as e:
        print(f"❌ Error en sistema de fallback: {e}")
        traceback.print_exc()

def main():
    """Función principal de debug"""
    print("🔧 DEBUG DEL SISTEMA PREDICTIVO DE DIABETES")
    print("=" * 60)
    print("Diagnóstico de problemas de carga de modelos")
    print("=" * 60)

    test_model_loading()
    test_fallback_system()

    print("
" + "=" * 60)
    print("📋 RESUMEN DEL DEBUG:")
    print("Si ves errores arriba, estos indican el problema.")
    print("Los errores comunes son:")
    print("- Archivos de modelo no encontrados")
    print("- Errores de importación de MLflow")
    print("- Problemas de compatibilidad de versiones")
    print("- Errores en el preprocesamiento de datos")

if __name__ == "__main__":
    main()