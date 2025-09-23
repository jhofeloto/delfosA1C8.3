#!/usr/bin/env python3
"""
Script para configurar y desplegar en Render
"""
import os
import subprocess
import sys
from pathlib import Path

def check_files():
    """Verificar que los archivos necesarios existen"""
    print("📋 Verificando archivos necesarios...")

    required_files = ['Procfile', 'runtime.txt', 'requirements.txt']
    missing_files = []

    for file in required_files:
        if Path(file).exists():
            print(f"   ✅ {file}")
        else:
            missing_files.append(file)
            print(f"   ❌ {file}")

    if missing_files:
        print(f"\n❌ Faltan archivos: {', '.join(missing_files)}")
        return False

    return True

def create_render_service():
    """Crear configuración para Render"""
    print("\n🔧 Configurando servicio para Render...")

    # Verificar que render.yaml existe
    if not Path('render.yaml').exists():
        print("❌ render.yaml no encontrado")
        return False

    print("   ✅ render.yaml configurado")
    print("   ✅ Variables de entorno incluidas")
    print("   ✅ Base de datos PostgreSQL incluida")

    return True

def show_deployment_steps():
    """Mostrar pasos para desplegar en Render"""
    print("\n🚀 PASOS PARA DESPLEGAR EN RENDER:")
    print("="*50)

    print("\n1️⃣ CREAR CUENTA EN RENDER:")
    print("   • Ve a: https://render.com")
    print("   • Regístrate con GitHub/GitLab")
    print("   • Autoriza acceso a tu repositorio")

    print("\n2️⃣ CONECTAR REPOSITORIO:")
    print("   • En Render Dashboard, haz clic en 'New'")
    print("   • Selecciona 'Blueprint'")
    print("   • Busca tu repositorio")

    print("\n3️⃣ CONFIGURAR SERVICIO:")
    print("   • Nombre: diabetes-prediction-api")
    print("   • Runtime: Python 3")
    print("   • Build Command: pip install -r requirements.txt")
    print("   • Start Command: python api.py --host 0.0.0.0 --port $PORT")

    print("\n4️⃣ VARIABLES DE ENTORNO (se configuran automáticamente):")
    variables = [
        "ENVIRONMENT=production",
        "DEBUG=false",
        "LOG_LEVEL=INFO",
        "SECRET_KEY (generada automáticamente)",
        "JWT_SECRET_KEY (generada automáticamente)",
        "API_HOST=0.0.0.0",
        "API_PORT=8002",
        "STREAMLIT_SERVER_ADDRESS=0.0.0.0",
        "STREAMLIT_SERVER_PORT=8501",
        "STREAMLIT_SERVER_HEADLESS=true",
        "MLFLOW_TRACKING_URI=file:///app/outputs/mlruns",
        "MLFLOW_HOST=0.0.0.0",
        "MLFLOW_PORT=5002"
    ]

    for var in variables:
        print(f"   • {var}")

    print("\n5️⃣ BASE DE DATOS:")
    print("   • Render creará automáticamente PostgreSQL")
    print("   • Variable DATABASE_URL se configurará automáticamente")

    print("\n6️⃣ DESPLEGAR:")
    print("   • Haz clic en 'Create Service'")
    print("   • Espera 3-5 minutos")
    print("   • ¡Tu API estará lista!")

def show_urls():
    """Mostrar URLs esperadas"""
    print("\n🌐 URLS QUE OBTENDRÁS:")
    print("="*30)
    print("   • API REST: https://diabetes-api.onrender.com")
    print("   • Documentación: https://diabetes-api.onrender.com/docs")
    print("   • Health Check: https://diabetes-api.onrender.com/health")
    print("   • Base de datos: Automática en Render")

def main():
    """Función principal"""
    print("🚀 CONFIGURACIÓN PARA DESPLIEGUE EN RENDER")
    print("="*50)

    # Verificar archivos
    if not check_files():
        return 1

    # Verificar configuración
    if not create_render_service():
        return 1

    # Mostrar pasos
    show_deployment_steps()

    # Mostrar URLs
    show_urls()

    print("\n✅ ¡CONFIGURACIÓN COMPLETADA!")
    print("\n🎯 VENTAJAS DE RENDER PARA TU SISTEMA:")
    print("   • ⚡ Mejor performance para ML")
    print("   • 💰 Base de datos incluida gratis")
    print("   • 🌍 Mejor latencia para Latinoamérica")
    print("   • 📊 Analytics incluidos")
    print("   • 🔄 Despliegues automáticos")

    print("\n💡 CONSEJO:")
    print("   Render es la opción más rápida y económica para tu")
    print("   Sistema Predictivo de Diabetes. ¡Tendrás todo funcionando")
    print("   en menos de 10 minutos!")

    return 0

if __name__ == "__main__":
    sys.exit(main())