#!/usr/bin/env python3
"""
Script simple para probar la carga del predictor
"""
import sys
import os
from pathlib import Path

# Agregar el directorio actual al path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    print("🔄 Probando importación del predictor...")
    from predictor import DiabetesPredictor
    print("✅ Predictor importado exitosamente")

    print("\n🔄 Creando instancia del predictor...")
    predictor = DiabetesPredictor()
    print("✅ Predictor creado exitosamente")

    print("\n🔄 Probando predicción simple...")
    test_data = {
        'edad': 50,
        'sexo': 'M',
        'imc': 25.0,
        'tas': 120,
        'tad': 80,
        'perimetro_abdominal': 90,
        'frecuencia_cardiaca': 70,
        'realiza_ejercicio': 'No',
        'fuma': 'No',
        'historia_familiar_dm': 'No',
        'puntaje_findrisc': 5,
        'riesgo_cardiovascular': 0.2
    }

    result = predictor.predict(test_data)

    if "error" in result:
        print(f"❌ Error en predicción: {result['error']}")
        sys.exit(1)
    else:
        print("✅ Predicción exitosa:")
        print(f"   Glucosa: {result['glucose_mg_dl']} mg/dL")
        print(f"   Categoría: {result['category']}")
        print(f"   Riesgo: {result['risk_level']}")
        print("\n🎉 TODO FUNCIONA CORRECTAMENTE")
        sys.exit(0)

except ImportError as e:
    print(f"❌ Error de importación: {e}")
    print("\n🔍 Posibles soluciones:")
    print("   1. Verificar que predictor.py existe")
    print("   2. Verificar dependencias en requirements.txt")
    print("   3. Verificar imports dentro de predictor.py")
    sys.exit(1)

except Exception as e:
    print(f"❌ Error inesperado: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)