#!/usr/bin/env python3
"""
VERIFICACIÓN DE VARIABLES DE ENTORNO EN RENDER
"""

import os
import sys

def check_environment_variables():
    """Verificar que todas las variables de entorno estén configuradas"""
    print("🔍 VERIFICANDO VARIABLES DE ENTORNO EN RENDER")
    print("="*50)

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

    all_good = True
    missing_vars = []

    for var, expected_value in required_vars.items():
        actual_value = os.getenv(var)

        if actual_value is None:
            print(f"❌ {var}: FALTANTE")
            all_good = False
            missing_vars.append(var)
        elif actual_value == expected_value:
            print(f"✅ {var}: {actual_value}")
        else:
            print(f"⚠️ {var}: {actual_value} (esperado: {expected_value})")
            all_good = False

    print("\n" + "="*50)
    if all_good:
        print("🎉 ¡TODAS LAS VARIABLES ESTÁN CONFIGURADAS!")
        print("\n📋 PRÓXIMOS PASOS:")
        print("   1. Ve a Render dashboard")
        print("   2. Haz clic en 'Save Changes'")
        print("   3. Espera 3-5 minutos")
        print("   4. Ejecuta: python scripts/verify_correct_prediction.py")
    else:
        print(f"❌ FALTAN {len(missing_vars)} VARIABLES:")
        for var in missing_vars:
            print(f"   • {var}")
        print("\n📋 INSTRUÇÕES:")
        print("   1. Ve a Environment tab en Render")
        print("   2. Agrega las variables faltantes")
        print("   3. Haz clic en 'Save Changes'")
        print("   4. Ejecuta este script nuevamente")

    return all_good

def main():
    """Función principal"""
    success = check_environment_variables()
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)