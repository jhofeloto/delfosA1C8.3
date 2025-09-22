#!/usr/bin/env python3
"""
Script de prueba para verificar el funcionamiento de diferentes modelos
"""
import requests
import json
from datetime import datetime

def test_api_models():
    """Probar diferentes modelos a través de la API"""
    base_url = "http://localhost:8002"

    # Datos de prueba
    test_patient = {
        "edad": 55,
        "sexo": "M",
        "imc": 28.5,
        "tas": 135,
        "tad": 85,
        "perimetro_abdominal": 95,
        "frecuencia_cardiaca": 75,
        "realiza_ejercicio": "No",
        "consume_alcohol": "Ocasional",
        "fuma": "No",
        "medicamentos_hta": "Si",
        "historia_familiar_dm": "Si",
        "diabetes_gestacional": "No",
        "puntaje_findrisc": 12,
        "riesgo_cardiovascular": 0.4
    }

    models = ["random_forest", "gradient_boosting"]

    print("🧪 Probando diferentes modelos via API")
    print("=" * 60)

    for model in models:
        try:
            url = f"{base_url}/models/{model}/predict"
            print(f"\n🔍 Probando modelo: {model}")

            response = requests.post(url, json=test_patient, timeout=30)

            if response.status_code == 200:
                result = response.json()
                print("✅ Éxito!")
                print(f"   Glucosa: {result['glucose_mg_dl']} mg/dL")
                print(f"   Categoría: {result['category']}")
                print(f"   Modelo: {result['model_version']}")
                print(f"   Tiempo: {result['processing_time_ms']}ms")
            else:
                print(f"❌ Error: {response.status_code}")
                print(f"   Respuesta: {response.text}")

        except Exception as e:
            print(f"❌ Error de conexión: {e}")

def test_mlflow_models():
    """Probar carga directa de modelos desde MLflow"""
    print("\n🔬 Probando carga directa desde MLflow")
    print("=" * 60)

    try:
        import mlflow.pyfunc

        models = {
            "Random Forest": "mlruns/108607450594143967/2b0bc40a5809462582fe4827a85d0567/artifacts/model",
            "Gradient Boosting": "mlruns/108607450594143967/7d8e8b5c65244e488b1a1431d11b4688/artifacts/model"
        }

        # Datos de prueba (necesitan preprocesamiento)
        test_data = [[55, 0, 25, 135, 85, 95, 75, 0, 0, 1, 1, 0, 12, 0.4,
                      103.33, 50, 0.95, 2, 2, 3025, 0.0, 1.0, 0, 1, 0]]

        for model_name, model_path in models.items():
            try:
                print(f"\n🔍 Cargando modelo: {model_name}")
                model = mlflow.pyfunc.load_model(model_path)
                print("✅ Modelo cargado exitosamente")

                # Hacer predicción
                prediction = model.predict(test_data)
                print(f"   Predicción: {prediction[0]:.2f} mg/dL")

            except Exception as e:
                print(f"❌ Error con {model_name}: {e}")

    except ImportError:
        print("❌ MLflow no disponible para testing directo")
    except Exception as e:
        print(f"❌ Error general: {e}")

def test_web_interface():
    """Verificar que la interfaz web esté funcionando"""
    print("\n🌐 Verificando interfaz web")
    print("=" * 60)

    try:
        response = requests.get("http://localhost:8501", timeout=10)
        if response.status_code == 200:
            print("✅ Interfaz web accesible en: http://localhost:8501")
            print("   - Deberías ver un selector de modelos en el sidebar")
            print("   - Prueba seleccionar diferentes modelos")
        else:
            print(f"❌ Interfaz web no accesible: {response.status_code}")
    except Exception as e:
        print(f"❌ No se puede conectar a la interfaz web: {e}")
        print("   Asegúrate de ejecutar: streamlit run web_app.py --server.port 8501")

def main():
    """Función principal de testing"""
    print("🏥 TESTING DEL SISTEMA PREDICTIVO DE DIABETES")
    print("=" * 60)
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # Verificar servicios
    test_web_interface()
    test_api_models()
    test_mlflow_models()

    print("\n" + "=" * 60)
    print("📋 RESUMEN DE TESTING:")
    print("✅ API disponible en: http://localhost:8002")
    print("✅ Documentación API: http://localhost:8002/docs")
    print("✅ Interfaz web: http://localhost:8501")
    print("✅ MLflow UI: http://localhost:5003")
    print()
    print("🔧 Modelos disponibles:")
    print("   - Random Forest")
    print("   - Gradient Boosting")
    print()
    print("📝 Para probar diferentes modelos:")
    print("   1. Web: Selecciona modelo en el sidebar")
    print("   2. API: Usa /models/{model_name}/predict")
    print("   3. MLflow: Carga modelos directamente desde la UI")

if __name__ == "__main__":
    main()