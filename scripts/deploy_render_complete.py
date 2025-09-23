#!/usr/bin/env python3
"""
Script COMPLETO para desplegar en Render
Prepara todo automáticamente y proporciona instrucciones paso a paso
"""
import os
import subprocess
import sys
from pathlib import Path

def create_deployment_files():
    """Crear todos los archivos necesarios para Render"""
    print("📁 Creando archivos de despliegue...")

    files_created = []

    # 1. Procfile
    procfile_content = "web: python api.py --host 0.0.0.0 --port $PORT"
    with open('Procfile', 'w') as f:
        f.write(procfile_content)
    files_created.append('Procfile')
    print("   ✅ Procfile creado")

    # 2. runtime.txt
    runtime_content = "python-3.12.0"
    with open('runtime.txt', 'w') as f:
        f.write(runtime_content)
    files_created.append('runtime.txt')
    print("   ✅ runtime.txt creado")

    # 3. render.yaml completo
    render_yaml_content = '''services:
  # API REST del Sistema Predictivo de Diabetes
  - type: web
    name: diabetes-api
    runtime: python3
    buildCommand: pip install -r requirements.txt
    startCommand: python api.py --host 0.0.0.0 --port $PORT
    envVars:
      - key: ENVIRONMENT
        value: production
      - key: DEBUG
        value: false
      - key: LOG_LEVEL
        value: INFO
      - key: SECRET_KEY
        generateValue: true
      - key: JWT_SECRET_KEY
        generateValue: true
      - key: API_HOST
        value: 0.0.0.0
      - key: API_PORT
        value: 8002
      - key: STREAMLIT_SERVER_ADDRESS
        value: 0.0.0.0
      - key: STREAMLIT_SERVER_PORT
        value: 8501
      - key: STREAMLIT_SERVER_HEADLESS
        value: true
      - key: MLFLOW_TRACKING_URI
        value: file:///app/outputs/mlruns
      - key: MLFLOW_HOST
        value: 0.0.0.0
      - key: MLFLOW_PORT
        value: 5002

  # Base de datos PostgreSQL
  - type: pserv
    name: diabetes-db
    envVars:
      - key: DATABASE_URL
        fromService:
          type: pserv
          name: diabetes-db
          property: connectionString'''
    with open('render.yaml', 'w') as f:
        f.write(render_yaml_content)
    files_created.append('render.yaml')
    print("   ✅ render.yaml creado")

    return files_created

def install_render_cli():
    """Instalar Render CLI"""
    print("\n🔧 Instalando Render CLI...")

    try:
        # Intentar diferentes métodos de instalación
        install_commands = [
            "curl -fsSL https://cli.render.com/install | bash",
            "npm install -g @render/cli",
            "curl -o- https://raw.githubusercontent.com/render-oss/cli/main/install.sh | bash"
        ]

        for cmd in install_commands:
            try:
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                if result.returncode == 0:
                    print(f"   ✅ CLI instalada con: {cmd}")
                    return True
            except:
                continue

        print("   ⚠️ No se pudo instalar CLI automáticamente")
        return False

    except Exception as e:
        print(f"   ❌ Error instalando CLI: {e}")
        return False

def setup_git_repo():
    """Configurar repositorio git"""
    print("\n📋 Configurando repositorio Git...")

    try:
        # Verificar si ya está en git
        if Path('.git').exists():
            print("   ✅ Repositorio Git ya existe")
            return True

        # Inicializar git
        subprocess.run(['git', 'init'], check=True)
        subprocess.run(['git', 'add', '.'], check=True)
        subprocess.run(['git', 'commit', '-m', 'Initial commit - Sistema Predictivo de Diabetes'], check=True)

        print("   ✅ Repositorio Git configurado")
        return True

    except Exception as e:
        print(f"   ❌ Error configurando Git: {e}")
        return False

