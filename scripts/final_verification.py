#!/usr/bin/env python3
"""
Verificación final completa del despliegue con tiempo adicional para MLflow
"""
import requests
import time
import sys
from datetime import datetime

def check_service(name, url, health_path="/", expected_status=200, timeout=60):
    """Verificar un servicio individual con timeout extendido"""
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
    """Verificar endpoints de la API"""
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
    """Verificar MLflow UI con múltiples intentos"""
    print("🔄 Verificando MLflow UI (puede tardar más en inicializar)...")

    # Intentar múltiples endpoints
    endpoints_to_try = [
        "/",
        "/static/css/main.css",
        "/api/2.0/mlflow/experiments/list"
    ]

    for endpoint in endpoints_to_try:
        success, status = check_service("MLflow UI", base_url, endpoint, 200, 90)
        if success:
            print(f"   ✅ MLflow accesible vía {endpoint}")
            return True, status

    return False, "ALL_ENDPOINTS_FAILED"

def main():
    """Función principal"""
    print("🚀 VERIFICACIÓN FINAL COMPLETA DEL DESPLIEGUE")
    print("=" * 60)
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC")
    print()

    # URLs de los servicios
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
    print("=" * 60)
    print("📊 RESUMEN FINAL DEL DESPLIEGUE:")
    print("=" * 60)

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

    print("\n" + "=" * 60)
    print(f"🎯 RESULTADO GLOBAL: {successful_endpoints}/{total_endpoints} endpoints funcionando")

    # Evaluar éxito general
    success_rate = successful_endpoints / total_endpoints if total_endpoints > 0 else 0

    if success_rate == 1.0:
        print("🎉 ¡DESPLIEGUE 100% EXITOSO!")
        print("   🌟 Todas las aplicaciones están funcionando correctamente")
        return True
    elif success_rate >= 0.8:
        print("⚠️ DESPLIEGUE MAYORITARIAMENTE EXITOSO")
        print("   🔧 La mayoría funciona, pero hay problemas menores")
        return False
    else:
        print("❌ DESPLIEGUE FALLIDO")
        print("   🚨 La mayoría de servicios no funcionan")
        return False

if __name__ == "__main__":
    print("⏳ Esperando 5 minutos para que todos los servicios terminen de inicializar...")
    print("   (MLflow puede tardar más tiempo en Render)")
    time.sleep(300)  # Esperar 5 minutos

    success = main()

    print("\n" + "=" * 60)
    if success:
        print("🎉 ¡FELICITACIONES! Tu Sistema Predictivo de Diabetes está completamente funcional")
        print("   📚 API Docs: https://delfosa1c8-3.onrender.com/docs")
        print("   🏥 Health: https://delfosa1c8-3.onrender.com/health")
        print("   🔮 Dashboard: https://diabetes-streamlit.onrender.com")
        print("   📊 MLflow: https://diabetes-mlflow.onrender.com")
        print("   🗄️ Database: PostgreSQL configurado")
    else:
        print("⚠️ Hay algunos problemas que necesitan atención")
        print("   📋 Revisa los logs en Render dashboard")
        print("   🔍 Ejecuta: python scripts/diagnose_mlflow.py")
        print("   🐛 Verifica la configuración de servicios")

    print("=" * 60)

    sys.exit(0 if success else 1)