#!/usr/bin/env python3
"""
Script final para verificar el despliegue en Render después de los cambios
"""
import requests
import time
import sys
from datetime import datetime

def check_service_status():
    """Verificar el estado completo del servicio"""
    print("🚀 VERIFICACIÓN FINAL DEL DESPLIEGUE EN RENDER")
    print("=" * 60)
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC")
    print()

    base_url = "https://delfosa1c8-3.onrender.com"

    # Lista de endpoints a verificar
    endpoints = [
        ("/health", "Health Check", "GET"),
        ("/docs", "Documentación API", "GET"),
        ("/model/info", "Información del Modelo", "GET"),
        ("/models", "Modelos Disponibles", "GET"),
        ("/categories", "Categorías", "GET"),
        ("/features", "Características", "GET")
    ]

    results = []

    for endpoint, description, method in endpoints:
        try:
            print(f"🔍 Verificando {description}...")
            print(f"   URL: {base_url}{endpoint}")

            if method == "GET":
                response = requests.get(f"{base_url}{endpoint}", timeout=30)
                status_code = response.status_code

                if status_code == 200:
                    print("   ✅ Éxito")
                    if endpoint == "/health":
                        health_data = response.json()
                        print(f"   📊 Estado: {health_data.get('status', 'N/A')}")
                        print(f"   🤖 Modelo cargado: {health_data.get('model_loaded', False)}")
                        print(f"   📈 Predicciones: {health_data.get('total_predictions', 0)}")
                    elif endpoint == "/model/info":
                        model_data = response.json()
                        print(f"   📊 Modelo: {model_data.get('model_name', 'N/A')}")
                        print(f"   📈 R² Score: {model_data.get('r2_score', 'N/A')}")
                        print(f"   🔢 Características: {model_data.get('n_features', 'N/A')}")
                else:
                    print(f"   ❌ Error HTTP {status_code}")

                results.append((endpoint, status_code == 200, status_code))

            else:
                print(f"   ⚠️ Método {method} no implementado")
                results.append((endpoint, False, 0))

        except requests.exceptions.Timeout:
            print("   ⏰ Timeout (30s)")
            results.append((endpoint, False, "TIMEOUT"))
        except requests.exceptions.ConnectionError:
            print("   🌐 Error de conexión")
            results.append((endpoint, False, "CONNECTION_ERROR"))
        except Exception as e:
            print(f"   ❌ Error: {e}")
            results.append((endpoint, False, "ERROR"))

        print()

    # Resumen final
    print("=" * 60)
    print("📊 RESUMEN FINAL:")
    print("=" * 60)

    successful = 0
    total = len(results)

    for endpoint, success, status in results:
        if success:
            successful += 1
            print(f"   ✅ {endpoint}")
        else:
            print(f"   ❌ {endpoint} (Status: {status})")

    print()
    print(f"🎯 RESULTADO: {successful}/{total} endpoints funcionando")

    if successful == total:
        print("🎉 ¡DESPLIEGUE COMPLETAMENTE EXITOSO!")
        print("   🌟 Tu API está funcionando perfectamente")
        return True
    elif successful >= total * 0.7:  # 70% éxito
        print("⚠️ DESPLIEGUE PARCIALMENTE EXITOSO")
        print("   🔧 Algunos endpoints funcionan, pero hay problemas menores")
        return False
    else:
        print("❌ DESPLIEGUE FALLIDO")
        print("   🚨 La mayoría de endpoints no funcionan")
        return False

def main():
    """Función principal"""
    print("⏳ Esperando 2 minutos para que Render termine el despliegue...")
    time.sleep(120)  # Esperar 2 minutos

    success = check_service_status()

    print("\n" + "=" * 60)
    if success:
        print("🎉 ¡FELICITACIONES! Tu API está funcionando correctamente")
        print("   📚 Documentación: https://delfosa1c8-3.onrender.com/docs")
        print("   🏥 Health Check: https://delfosa1c8-3.onrender.com/health")
        print("   🔮 Predicciones: https://delfosa1c8-3.onrender.com/predict")
    else:
        print("⚠️ Hay algunos problemas que necesitan atención")
        print("   📋 Revisa los logs en Render dashboard")
        print("   🔍 Verifica las variables de entorno")
        print("   🐛 Revisa la configuración del servicio")

    print("=" * 60)

    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)