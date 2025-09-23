#!/bin/bash
# Script completo de pruebas del Sistema Predictivo de Diabetes
echo "🏥 PRUEBAS COMPLETAS DEL SISTEMA PREDICTIVO DE DIABETES"
echo "=================================================="

BASE_URL="http://localhost:8000"

echo -e "\n🔍 1. HEALTH CHECK"
curl -X GET "$BASE_URL/health" | python -m json.tool

echo -e "\n📊 2. INFORMACIÓN DEL MODELO"
curl -X GET "$BASE_URL/model/info" | python -m json.tool

echo -e "\n🤖 3. MODELOS DISPONIBLES"
curl -X GET "$BASE_URL/models" | python -m json.tool

echo -e "\n📋 4. CATEGORÍAS DE PREDICCIÓN"
curl -X GET "$BASE_URL/categories" | python -m json.tool

echo -e "\n🔧 5. CARACTERÍSTICAS REQUERIDAS"
curl -X GET "$BASE_URL/features" | python -m json.tool

echo -e "\n🔮 6. PREDICCIÓN CON GRADIENT BOOSTING"
curl -X POST "$BASE_URL/models/gradient_boosting/predict" \
  -H "Content-Type: application/json" \
  -d '{
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
  }' | python -m json.tool

echo -e "\n🌲 7. PREDICCIÓN CON RANDOM FOREST"
curl -X POST "$BASE_URL/models/random_forest/predict" \
  -H "Content-Type: application/json" \
  -d '{
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
  }' | python -m json.tool

echo -e "\n📊 8. ANÁLISIS BATCH (5 pacientes)"
curl -X POST "$BASE_URL/predict/batch" \
  -H "Content-Type: application/json" \
  -d '[
    {
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
    },
    {
      "edad": 35,
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
    },
    {
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
  ]' | python -m json.tool

echo -e "\n✅ PRUEBAS COMPLETADAS"
echo "===================="
echo "🌐 API: http://localhost:8000"
echo "📊 Swagger: http://localhost:8000/docs"
echo "🖥️ Streamlit: http://localhost:8502"
echo "📈 MLflow: http://localhost:5000 (si está ejecutándose)"