#!/usr/bin/env python3
"""
Script para configurar el servicio en Render
Proporciona instrucciones paso a paso para el deployment
"""

import webbrowser
import os
import sys

def print_header():
    print("🚀 CONFIGURACIÓN DEL SERVICIO EN RENDER")
    print("=" * 50)
    print("Sistema de Biomarcadores Digitales - Optimizado")
    print("=" * 50)

def print_configuration():
    print("\n📋 CONFIGURACIÓN REQUERIDA:")
    print("-" * 30)
    print("🌐 URL del servicio: https://delfos-biomarkers.onrender.com")
    print("🔧 Runtime: Docker")
    print("📦 Dockerfile: ./Dockerfile")
    print("🚀 Start Command: ./start_services.sh")
    print("💾 Puerto: 8000")

def print_environment_variables():
    print("\n🔐 VARIABLES DE ENTORNO:")
    print("-" * 30)
    env_vars = [
        ("PYTHON_VERSION", "3.12"),
        ("PORT", "8000"),
        ("RENDER", "true"),
        ("PYTHONUNBUFFERED", "1"),
        ("PYTHONDONTWRITEBYTECODE", "1")
    ]

    for key, value in env_vars:
        print(f"   {key}={value}")

def print_disk_configuration():
    print("\n💾 CONFIGURACIÓN DE DISCO PERSISTENTE:")
    print("-" * 40)
    print("   Mount Path: /app")
    print("   Size: 10 GB")

def print_verification_steps():
    print("\n🔍 VERIFICACIÓN DESPUÉS DEL DEPLOYMENT:")
    print("-" * 40)
    print("1. Esperar a que termine el build (5-10 minutos)")
    print("2. Verificar health check:")
    print("   curl https://delfos-biomarkers.onrender.com/health")
    print("3. Probar la aplicación:")
    print("   curl https://delfos-biomarkers.onrender.com/")
    print("4. Probar API de predicción:")
    print("   curl -X POST https://delfos-biomarkers.onrender.com/predict \\")
    print("        -H 'Content-Type: application/json' \\")
    print("        -d '{\"edad\": 45, \"sexo\": 1, \"imc\": 25.0}'")

def print_urls():
    print("\n🌐 URLS DESPUÉS DEL DEPLOYMENT:")
    print("-" * 35)
    urls = [
        ("Dashboard Principal", "https://delfos-biomarkers.onrender.com/"),
        ("API de Predicción", "https://delfos-biomarkers.onrender.com/predict"),
        ("Información del Sistema", "https://delfos-biomarkers.onrender.com/info"),
        ("Health Check", "https://delfos-biomarkers.onrender.com/health")
    ]

    for name, url in urls:
        print(f"   {name}: {url}")

def open_render_dashboard():
    print("\n🌐 Abriendo Render Dashboard...")
    try:
        webbrowser.open("https://dashboard.render.com")
        print("✅ Dashboard de Render abierto en tu navegador")
    except Exception as e:
        print(f"❌ Error abriendo el navegador: {e}")
        print("   Ve manualmente a: https://dashboard.render.com")

def main():
    print_header()
    print_configuration()
    print_environment_variables()
    print_disk_configuration()
    print_verification_steps()
    print_urls()

    print("\n" + "=" * 50)
    print("📝 INSTRUCCIONES PASO A PASO:")
    print("=" * 50)

    print("\n1️⃣  Ir al Dashboard de Render:")
    print("   🌐 https://dashboard.render.com")

    print("\n2️⃣  Crear nuevo servicio:")
    print("   • Click en 'New' > 'Blueprint'")
    print("   • Seleccionar 'Docker' como runtime")
    print("   • Conectar repositorio de GitHub")

    print("\n3️⃣  Configurar el servicio:")
    print("   • Nombre: delfos-biomarkers")
    print("   • Runtime: Docker")
    print("   • Dockerfile Path: ./Dockerfile")
    print("   • Build Command: (dejar vacío)")
    print("   • Start Command: ./start_services.sh")

    print("\n4️⃣  Configurar variables de entorno:")
    print("   • Copiar las variables listadas arriba")

    print("\n5️⃣  Configurar disco persistente:")
    print("   • Mount Path: /app")
    print("   • Size: 10 GB")

    print("\n6️⃣  Desplegar:")
    print("   • Click en 'Create Web Service'")
    print("   • Esperar el build (5-10 minutos)")

    print("\n7️⃣  Verificar funcionamiento:")
    print("   • Usar los comandos de verificación arriba")

    # Abrir el dashboard automáticamente
    print("\n🌐 Abriendo el Dashboard de Render automáticamente...")
    open_render_dashboard()

    print("\n✅ ¡Configuración lista!")
    print("🎉 El servicio está optimizado y listo para desplegar en Render.")

if __name__ == "__main__":
    main()