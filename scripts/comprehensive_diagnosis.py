#!/usr/bin/env python3
"""
Diagnóstico completo del Sistema Predictivo de Diabetes
"""
import requests
import time
import sys
from datetime import datetime
import subprocess
import os

def check_local_api():
    """Verificar API localmente"""
    print("🔍 Verificando API localmente...")
    try:
        response = requests.get('http://localhost:8002/health', timeout=10)
        if response.status_code == 200:
            print("   ✅ API local funcionando")
            return True
        else:
            print(f"   ❌ API local error: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ API local no disponible: {e}")
        return False

def check_local_mlflow():
    """Verificar MLflow localmente"""
    print("🔍 Verificando MLflow localmente...")
    try:
        # Verificar si el directorio existe
        mlruns_dir = "outputs/mlruns"
        if not os.path.exists(mlruns_dir):
            print(f"   📁 Creando directorio: {mlruns_dir}")
            os.makedirs(mlruns_dir, exist_ok=True)

        # Verificar si podemos importar MLflow
        try:
            import mlflow
            print("   ✅ MLflow importado correctamente")
        except ImportError as e:
            print(f"   ❌ Error importando MLflow: {e}")
            return False

        # Configurar MLflow con URI relativa
        try:
            mlflow.set_tracking_uri("./outputs/mlruns")
            experiment = mlflow.get_experiment_by_name("diabetes_prediction")
            if experiment is None:
                experiment_id = mlflow.create_experiment("diabetes_prediction")
                print("   ✅ Experimento creado: diabetes_prediction")
            else:
                print(f"   ✅ Experimento existe: {experiment.name}")
            return True
        except Exception as e:
            print(f"   ❌ Error con experimentos: {e}")
            return False

    except Exception as e:
        print(f"   ❌ Error general: {e}")
        return False

def check_render_services():
    """Verificar servicios en Render"""
    print("\n🔍 Verificando servicios en Render...")
    services = {
        "API REST": "https://delfosa1c8-3.onrender.com",
        "Streamlit Dashboard": "https://diabetes-streamlit.onrender.com",
        "MLflow UI": "https://diabetes-mlflow.onrender.com"
    }

    results = {}

    for name, url in services.items():
        print(f"\n📋 Verificando {name}")
        print("-" * 30)

        try:
            # Probar múltiples endpoints
            endpoints = ["/health", "/"] if name == "API REST" else ["/"]

            service_ok = False
            for endpoint in endpoints:
                try:
                    print(f"   Probando: {url}{endpoint}")
                    response = requests.get(f"{url}{endpoint}", timeout=30)

                    if response.status_code == 200:
                        print(f"   ✅ {endpoint} - Status: {response.status_code}")
                        service_ok = True
                        break
                    else:
                        print(f"   ⚠️ {endpoint} - Status: {response.status_code}")

                except requests.exceptions.Timeout:
                    print(f"   ⏰ {endpoint} - Timeout (30s)")
                except requests.exceptions.ConnectionError:
                    print(f"   🌐 {endpoint} - Error de conexión")
                except Exception as e:
                    print(f"   ❌ {endpoint} - Error: {e}")

            results[name] = service_ok

        except Exception as e:
            print(f"   ❌ Error general: {e}")
            results[name] = False

    return results

def suggest_fixes(results):
    """Sugerir correcciones basadas en resultados"""
    print("\n🔧 RECOMENDACIONES DE CORRECCIÓN:")
    print("=" * 50)

    issues = []

    if not results.get("API REST", False):
        issues.append("""
        ❌ API REST no funciona:
           - Verificar logs en Render dashboard
           - Confirmar que el puerto 8002 esté disponible
           - Revisar variables de entorno SECRET_KEY y JWT_SECRET_KEY
           - Verificar que api.py no tenga errores de importación""")

    if not results.get("Streamlit Dashboard", False):
        issues.append("""
        ❌ Streamlit Dashboard no funciona:
           - Verificar que web_app.py no tenga errores
           - Confirmar que todas las dependencias estén instaladas
           - Revisar configuración de puerto en Render""")

    if not results.get("MLflow UI", False):
        issues.append("""
        ❌ MLflow UI no funciona:
           - Verificar que la URI './outputs/mlruns' sea correcta
           - Confirmar que el directorio outputs/mlruns se cree correctamente
           - Revisar logs de MLflow en Render dashboard
           - Verificar que el timeout de 90s sea suficiente""")

    if not issues:
        print("✅ Todos los servicios parecen estar funcionando correctamente")
    else:
        for issue in issues:
            print(issue)

def main():
    """Función principal"""
    print("🔬 DIAGNÓSTICO COMPLETO DEL SISTEMA PREDICTIVO DE DIABETES")
    print("=" * 70)
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC")
    print()

    # Verificar servicios locales
    print("📍 1. VERIFICACIÓN LOCAL:")
    print("-" * 30)

    local_api_ok = check_local_api()
    local_mlflow_ok = check_local_mlflow()

    # Verificar servicios en Render
    print("\n📍 2. VERIFICACIÓN EN RENDER:")
    print("-" * 30)

    render_results = check_render_services()

    # Mostrar resumen
    print("\n📊 RESUMEN DE RESULTADOS:")
    print("=" * 30)

    print("\n📍 Servicios Locales:")
    print(f"   API REST: {'✅' if local_api_ok else '❌'}")
    print(f"   MLflow: {'✅' if local_mlflow_ok else '❌'}")

    print("\n🌐 Servicios en Render:")
    for service, status in render_results.items():
        print(f"   {service}: {'✅' if status else '❌'}")

    # Sugerir correcciones
    suggest_fixes(render_results)

    # Evaluar estado general
    all_ok = all(render_results.values()) and local_api_ok and local_mlflow_ok

    print(f"\n🎯 ESTADO GENERAL: {'✅ TODO FUNCIONA' if all_ok else '⚠️ HAY PROBLEMAS'}")

    return all_ok

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)