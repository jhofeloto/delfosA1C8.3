#!/usr/bin/env python3
"""
Script para automatizar el despliegue en Render
"""
import os
import subprocess
import sys
import webbrowser
from pathlib import Path

def check_requirements():
    """Verificar que todo esté listo"""
    print("📋 Verificando requisitos...")

    required_files = ['Procfile', 'runtime.txt', 'requirements.txt', 'render.yaml']
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

def create_deploy_script():
    """Crear script de despliegue"""
    print("\n📝 Creando script de despliegue...")

    script_content = '''#!/bin/bash
echo "🚀 DESPLIEGUE AUTOMÁTICO EN RENDER"
echo "="*50

# Verificar archivos
echo "📋 Verificando archivos..."
for file in Procfile runtime.txt requirements.txt render.yaml; do
    if [ -f "$file" ]; then
        echo "   ✅ $file"
    else
        echo "   ❌ $file no encontrado"
        exit 1
    fi
done

echo ""
echo "🌐 URLs esperadas:"
echo "   • API: https://diabetes-api.onrender.com"
echo "   • Docs: https://diabetes-api.onrender.com/docs"
echo "   • Health: https://diabetes-api.onrender.com/health"
echo ""
echo "📊 Variables de entorno automáticas:"
echo "   • ENVIRONMENT=production"
echo "   • DEBUG=false"
echo "   • LOG_LEVEL=INFO"
echo "   • SECRET_KEY (generada)"
echo "   • JWT_SECRET_KEY (generada)"
echo "   • API_HOST=0.0.0.0"
echo "   • API_PORT=8002"
echo "   • STREAMLIT_SERVER_ADDRESS=0.0.0.0"
echo "   • STREAMLIT_SERVER_PORT=8501"
echo "   • STREAMLIT_SERVER_HEADLESS=true"
echo "   • MLFLOW_TRACKING_URI=file:///app/outputs/mlruns"
echo "   • MLFLOW_HOST=0.0.0.0"
echo "   • MLFLOW_PORT=5002"
echo ""
echo "💡 INSTRUCCIONES:"
echo "1. Ve a: https://render.com"
echo "2. Regístrate con GitHub"
echo "3. New → Web Service"
echo "4. Conecta repositorio"
echo "5. Configura servicio:"
echo "   - Nombre: diabetes-api"
echo "   - Runtime: Python 3"
echo "   - Build: pip install -r requirements.txt"
echo "   - Start: python api.py --host 0.0.0.0 --port $PORT"
echo "6. Variables se configuran automáticamente"
echo "7. ¡Create Service!"
echo ""
echo "⏱️ Tiempo: 5-10 minutos"
echo "💰 Costo: GRATIS (750 horas)"
echo "🌍 URL final: https://diabetes-api.onrender.com"
'''

    with open('deploy.sh', 'w') as f:
        f.write(script_content)

    os.chmod('deploy.sh', 0o755)
    print("   ✅ deploy.sh creado")

def open_render_website():
    """Abrir sitio web de Render"""
    print("\n🌐 Abriendo Render...")
    try:
        webbrowser.open('https://render.com')
        print("   ✅ Navegador abierto en https://render.com")
        return True
    except:
        print("   ⚠️ No se pudo abrir navegador automáticamente")
        return False

def show_manual_steps():
    """Mostrar pasos manuales necesarios"""
    print("\n🎯 PASOS MANUALES REQUERIDOS:")
    print("="*50)

    print("\n1️⃣ CREAR CUENTA:")
    print("   • Ve a: https://render.com")
    print("   • Regístrate con GitHub (más rápido)")
    print("   • Confirma tu email")

    print("\n2️⃣ CONECTAR REPOSITORIO:")
    print("   • En Render Dashboard → 'New'")
    print("   • Selecciona 'Web Service'")
    print("   • Conecta tu repositorio GitHub")

    print("\n3️⃣ CONFIGURAR SERVICIO:")
    print("   • Nombre: diabetes-api")
    print("   • Runtime: Python 3")
    print("   • Build Command: pip install -r requirements.txt")
    print("   • Start Command: python api.py --host 0.0.0.0 --port $PORT")

    print("\n4️⃣ VARIABLES DE ENTORNO:")
    print("   • Se configuran automáticamente en render.yaml")
    print("   • SECRET_KEY y JWT_SECRET_KEY se generan automáticamente")

    print("\n5️⃣ DESPLEGAR:")
    print("   • Haz clic en 'Create Service'")
    print("   • Espera 3-5 minutos")
    print("   • ¡Tu API estará en: https://diabetes-api.onrender.com")

def show_benefits():
    """Mostrar beneficios de Render"""
    print("\n🏆 VENTAJAS DE RENDER PARA TU SISTEMA:")
    print("="*50)

    benefits = [
        "⚡ Mejor performance para ML (tus 15 modelos)",
        "💰 Base de datos PostgreSQL incluida GRATIS",
        "🌍 Mejor latencia para Latinoamérica",
        "📊 Analytics y métricas incluidos",
        "🔄 Despliegues automáticos desde Git",
        "🔒 SSL automático y gratuito",
        "📈 Auto-scaling automático",
        "🛠️ Fácil configuración y mantenimiento"
    ]

    for benefit in benefits:
        print(f"   • {benefit}")

def main():
    """Función principal"""
    print("🚀 DESPLIEGUE AUTOMÁTICO EN RENDER")
    print("="*50)

    # Verificar requisitos
    if not check_requirements():
        return 1

    # Crear script de despliegue
    create_deploy_script()

    # Abrir sitio web
    open_render_website()

    # Mostrar pasos manuales
    show_manual_steps()

    # Mostrar beneficios
    show_benefits()

    print("\n✅ ¡TODO LISTO PARA DESPLEGAR!")
    print("⏱️ Tiempo estimado: 5-10 minutos")
    print("💰 Costo inicial: GRATIS")
    print("🌍 URL final: https://diabetes-api.onrender.com")
    print("\n🎯 ¡Tu Sistema Predictivo de Diabetes estará funcionando en minutos!")

    return 0

if __name__ == "__main__":
    sys.exit(main())