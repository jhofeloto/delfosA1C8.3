#!/usr/bin/env python3
"""
Script para completar el despliegue en Render desde la CLI
Proporciona comandos específicos para cada paso
"""
import os
import subprocess
import sys
from pathlib import Path

def show_current_status():
    """Mostrar estado actual"""
    print("📊 ESTADO ACTUAL DEL DESPLIEGUE:")
    print("="*50)
    print("✅ PASO 1: Crear cuenta en Render - COMPLETADO")
    print("✅ PASO 2: Conectar repositorio - COMPLETADO")
    print("🔄 PASO 3: Configurar servicio - EN PROCESO")
    print("⏳ PASO 4: Desplegar - PENDIENTE")

def show_exact_commands():
    """Mostrar comandos exactos para Render"""
    print("\n🖥️ COMANDOS EXACTOS PARA RENDER:")
    print("="*50)

    print("\n1️⃣ EN RENDER DASHBOARD:")
    print("   • Ve a: https://dashboard.render.com")
    print("   • Busca tu repositorio conectado")
    print("   • Haz clic en 'Connect' si no está conectado")

    print("\n2️⃣ CREAR SERVICIO WEB:")
    print("   • En tu repositorio → 'Create Web Service'")
    print("   • Configura EXACTAMENTE así:")

    print("\n   📝 NOMBRE DEL SERVICIO:")
    print("   diabetes-api")

    print("\n   ⚙️ CONFIGURACIÓN:")
    print("   • Runtime: Python 3")
    print("   • Build Command: pip install -r requirements.txt")
    print("   • Start Command: python api.py --host 0.0.0.0 --port $PORT")

    print("\n   🌍 VARIABLES DE ENTORNO (copia y pega):")
    env_vars = {
        "ENVIRONMENT": "production",
        "DEBUG": "false",
        "LOG_LEVEL": "INFO",
        "SECRET_KEY": "diabetes-secret-key-2025-super-seguro",
        "JWT_SECRET_KEY": "diabetes-jwt-secret-key-2025-super-seguro",
        "API_HOST": "0.0.0.0",
        "API_PORT": "8002",
        "STREAMLIT_SERVER_ADDRESS": "0.0.0.0",
        "STREAMLIT_SERVER_PORT": "8501",
        "STREAMLIT_SERVER_HEADLESS": "true",
        "MLFLOW_TRACKING_URI": "file:///app/outputs/mlruns",
        "MLFLOW_HOST": "0.0.0.0",
        "MLFLOW_PORT": "5002"
    }

    for key, value in env_vars.items():
        print(f"   {key}={value}")

    print("\n   💾 BASE DE DATOS:")
    print("   • Selecciona 'Create PostgreSQL database'")
    print("   • Nombre: diabetes-db")

    print("\n3️⃣ DESPLEGAR:")
    print("   • Haz clic en 'Create Web Service'")
    print("   • Espera 3-5 minutos")
    print("   • ¡Tu API estará lista!")

def create_service_yaml():
    """Crear archivo de configuración para Render"""
    print("\n📄 Creando configuración automática...")

    service_config = {
        "services": [
            {
                "type": "web",
                "name": "diabetes-api",
                "runtime": "python3",
                "buildCommand": "pip install -r requirements.txt",
                "startCommand": "python api.py --host 0.0.0.0 --port $PORT",
                "envVars": [
                    {"key": "ENVIRONMENT", "value": "production"},
                    {"key": "DEBUG", "value": "false"},
                    {"key": "LOG_LEVEL", "value": "INFO"},
                    {"key": "SECRET_KEY", "value": "diabetes-secret-key-2025-super-seguro"},
                    {"key": "JWT_SECRET_KEY", "value": "diabetes-jwt-secret-key-2025-super-seguro"},
                    {"key": "API_HOST", "value": "0.0.0.0"},
                    {"key": "API_PORT", "value": "8002"},
                    {"key": "STREAMLIT_SERVER_ADDRESS", "value": "0.0.0.0"},
                    {"key": "STREAMLIT_SERVER_PORT", "value": "8501"},
                    {"key": "STREAMLIT_SERVER_HEADLESS", "value": "true"},
                    {"key": "MLFLOW_TRACKING_URI", "value": "file:///app/outputs/mlruns"},
                    {"key": "MLFLOW_HOST", "value": "0.0.0.0"},
                    {"key": "MLFLOW_PORT", "value": "5002"}
                ]
            },
            {
                "type": "pserv",
                "name": "diabetes-db",
                "envVars": [
                    {
                        "key": "DATABASE_URL",
                        "fromService": {
                            "type": "pserv",
                            "name": "diabetes-db",
                            "property": "connectionString"
                        }
                    }
                ]
            }
        ]
    }

    import json
    with open('render-service.json', 'w') as f:
        json.dump(service_config, f, indent=2)

    print("   ✅ render-service.json creado")

def show_verification_commands():
    """Mostrar comandos para verificar el despliegue"""
    print("\n🔍 COMANDOS DE VERIFICACIÓN:")
    print("="*50)

    print("\nDespués del despliegue, ejecuta:")
    print("   curl https://diabetes-api.onrender.com/health")
    print("   curl https://diabetes-api.onrender.com/docs")
    print("   curl -X POST https://diabetes-api.onrender.com/predict \\")
    print("     -H 'Content-Type: application/json' \\")
    print("     -d '{\"edad\": 45, \"sexo\": \"M\", \"imc\": 25.5, \"tas\": 120, \"tad\": 80, \"perimetro_abdominal\": 90, \"realiza_ejercicio\": \"Si\", \"fuma\": \"No\", \"historia_familiar_dm\": \"No\"}'")

def show_troubleshooting():
    """Mostrar guía de solución de problemas"""
    print("\n🔧 SOLUCIÓN DE PROBLEMAS:")
    print("="*50)

    print("\nSi hay errores:")
    print("   1. Verifica que requirements.txt esté correcto")
    print("   2. Asegúrate de que Procfile esté presente")
    print("   3. Revisa los logs en Render Dashboard")
    print("   4. Verifica que el puerto sea $PORT")
    print("   5. Confirma que el host sea 0.0.0.0")

    print("\nComandos útiles:")
    print("   # Ver logs en tiempo real (después del despliegue)")
    print("   curl -s https://diabetes-api.onrender.com/health")
    print("   ")
    print("   # Ver documentación")
    print("   curl -s https://diabetes-api.onrender.com/docs")

def main():
    """Función principal"""
    print("🚀 COMPLETAR DESPLIEGUE EN RENDER - PASO 3 y 4")
    print("="*60)

    # Mostrar estado actual
    show_current_status()

    # Mostrar comandos exactos
    show_exact_commands()

    # Crear configuración
    create_service_yaml()

    # Mostrar verificación
    show_verification_commands()

    # Mostrar troubleshooting
    show_troubleshooting()

    print("
🎯 RESUMEN:"    print("✅ Repositorio conectado")
    print("📋 Configuración lista")
    print("⏱️ Tiempo restante: 5 minutos")
    print("🌍 URL final: https://diabetes-api.onrender.com"
    print("
💡 Sigue las instrucciones arriba EXACTAMENTE como están escritas!"
    print("🔄 Render configurará automáticamente:")
    print("   • Variables de entorno")
    print("   • Base de datos PostgreSQL")
    print("   • SSL automático")
    print("   • Dominio personalizado")

    return 0

if __name__ == "__main__":
    sys.exit(main())