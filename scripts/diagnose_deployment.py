#!/usr/bin/env python3
"""
Script de diagnóstico para el despliegue en Railway
Verifica variables de entorno críticas y configuración del sistema
"""
import os
import sys
from pathlib import Path
import json

def check_critical_variables():
    """Verificar variables de entorno críticas"""
    print("🔍 Verificando variables de entorno críticas...")

    critical_vars = {
        'ENVIRONMENT': 'test|production',
        'DEBUG': 'true|false',
        'LOG_LEVEL': 'DEBUG|INFO|WARNING|ERROR',
        'API_HOST': '0.0.0.0',
        'API_PORT': '8002',
        'STREAMLIT_SERVER_ADDRESS': '0.0.0.0',
        'STREAMLIT_SERVER_PORT': '8501',
        'STREAMLIT_SERVER_HEADLESS': 'true',
        'MLFLOW_TRACKING_URI': 'file:///app/outputs/mlruns',
        'MLFLOW_HOST': '0.0.0.0',
        'MLFLOW_PORT': '5002'
    }

    security_vars = {
        'SECRET_KEY': 'Debe estar configurada',
        'JWT_SECRET_KEY': 'Debe estar configurada'
    }

    issues = []

    # Verificar variables críticas
    for var, expected in critical_vars.items():
        value = os.getenv(var)
        if value is None:
            issues.append(f"❌ Variable faltante: {var}")
        else:
            print(f"   ✅ {var}: {value}")

    # Verificar variables de seguridad
    for var, expected in security_vars.items():
        value = os.getenv(var)
        if value is None:
            issues.append(f"❌ Variable de seguridad faltante: {var}")
        elif len(value) < 10:
            issues.append(f"⚠️ Variable de seguridad muy corta: {var}")
        else:
            print(f"   ✅ {var}: {'*' * len(value)}")

    return issues

def check_file_permissions():
    """Verificar permisos de archivos"""
    print("\n🔐 Verificando permisos de archivos...")

    issues = []

    # Verificar archivos críticos
    critical_files = [
        'api.py',
        'web_app.py',
        'predictor.py',
        'config.py'
    ]

    for file_path in critical_files:
        if Path(file_path).exists():
            print(f"   ✅ {file_path} existe")
        else:
            issues.append(f"❌ Archivo faltante: {file_path}")

    return issues

def check_models_availability():
    """Verificar disponibilidad de modelos"""
    print("\n🤖 Verificando modelos...")

    issues = []

    models_dir = Path('models')
    if models_dir.exists():
        model_files = list(models_dir.glob('*.joblib'))
        if model_files:
            print(f"   ✅ Modelos encontrados: {len(model_files)}")
            for model_file in model_files[:3]:  # Mostrar primeros 3
                print(f"      - {model_file.name}")
            if len(model_files) > 3:
                print(f"      ... y {len(model_files) - 3} más")
        else:
            issues.append("❌ No se encontraron modelos .joblib")
    else:
        issues.append("❌ Directorio models/ no existe")

    # Verificar scaler
    scaler_path = models_dir / 'scaler.joblib'
    if scaler_path.exists():
        print("   ✅ Scaler encontrado")
    else:
        issues.append("❌ Scaler no encontrado")

    return issues

def check_requirements():
    """Verificar dependencias críticas"""
    print("\n📦 Verificando dependencias...")

    issues = []

    try:
        import fastapi
        print("   ✅ FastAPI disponible")
    except ImportError:
        issues.append("❌ FastAPI no disponible")

    try:
        import streamlit
        print("   ✅ Streamlit disponible")
    except ImportError:
        issues.append("❌ Streamlit no disponible")

    try:
        import mlflow
        print("   ✅ MLflow disponible")
    except ImportError:
        issues.append("❌ MLflow no disponible")

    try:
        import sklearn
        print("   ✅ Scikit-learn disponible")
    except ImportError:
        issues.append("❌ Scikit-learn no disponible")

    return issues

def check_ports_configuration():
    """Verificar configuración de puertos"""
    print("\n🔌 Verificando configuración de puertos...")

    issues = []

    # Verificar que los puertos no estén en conflicto
    ports = {
        'API': os.getenv('API_PORT', '8002'),
        'Streamlit': os.getenv('STREAMLIT_SERVER_PORT', '8501'),
        'MLflow': os.getenv('MLFLOW_PORT', '5002')
    }

    port_numbers = []
    for service, port in ports.items():
        try:
            port_num = int(port)
            if port_num in port_numbers:
                issues.append(f"❌ Conflicto de puertos: {service} usa puerto {port} (ya usado)")
            else:
                port_numbers.append(port_num)
                print(f"   ✅ {service}: {port}")
        except ValueError:
            issues.append(f"❌ Puerto inválido para {service}: {port}")

    return issues

def main():
    """Función principal de diagnóstico"""
    print("="*70)
    print("🔍 DIAGNÓSTICO DE DESPLIEGUE EN RAILWAY")
    print("="*70)

    all_issues = []

    # Ejecutar todas las verificaciones
    checks = [
        ("Variables de Entorno", check_critical_variables),
        ("Permisos de Archivos", check_file_permissions),
        ("Modelos", check_models_availability),
        ("Dependencias", check_requirements),
        ("Configuración de Puertos", check_ports_configuration)
    ]

    for check_name, check_function in checks:
        print(f"\n{'='*20} {check_name} {'='*20}")
        issues = check_function()
        all_issues.extend(issues)

    # Resumen
    print(f"\n{'='*70}")
    print("📊 RESUMEN DEL DIAGNÓSTICO")
    print(f"{'='*70}")

    if all_issues:
        print(f"\n❌ Se encontraron {len(all_issues)} problemas:")
        for i, issue in enumerate(all_issues, 1):
            print(f"   {i}. {issue}")

        print("\n🚨 ACCIONES RECOMENDADAS:")
        print("1. Configurar las variables de entorno faltantes")
        print("2. Verificar que los modelos estén incluidos en el build")
        print("3. Revisar los logs del despliegue")
        print("4. Probar el health check de la API")
        print("5. Verificar conectividad entre servicios")
    else:
        print("\n✅ No se encontraron problemas críticos")
        print("🎉 El sistema parece estar correctamente configurado")

    print(f"\n{'='*70}")

    return len(all_issues) == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)