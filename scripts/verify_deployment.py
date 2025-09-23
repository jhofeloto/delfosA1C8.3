#!/usr/bin/env python3
"""
VERIFICACIÓN POST-DEPLOYMENT EN RENDER
"""

import requests
import time
import sys

def check_api_health(base_url="https://diabetes-api.onrender.com"):
    """Verifica que la API esté funcionando"""
    print(f"🔍 Verificando API en: {base_url}")

    try:
        # Health check
        response = requests.get(f"{base_url}/health", timeout=10)
        if response.status_code == 200:
            print("✅ Health check: OK")
            return True
        else:
            print(f"❌ Health check falló: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error conectando a la API: {e}")
        return False

def check_api_docs(base_url="https://diabetes-api.onrender.com"):
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

def test_prediction(base_url="https://diabetes-api.onrender.com"):
    """Prueba una predicción con datos de ejemplo"""
    print("🧪 Probando predicción...")

    test_data = {
        "glucose": 120,
        "blood_pressure": 80,
        "insulin": 100,
        "bmi": 25.0,
        "age": 45,
        "skin_thickness": 20
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
            print(f"   Resultado: {result}")
            return True
        else:
            print(f"❌ Predicción falló: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error en predicción: {e}")
        return False

def main():
    print("🚀 VERIFICACIÓN DE DEPLOYMENT EN RENDER")
    print("="*50)

    base_url = "https://diabetes-api.onrender.com"

    # Esperar un poco por si el servicio está iniciando
    print("⏳ Esperando 30 segundos para que el servicio inicie...")
    time.sleep(30)

    checks = [
        ("Health Check", check_api_health),
        ("Documentación", check_api_docs),
        ("Predicción", test_prediction)
    ]

    results = []
    for name, check_func in checks:
        print(f"\n🔍 {name}:")
        result = check_func(base_url)
        results.append((name, result))

    print("\n" + "="*50)
    print("📊 RESULTADOS FINALES:")

    all_passed = True
    for name, result in results:
        status = "✅ PASÓ" if result else "❌ FALLÓ"
        print(f"   {name}: {status}")
        if not result:
            all_passed = False

    if all_passed:
        print("\n🎉 ¡FELICITACIONES! Tu API está funcionando perfectamente.")
        print(f"🌐 URL de tu API: {base_url}")
        print(f"📚 Documentación: {base_url}/docs")
        print(f"❤️ Health Check: {base_url}/health")
    else:
        print("\n⚠️ Algunos checks fallaron. Revisa los logs en Render.")
        print("💡 Posibles soluciones:")
        print("   1. Espera 2-3 minutos más")
        print("   2. Revisa los logs en el dashboard de Render")
        print("   3. Verifica que todas las variables de entorno estén correctas")

    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)