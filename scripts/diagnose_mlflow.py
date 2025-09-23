#!/usr/bin/env python3
"""
Script específico para diagnosticar y solucionar problemas con MLflow en Render
"""
import requests
import time
import sys
from datetime import datetime
import subprocess
import os

def check_mlflow_locally():
    """Verificar si MLflow funciona localmente"""
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

        # Configurar MLflow
        mlflow.set_tracking_uri(f"file://{mlruns_dir}")

        # Verificar experimentos
        try:
            experiment = mlflow.get_experiment_by_name("diabetes_prediction")
            if experiment is None:
                experiment_id = mlflow.create_experiment("diabetes_prediction")
                print(f"   ✅ Experimento creado: diabetes_prediction")
            else:
                print(f"   ✅ Experimento existe: {experiment.name}")
        except Exception as e:
            print(f"   ❌ Error con experimentos: {e}")
            return False

        return True

    except Exception as e:
        print(f"   ❌ Error general: {e}")
        return False

def check_mlflow_service(url, timeout=60):
    """Verificar servicio MLflow en Render"""
    print(f"🔍 Verificando MLflow en: {url}")

    endpoints = [
        "/",
        "/static/css/main.css",
        "/api/2.0/mlflow/experiments/list"
    ]

    for endpoint in endpoints:
        try:
            print(f"   Probando: {endpoint}")
            response = requests.get(f"{url}{endpoint}", timeout=timeout)

            if response.status_code == 200:
                print(f"   ✅ {endpoint} - Status: {response.status_code}")
                return True
            else:
                print(f"   ⚠️ {endpoint} - Status: {response.status_code}")

        except requests.exceptions.Timeout:
            print(f"   ⏰ {endpoint} - Timeout ({timeout}s)")
        except requests.exceptions.ConnectionError:
            print(f"   🌐 {endpoint} - Error de conexión")
        except Exception as e:
            print(f"   ❌ {endpoint} - Error: {e}")

    return False

def suggest_mlflow_fixes():
    """Sugerir correcciones para MLflow"""
    print("\n🔧 SUGERENCIAS PARA CORREGIR MLFLOW:")
    print("-" * 50)

    suggestions = [
        "1. Verificar que el directorio /app/outputs/mlruns existe",
        "2. Asegurar que MLflow tenga permisos de escritura",
        "3. Verificar que el puerto esté disponible",
        "4. Confirmar que todas las dependencias estén instaladas",
        "5. Revisar los logs en Render dashboard",
        "6. Considerar usar un health check más específico",
        "7. Verificar variables de entorno MLFLOW_*"
    ]

    for suggestion in suggestions:
        print(f"   {suggestion}")

def main():
    """Función principal"""
    print("🔬 DIAGNÓSTICO ESPECÍFICO DE MLFLOW")
    print("=" * 50)
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC")
    print()

    # Verificar localmente primero
    print("📍 1. VERIFICACIÓN LOCAL:")
    print("-" * 30)
    local_ok = check_mlflow_locally()

    if not local_ok:
        print("❌ MLflow tiene problemas locales")
        suggest_mlflow_fixes()
        return False

    print()
    print("📍 2. VERIFICACIÓN EN RENDER:")
    print("-" * 30)

    # URL de MLflow en Render
    mlflow_url = "https://diabetes-mlflow.onrender.com"

    # Esperar un poco más para que MLflow termine de inicializar
    print("⏳ Esperando 2 minutos adicionales para inicialización de MLflow...")
    time.sleep(120)

    # Verificar servicio
    service_ok = check_mlflow_service(mlflow_url)

    print()
    print("📊 RESULTADO DEL DIAGNÓSTICO:")
    print("=" * 30)

    if service_ok:
        print("✅ MLflow está funcionando correctamente")
        print(f"   🌐 URL: {mlflow_url}")
        print("   📊 Experimentos: https://diabetes-mlflow.onrender.com/#/experiments")
        return True
    else:
        print("❌ MLflow tiene problemas en Render")
        suggest_mlflow_fixes()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)