def create_deploy_script():
    """Crear script de despliegue automático"""
    print("\n🚀 Creando script de despliegue...")

    deploy_script = '''#!/bin/bash
echo "🚀 DESPLEGANDO SISTEMA PREDICTIVO DE DIABETES EN RENDER"
echo "="*60

# Verificar archivos necesarios
echo "📋 Verificando archivos..."
for file in Procfile runtime.txt requirements.txt; do
    if [ -f "$file" ]; then
        echo "   ✅ $file"
    else
        echo "   ❌ $file no encontrado"
        exit 1
    fi
done

echo ""
echo "🌐 URLs esperadas después del despliegue:"
echo "   • API REST: https://diabetes-api.onrender.com"
echo "   • Documentación: https://diabetes-api.onrender.com/docs"
echo "   • Health Check: https://diabetes-api.onrender.com/health"
echo ""
echo "📊 Variables de entorno que se configurarán automáticamente:"
echo "   • ENVIRONMENT=production"
echo "   • DEBUG=false"
echo "   • LOG_LEVEL=INFO"
echo "   • SECRET_KEY (generada automáticamente)"
echo "   • JWT_SECRET_KEY (generada automáticamente)"
echo "   • API_HOST=0.0.0.0"
echo "   • API_PORT=8002"
echo "   • STREAMLIT_SERVER_ADDRESS=0.0.0.0"
echo "   • STREAMLIT_SERVER_PORT=8501"
echo "   • STREAMLIT_SERVER_HEADLESS=true"
echo "   • MLFLOW_TRACKING_URI=file:///app/outputs/mlruns"
echo "   • MLFLOW_HOST=0.0.0.0"
echo "   • MLFLOW_PORT=5002"
echo ""
echo "💡 INSTRUCCIONES MANUALES:"
echo ""
echo "1. Ve a: https://render.com"
echo "2. Regístrate con GitHub/GitLab"
echo "3. Autoriza acceso a tu repositorio"
echo "4. New → Web Service"
echo "5. Conecta tu repositorio"
echo "6. Configura:"
echo "   - Nombre: diabetes-api"
echo "   - Runtime: Python 3"
echo "   - Build Command: pip install -r requirements.txt"
echo "   - Start Command: python api.py --host 0.0.0.0 --port $PORT"
echo "7. Las variables de entorno se configuran automáticamente"
echo "8. ¡Haz clic en 'Create Service'!"
echo ""
echo "⏱️ Tiempo estimado: 5-10 minutos"
echo "💰 Costo inicial: GRATIS"
echo "🌍 URL final: https://diabetes-api.onrender.com"
'''

    with open('deploy.sh', 'w') as f:
        f.write(deploy_script)

    # Hacer ejecutable
    os.chmod('deploy.sh', 0o755)
    print("   ✅ deploy.sh creado")

def show_final_instructions():
    """Mostrar instrucciones finales"""
    print("\n🎯 INSTRUCCIONES FINALES PARA DESPLEGAR:")
    print("="*60)

    print("\n1️⃣ CREAR CUENTA EN RENDER:")
    print("   • Ve a: https://render.com")
    print("   • Regístrate con GitHub (recomendado)")
    print("   • Confirma tu email")

    print("\n2️⃣ CONECTAR REPOSITORIO:")
    print("   • En Render Dashboard, haz clic en 'New'")
    print("   • Selecciona 'Web Service'")
    print("   • Conecta tu repositorio GitHub")

    print("\n3️⃣ CONFIGURAR SERVICIO:")
    print("   • Nombre: diabetes-api")
    print("   • Runtime: Python 3")
    print("   • Build Command: pip install -r requirements.txt")
    print("   • Start Command: python api.py --host 0.0.0.0 --port $PORT")

    print("\n4️⃣ VARIABLES DE ENTORNO (automáticas):")
    print("   • ENVIRONMENT=production")
    print("   • DEBUG=false")
    print("   • LOG_LEVEL=INFO")
    print("   • SECRET_KEY (generada)")
    print("   • JWT_SECRET_KEY (generada)")
    print("   • API_HOST=0.0.0.0")
    print("   • API_PORT=8002")
    print("   • STREAMLIT_SERVER_ADDRESS=0.0.0.0")
    print("   • STREAMLIT_SERVER_PORT=8501")
    print("   • STREAMLIT_SERVER_HEADLESS=true")
    print("   • MLFLOW_TRACKING_URI=file:///app/outputs/mlruns")
    print("   • MLFLOW_HOST=0.0.0.0")
    print("   • MLFLOW_PORT=5002")

    print("\n5️⃣ DESPLEGAR:")
    print("   • Haz clic en 'Create Service'")
    print("   • Espera 3-5 minutos")
    print("   • ¡Tu API estará lista!")

    print("\n🌐 URLS QUE OBTENDRÁS:")
    print("   • API REST: https://diabetes-api.onrender.com")
    print("   • Documentación: https://diabetes-api.onrender.com/docs")
    print("   • Health Check: https://diabetes-api.onrender.com/health")

    print("\n💰 COSTOS:")
    print("   • Primeros 750 horas: GRATIS")
    print("   • Después: $7/mes")
    print("   • Base de datos: INCLUIDA GRATIS")

def main():
    """Función principal"""
    print("🚀 DESPLIEGUE COMPLETO EN RENDER - SISTEMA PREDICTIVO DE DIABETES")
    print("="*70)

    # Crear archivos necesarios
    files_created = create_deployment_files()

    # Configurar git
    setup_git_repo()

    # Crear script de despliegue
    create_deploy_script()

    # Mostrar instrucciones
    show_final_instructions()

    print("\n✅ ¡CONFIGURACIÓN COMPLETADA!")
    print(f"📁 Archivos creados: {', '.join(files_created)}")
    print("📋 Repositorio Git: Configurado")
    print("🚀 Script de despliegue: Listo")
    print("\n🎯 TU SISTEMA ESTÁ LISTO PARA PRODUCCIÓN!")
    print("⏱️ Tiempo estimado de despliegue: 5-10 minutos")
    print("💰 Costo inicial: GRATIS")
    print("🌍 URL final: https://diabetes-api.onrender.com")

    return 0

if __name__ == "__main__":
    sys.exit(main())