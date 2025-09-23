#!/usr/bin/env python3
"""
Script para verificar y corregir variables de entorno en Render
"""
import os
import sys
from pathlib import Path

def check_render_environment():
    """Verifica variables de entorno críticas en Render"""
    print("🔍 VERIFICANDO VARIABLES DE ENTORNO EN RENDER")
    print("=" * 50)

    required_vars = {
        'ENVIRONMENT': 'production',
        'DEBUG': 'false',
        'LOG_LEVEL': 'INFO',
        'SECRET_KEY': 'diabetes-secret-key-2025-super-seguro',
        'JWT_SECRET_KEY': 'diabetes-jwt-secret-key-2025-super-seguro',
        'API_HOST': '0.0.0.0',
        'API_PORT': '8002',
        'STREAMLIT_SERVER_ADDRESS': '0.0.0.0',
        'STREAMLIT_SERVER_PORT': '8501',
        'STREAMLIT_SERVER_HEADLESS': 'true',
        'MLFLOW_TRACKING_URI': 'file:///app/outputs/mlruns',
        'MLFLOW_HOST': '0.0.0.0',
        'MLFLOW_PORT': '5002'
    }

    missing_vars = []
    incorrect_vars = []

    for var_name, expected_value in required_vars.items():
        actual_value = os.getenv(var_name)
        if actual_value is None:
            missing_vars.append(var_name)
        elif actual_value != expected_value:
            incorrect_vars.append((var_name, actual_value, expected_value))

    if missing_vars:
        print("❌ VARIABLES FALTANTES:")
        for var in missing_vars:
            print(f"   • {var}")
        print()

    if incorrect_vars:
        print("❌ VARIABLES CON VALORES INCORRECTOS:")
        for var, actual, expected in incorrect_vars:
            print(f"   • {var}: '{actual}' != '{expected}'")
        print()

    if not missing_vars and not incorrect_vars:
        print("✅ TODAS LAS VARIABLES DE ENTORNO ESTÁN CORRECTAS")
        return True

    print("📋 INSTRUCCIONES PARA CORREGIR:")
    print("   1. Ve a tu servicio en Render dashboard")
    print("   2. Haz clic en 'Environment' tab")
    print("   3. Agrega las siguientes variables:")
    print()

    for var_name, expected_value in required_vars.items():
        if var_name in missing_vars:
            print(f"      {var_name} = {expected_value}")

    print()
    print("   4. Haz clic en 'Save Changes'")
    print("   5. Espera 3-5 minutos para que se redeploye")
    print("   6. Ejecuta este script nuevamente")
    print()

    return False

def create_environment_file():
    """Crea archivo .env para desarrollo local"""
    env_file = Path('.env')
    if not env_file.exists():
        print("📄 Creando archivo .env para desarrollo local...")

        env_content = """# Environment Configuration
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=INFO

# Security
SECRET_KEY=diabetes-secret-key-2025-super-seguro
JWT_SECRET_KEY=diabetes-jwt-secret-key-2025-super-seguro

# API Configuration
API_HOST=0.0.0.0
API_PORT=8002

# Streamlit Configuration
STREAMLIT_SERVER_ADDRESS=0.0.0.0
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_HEADLESS=true

# MLflow Configuration
MLFLOW_TRACKING_URI=file:///app/outputs/mlruns
MLFLOW_HOST=0.0.0.0
MLFLOW_PORT=5002
"""

        env_file.write_text(env_content)
        print("✅ Archivo .env creado exitosamente")
    else:
        print("📄 Archivo .env ya existe")

if __name__ == "__main__":
    print("🚀 DIAGNÓSTICO DE VARIABLES DE ENTORNO")
    print("=" * 50)

    # Verificar variables de entorno
    env_ok = check_render_environment()

    if not env_ok:
        print("\n" + "=" * 50)
        create_environment_file()

        print("\n💡 RECOMENDACIONES:")
        print("   • Verifica que las variables estén en Environment tab")
        print("   • Asegúrate de que los valores sean exactamente iguales")
        print("   • Después de guardar, espera el redeploy automático")
        print("   • Revisa los logs en Render para más detalles")

    sys.exit(0 if env_ok else 1)