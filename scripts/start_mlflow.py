#!/usr/bin/env python3
"""
Script wrapper para iniciar MLflow UI con mejor manejo de errores
"""
import os
import sys
import time
import subprocess
from pathlib import Path

def main():
    """Iniciar MLflow UI con configuración robusta"""
    print("🚀 Iniciando MLflow UI...")

    # Crear directorio de outputs si no existe
    outputs_dir = Path("outputs")
    mlruns_dir = outputs_dir / "mlruns"

    try:
        outputs_dir.mkdir(exist_ok=True)
        mlruns_dir.mkdir(exist_ok=True)
        print(f"✅ Directorio creado: {mlruns_dir}")
    except Exception as e:
        print(f"⚠️ Error creando directorio: {e}")

    # Configurar variables de entorno
    env = os.environ.copy()
    env['MLFLOW_TRACKING_URI'] = str(mlruns_dir.absolute())
    env['MLFLOW_BACKEND_STORE_URI'] = str(mlruns_dir.absolute())

    # Comando para iniciar MLflow
    cmd = [
        sys.executable, "-m", "mlflow", "ui",
        "--backend-store-uri", str(mlruns_dir.absolute()),
        "--host", "0.0.0.0",
        "--port", "5000"  # Usar puerto fijo en lugar de $PORT
    ]

    print(f"📍 Comando: {' '.join(cmd)}")
    print(f"📁 Backend Store: {mlruns_dir.absolute()}")

    try:
        # Iniciar MLflow
        process = subprocess.Popen(cmd, env=env)
        print("✅ MLflow UI iniciado correctamente")
        print("🌐 URL: http://localhost:5000")
        # Mantener el proceso vivo
        process.wait()

    except KeyboardInterrupt:
        print("\n🛑 Deteniendo MLflow UI...")
        process.terminate()
    except Exception as e:
        print(f"❌ Error iniciando MLflow: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()