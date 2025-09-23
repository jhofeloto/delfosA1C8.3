#!/usr/bin/env python3
"""
Script completo para verificar el despliegue de todas las aplicaciones en Render
"""
import requests
import time
import sys
from datetime import datetime
import json

def check_service(name, url, health_path="/", expected_status=200, timeout=30):
    """Verificar un servicio individual"""
    try:
        print(f"🔍 Verificando {name}...")
        print(f"   URL: {url}{health_path}")

        response = requests.get(f"{url}{health_path}", timeout=timeout)
        status_code = response.status_code

        if status_code == expected_status:
            print("   ✅ Servicio funcionando")
            return True, status_code
        else:
            print(f"   ❌ Error HTTP {status_code}")
            return False, status_code

    except requests.exceptions.Timeout:
        print(f"   ⏰ Timeout ({timeout}s)")
        return False, "TIMEOUT"
    except requests.exceptions.ConnectionError:
        print("   🌐 Error de conexión")
        return False, "CONNECTION_ERROR"
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False, "ERROR"

def check_api_endpoints(base_url):
    """Verificar endpoints específicos de la API"""
    endpoints = [
        ("/health", "Health Check"),
        ("/docs", "Documentación API"),
        ("/model/info", "Información del Modelo"),
        ("/models", "Modelos Disponibles"),
        ("/categories", "Categorías"),
        ("/features", "Características")
    ]

    results = []
    for endpoint, description in endpoints:
        success, status = check_service(f"API {description}", base_url, endpoint)
        results.append((endpoint, success, status))

    return results

def check_streamlit_dashboard(base_url):
    """Verificar dashboard de Streamlit"""
    return check_service("Streamlit Dashboard", base_url, "/")

def check_mlflow_ui(base_url):
    """Verificar interfaz de MLflow"""
    return check_service("MLflow UI", base_url, "/")

def main():
    """Función principal"""
    print("🚀 VERIFICACIÓN COMPLETA DEL DESPLIEGUE EN RENDER")
    print("=" * 70)
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC")
    print()

    # URLs de los servicios (ajustar según el despliegue real)
    services = {
        "API REST": "https://delfosa1c8-3.onrender.com",
        "Streamlit Dashboard": "https://diabetes-streamlit.onrender.com",
        "MLflow UI": "https://diabetes-mlflow.onrender.com"
    }

    all_results = {}

    # Verificar cada servicio
    for service_name, base_url in services.items():
        print(f"📋 Verificando {service_name}")
        print("-" * 50)

        if service_name == "API REST":
            results = check_api_endpoints(base_url)
        elif service_name == "Streamlit Dashboard":
            success, status = check_streamlit_dashboard(base_url)
            results = [("/", success, status)]
        elif service_name == "MLflow UI":
            success, status = check_mlflow_ui(base_url)
            results = [("/", success, status)]

        all_results[service_name] = results
        print()

    # Resumen final
    print("=" * 70)
    print("📊 RESUMEN COMPLETO DEL DESPLIEGUE:")
    print("=" * 70)

    total_endpoints = 0
    successful_endpoints = 0

    for service_name, results in all_results.items():
        print(f"\n🔧 {service_name}:")
        service_success = 0
        service_total = len(results)

        for endpoint, success, status in results:
            total_endpoints += 1
            if success:
                successful_endpoints += 1
                service_success += 1
                print(f"   ✅ {endpoint}")
            else:
                print(f"   ❌ {endpoint} (Status: {status})")

        print(f"   📈 {service_success}/{service_total} endpoints funcionando")

    print("\n" + "=" * 70)
    print(f"🎯 RESULTADO GLOBAL: {successful_endpoints}/{total_endpoints} endpoints funcionando")

    # Evaluar éxito general
    success_rate = successful_endpoints / total_endpoints if total_endpoints > 0 else 0

    if success_rate == 1.0:
        print("🎉 ¡DESPLIEGUE 100% EXITOSO!")
        print("   🌟 Todas las aplicaciones están funcionando correctamente")
        return True
    elif success_rate >= 0.8:
        print("⚠️ DESPLIEGUE MAYORITARIAMENTE EXITOSO")
        print("   🔧 La mayoría funciona, pero hay algunos problemas menores")
        return False
    else:
        print("❌ DESPLIEGUE FALLIDO")
        print("   🚨 La mayoría de servicios no funcionan")
        return False

if __name__ == "__main__":
    print("⏳ Esperando 3 minutos para que Render termine el despliegue...")
    time.sleep(180)  # Esperar 3 minutos

    success = main()

    print("\n" + "=" * 70)
    if success:
        print("🎉 ¡FELICITACIONES! Todas tus aplicaciones están funcionando")
        print("   📚 API Docs: https://delfosa1c8-3.onrender.com/docs")
        print("   🏥 Health: https://delfosa1c8-3.onrender.com/health")
        print("   🔮 Dashboard: https://diabetes-streamlit.onrender.com")
        print("   📊 MLflow: https://diabetes-mlflow.onrender.com")
    else:
        print("⚠️ Hay problemas que necesitan atención")
        print("   📋 Revisa los logs en Render dashboard")
        print("   🔍 Verifica las variables de entorno")
        print("   🐛 Revisa la configuración de servicios")

    print("=" * 70)

    sys.exit(0 if success else 1)