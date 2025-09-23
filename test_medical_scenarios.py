#!/usr/bin/env python3
"""
Script de pruebas médicas con diferentes escenarios clínicos
"""
import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"

def test_scenario(name, patient_data):
    """Probar un escenario médico específico"""
    print(f"\n🩺 {name}")
    print("=" * 50)

    try:
        response = requests.post(
            f"{BASE_URL}/predict",
            json=patient_data,
            timeout=10
        )

        if response.status_code == 200:
            result = response.json()
            print("✅ Predicción exitosa:")
            print(f"   🩸 Glucosa: {result['glucose_mg_dl']:.1f} mg/dL")
            print(f"   📊 Categoría: {result['category']}")
            print(f"   ⚠️ Riesgo: {result['risk_level']}")
            print(f"   🎯 Confianza: {result['confidence']}")
            print(f"   💡 Interpretación: {result['interpretation']}")
            print(f"   ⏱️ Tiempo: {result['processing_time_ms']:.2f}ms")
            return True
        else:
            print(f"❌ Error HTTP {response.status_code}: {response.text}")
            return False

    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False

def main():
    print("🏥 PRUEBAS DE ESCENARIOS MÉDICOS")
    print("================================")

    # Escenario 1: Paciente de bajo riesgo
    low_risk_patient = {
        "edad": 25,
        "sexo": "F",
        "imc": 22.1,
        "tas": 110,
        "tad": 70,
        "perimetro_abdominal": 75,
        "frecuencia_cardiaca": 65,
        "realiza_ejercicio": "Si",
        "consume_alcohol": "Nunca",
        "fuma": "No",
        "medicamentos_hta": "No",
        "historia_familiar_dm": "No",
        "diabetes_gestacional": "No",
        "puntaje_findrisc": 3,
        "riesgo_cardiovascular": 0.1
    }

    # Escenario 2: Paciente de riesgo moderado
    moderate_risk_patient = {
        "edad": 45,
        "sexo": "M",
        "imc": 28.5,
        "tas": 135,
        "tad": 85,
        "perimetro_abdominal": 95,
        "frecuencia_cardiaca": 75,
        "realiza_ejercicio": "Si",
        "consume_alcohol": "Ocasional",
        "fuma": "No",
        "medicamentos_hta": "Si",
        "historia_familiar_dm": "Si",
        "diabetes_gestacional": "No",
        "puntaje_findrisc": 12,
        "riesgo_cardiovascular": 0.4
    }

    # Escenario 3: Paciente de alto riesgo
    high_risk_patient = {
        "edad": 65,
        "sexo": "M",
        "imc": 32.8,
        "tas": 150,
        "tad": 95,
        "perimetro_abdominal": 110,
        "frecuencia_cardiaca": 85,
        "realiza_ejercicio": "No",
        "consume_alcohol": "Frecuente",
        "fuma": "Si",
        "medicamentos_hta": "Si",
        "historia_familiar_dm": "Si",
        "diabetes_gestacional": "No",
        "puntaje_findrisc": 18,
        "riesgo_cardiovascular": 0.7
    }

    # Escenario 4: Mujer con diabetes gestacional
    gestational_patient = {
        "edad": 35,
        "sexo": "F",
        "imc": 29.2,
        "tas": 125,
        "tad": 80,
        "perimetro_abdominal": 88,
        "frecuencia_cardiaca": 72,
        "realiza_ejercicio": "Si",
        "consume_alcohol": "Nunca",
        "fuma": "No",
        "medicamentos_hta": "No",
        "historia_familiar_dm": "Si",
        "diabetes_gestacional": "Si",
        "puntaje_findrisc": 8,
        "riesgo_cardiovascular": 0.3
    }

    # Ejecutar pruebas
    scenarios = [
        ("PACIENTE BAJO RIESGO", low_risk_patient),
        ("PACIENTE RIESGO MODERADO", moderate_risk_patient),
        ("PACIENTE ALTO RIESGO", high_risk_patient),
        ("MUJER CON DIABETES GESTACIONAL", gestational_patient)
    ]

    results = []
    for name, data in scenarios:
        success = test_scenario(name, data)
        results.append((name, success))

    # Resumen
    print("\n📊 RESUMEN DE PRUEBAS")
    print("=" * 50)
    successful = sum(1 for _, success in results if success)
    total = len(results)

    print(f"✅ Pruebas exitosas: {successful}/{total}")

    for name, success in results:
        status = "✅" if success else "❌"
        print(f"   {status} {name}")

    print("\n🌐 INTERFACES DISPONIBLES:")
    print(f"   🔌 API REST: {BASE_URL}")
    print(f"   📊 Swagger: {BASE_URL}/docs")
    print(f"   🖥️ Streamlit: http://localhost:8502")
    print(f"   📈 MLflow: http://localhost:5000")

if __name__ == "__main__":
    main()