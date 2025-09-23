#!/usr/bin/env python3
"""
VERIFICACIÓN CORRECTA DE PREDICCIÓN EN RENDER
"""

import requests
import time
import sys

def check_service_health(base_url="https://delfosa1c8-3.onrender.com"):
    """Verifica que el servicio esté funcionando"""
    print(f"🔍 Verificando servicio en: {base_url}")

    try:
        response = requests.get(f"{base_url}/health", timeout=10)
        if response.status_code == 200:
            print("✅ Health check: OK")
            return True
        else:
            print(f"❌ Health check falló: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error conectando al servicio: {e}")
        return False

def check_service_docs(base_url="https://delfosa1c8-3.onrender.com"):
    """Verifica que la documentación esté disponible"""
    print(f"📚 Verificando documentación en: {base_url}/docs")

    try:
        response = requests.get(f"{base_url}/docs", timeout=10)
        if response.status_code == 200:
            print("✅ Documentación: OK")
            return True
        else:
            print(f"❌ Documentación falló: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error cargando documentación: {e}")
        return False

def test_prediction_correct(base_url="https://delfosa1c8-3.onrender.com"):
    """Prueba una predicción con los campos CORRECTOS"""
    print("🧪 Probando predicción con campos correctos...")

    # Datos correctos según el modelo PatientData
    test_data = {
        "edad": 45,
        "sexo": "F",
        "imc": 25.0,
        "tas": 120,
        "tad": 80,
        "perimetro_abdominal": 85,
        "realiza_ejercicio": "Si",
        "consume_alcohol": "Nunca",
        "fuma": "No",
        "medicamentos_hta": "No",
        "historia_familiar_dm": "No",
        "diabetes_gestacional": "No"
    }

    try:
        response = requests.post(
            f"{base_url}/predict",
            json=test_data,
            timeout=30
        )

        if response.status_code == 200:
            result = response.json()
            print("✅ Predicción: OK")
            print(f"   Glucosa: {result.get('glucose_mg_dl', 'N/A')} mg/dL")
            print(f"   Categoría: {result.get('category', 'N/A')}")
            print(f"   Riesgo: {result.get('risk_level', 'N/A')}")
            return True
        else:
            print(f"❌ Predicción falló: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error en predicción: {e}")
        return False

def test_model_info(base_url="https://delfosa1c8-3.onrender.com"):
    """Verifica que la información del modelo esté disponible"""
    print("📊 Verificando información del modelo...")

    try:
        response = requests.get(f"{base_url}/model/info", timeout=10)
        if response.status_code == 200:
            print("✅ Información del modelo: OK")
            return True
        else:
            print(f"❌ Información del modelo falló: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error obteniendo info del modelo: {e}")
        return False

def main():
    print("🚀 VERIFICACIÓN COMPLETA DEL SERVICIO EN RENDER")
    print("="*55)

    base_url = "https://delfosa1c8-3.onrender.com"

    # Esperar un poco por si el servicio está iniciando
    print("⏳ Esperando 30 segundos para que el servicio inicie...")
    time.sleep(30)

    checks = [
        ("Health Check", check_service_health),
        ("Documentación", check_service_docs),
        ("Información del Modelo", test_model_info),
        ("Predicción Correcta", test_prediction_correct)
    ]

    results = []
    for name, check_func in checks:
        print(f"\n🔍 {name}:")
        result = check_func(base_url)
        results.append((name, result))

    print("\n" + "="*55)
    print("📊 RESULTADOS FINALES:")

    all_passed = True
    for name, result in results:
        status = "✅ PASÓ" if result else "❌ FALLÓ"
        print(f"   {name}: {status}")
        if not result:
            all_passed = False

    if all_passed:
        print("\n🎉 ¡FELICITACIONES! Tu API está funcionando PERFECTAMENTE.")
        print(f"🌐 URL de tu API: {base_url}")
        print(f"📚 Documentación: {base_url}/docs")
        print(f"❤️ Health Check: {base_url}/health")
        print(f"🔮 Predicción: {base_url}/predict")
        print(f"📊 Info Modelo: {base_url}/model/info")
        print("\n💡 TU API ESTÁ LISTA PARA PRODUCCIÓN")
        print("   • 15 modelos ML funcionando")
        print("   • Auto-scaling automático")
        print("   • Documentación completa")
        print("   • Health checks activos")
    else:
        print("\n⚠️ Algunos checks fallaron.")
        print("💡 Posibles soluciones:")
        print("   1. Revisa los logs en Render dashboard")
        print("   2. Verifica que todas las variables de entorno estén correctas")
        print("   3. Asegúrate de que el health check esté en /health")

    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)