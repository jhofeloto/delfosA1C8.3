#!/usr/bin/env python3
"""
Script para configurar las variables de entorno críticas en Railway
"""
import subprocess
import sys
import os
from pathlib import Path

def set_railway_variables():
    """Configurar variables de entorno en Railway"""
    print("🔧 Configurando variables de entorno en Railway...")

    # Variables críticas para ambos ambientes
    variables = {
        'ENVIRONMENT': 'test',
        'DEBUG': 'true',
        'LOG_LEVEL': 'INFO',
        'API_HOST': '0.0.0.0',
        'API_PORT': '8002',
        'API_WORKERS': '1',
        'STREAMLIT_SERVER_ADDRESS': '0.0.0.0',
        'STREAMLIT_SERVER_PORT': '8501',
        'STREAMLIT_SERVER_HEADLESS': 'true',
        'MLFLOW_TRACKING_URI': 'file:///app/outputs/mlruns',
        'MLFLOW_HOST': '0.0.0.0',
        'MLFLOW_PORT': '5002',
        'SECRET_KEY': 'test-secret-key-12345',
        'JWT_SECRET_KEY': 'test-jwt-secret-12345'
    }

    success_count = 0
    error_count = 0

    for var, value in variables.items():
        try:
            # Configurar en ambiente test
            result = subprocess.run([
                'railway', 'variables',
                '--set', f"{var}={value}",
                '--environment', 'production'
            ], capture_output=True, text=True)

            if result.returncode == 0:
                print(f"   ✅ {var}: {value}")
                success_count += 1
            else:
                print(f"   ❌ Error configurando {var}: {result.stderr}")
                error_count += 1

        except Exception as e:
            print(f"   ❌ Error configurando {var}: {e}")
            error_count += 1

    return success_count, error_count

def verify_configuration():
    """Verificar que las variables se configuraron correctamente"""
    print("\n🔍 Verificando configuración...")

    # Verificar variables críticas
    critical_vars = [
        'ENVIRONMENT', 'DEBUG', 'LOG_LEVEL', 'API_HOST', 'API_PORT',
        'STREAMLIT_SERVER_ADDRESS', 'STREAMLIT_SERVER_PORT',
        'MLFLOW_TRACKING_URI', 'SECRET_KEY'
    ]

    missing_vars = []

    for var in critical_vars:
        value = os.getenv(var)
        if value is None:
            missing_vars.append(var)
        else:
            print(f"   ✅ {var}: {value}")

    if missing_vars:
        print(f"\n⚠️ Variables aún faltantes: {', '.join(missing_vars)}")
        return False
    else:
        print("\n✅ Todas las variables críticas configuradas")
        return True

def main():
    """Función principal"""
    print("="*60)
    print("🔧 CONFIGURACIÓN DE VARIABLES DE ENTORNO EN RAILWAY")
    print("="*60)

    # Verificar que railway CLI esté disponible
    try:
        result = subprocess.run(['railway', '--version'],
                              capture_output=True, text=True)
        if result.returncode != 0:
            print("❌ Railway CLI no disponible")
            print("   Instala Railway CLI: curl -fsSL https://railway.app/install.sh | sh")
            return 1
        print(f"✅ Railway CLI disponible: {result.stdout.strip()}")
    except Exception as e:
        print(f"❌ Error con Railway CLI: {e}")
        return 1

    # Configurar variables
    success_count, error_count = set_railway_variables()

    print("\n📊 RESUMEN:")
    print(f"   ✅ Variables configuradas: {success_count}")
    print(f"   ❌ Errores: {error_count}")

    if error_count == 0:
        print("\n🎉 ¡Configuración completada exitosamente!")
        print("\n🚀 Próximos pasos:")
        print("1. Ejecutar: railway up")
        print("2. Verificar logs: railway logs")
        print("3. Probar API: curl https://tu-app.up.railway.app/health")
        return 0
    else:
        print(f"\n⚠️ {error_count} variables no se pudieron configurar")
        print("   Revisa tu conexión a Railway y permisos del proyecto")
        return 1

if __name__ == "__main__":
    sys.exit(main())