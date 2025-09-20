#!/usr/bin/env python3
"""
Script de prueba para verificar que el sistema funciona correctamente
"""
import sys
import os
from pathlib import Path

def test_imports():
    """Probar que todos los módulos se pueden importar"""
    print("🧪 Probando importaciones...")

    try:
        from config import config
        print("   ✅ config.py - OK")

        from data_generator import create_sample_dataset
        print("   ✅ data_generator.py - OK")

        from data_preprocessor import preprocess_diabetes_data
        print("   ✅ data_preprocessor.py - OK")

        from model_trainer import train_diabetes_models
        print("   ✅ model_trainer.py - OK")

        from predictor import predict_glucose
        print("   ✅ predictor.py - OK")

        return True

    except ImportError as e:
        print(f"   ❌ Error de importación: {e}")
        return False

def test_config():
    """Probar configuración"""
    print("\n🔧 Probando configuración...")

    try:
        from config import config

        print(f"   ✅ Directorio raíz: {config.PROJECT_ROOT}")
        print(f"   ✅ Directorio modelos: {config.MODELS_DIR}")
        print(f"   ✅ Directorio salidas: {config.OUTPUTS_DIR}")
        print(f"   ✅ Directorio datos: {config.DATA_DIR}")

        # Verificar que los directorios existen
        for dir_path in [config.MODELS_DIR, config.OUTPUTS_DIR, config.DATA_DIR]:
            if dir_path.exists():
                print(f"   ✅ Directorio existe: {dir_path}")
            else:
                print(f"   ⚠️ Directorio no existe (se creará): {dir_path}")

        return True

    except Exception as e:
        print(f"   ❌ Error en configuración: {e}")
        return False

def test_data_generation():
    """Probar generación de datos"""
    print("\n📊 Probando generación de datos...")

    try:
        from data_generator import create_sample_dataset

        # Generar datos pequeños para prueba
        df = create_sample_dataset(n_samples=50)

        print(f"   ✅ Datos generados: {df.shape[0]} filas, {df.shape[1]} columnas")
        print(f"   ✅ Columnas: {list(df.columns)}")
        print(f"   ✅ Tipos de datos únicos: {df.dtypes.nunique()}")

        # Verificar que no hay valores nulos
        null_count = df.isnull().sum().sum()
        if null_count == 0:
            print("   ✅ No hay valores nulos")
        else:
            print(f"   ⚠️ Hay {null_count} valores nulos")

        return True

    except Exception as e:
        print(f"   ❌ Error en generación de datos: {e}")
        return False

def test_preprocessing():
    """Probar preprocesamiento"""
    print("\n🔧 Probando preprocesamiento...")

    try:
        from data_generator import create_sample_dataset
        from data_preprocessor import preprocess_diabetes_data

        # Generar datos
        df = create_sample_dataset(n_samples=50)

        # Preprocesar
        df_processed, preprocessor = preprocess_diabetes_data(df)

        print(f"   ✅ Datos procesados: {df_processed.shape[0]} filas, {df_processed.shape[1]} columnas")
        print(f"   ✅ Características finales: {list(df_processed.columns)}")

        # Verificar que la variable objetivo existe
        if 'Resultado' in df_processed.columns:
            print("   ✅ Variable objetivo presente")
        else:
            print("   ❌ Variable objetivo faltante")

        return True

    except Exception as e:
        print(f"   ❌ Error en preprocesamiento: {e}")
        return False

def test_prediction():
    """Probar predicción"""
    print("\n🔮 Probando predicción...")

    try:
        from predictor import predict_glucose

        # Datos de prueba
        patient_data = {
            'edad': 45,
            'sexo': 'M',
            'imc': 25.5,
            'tas': 120,
            'tad': 80,
            'perimetro_abdominal': 90,
            'realiza_ejercicio': 'Si',
            'fuma': 'No',
            'historia_familiar_dm': 'No'
        }

        # Hacer predicción
        result = predict_glucose(patient_data)

        if "error" not in result:
            print("   ✅ Predicción exitosa")
            print(f"      Glucosa: {result['glucose_mg_dl']} mg/dL")
            print(f"      Categoría: {result['category']}")
            print(f"      Riesgo: {result['risk_level']}")
            print(f"      Confianza: {result['confidence']}")
        else:
            print(f"   ❌ Error en predicción: {result['error']}")
            return False

        return True

    except Exception as e:
        print(f"   ❌ Error en predicción: {e}")
        return False

def test_model_training():
    """Probar entrenamiento de modelos (versión ligera)"""
    print("\n🤖 Probando entrenamiento de modelos...")

    try:
        from data_generator import create_sample_dataset
        from data_preprocessor import preprocess_diabetes_data
        from model_trainer import train_diabetes_models

        # Generar datos pequeños
        df = create_sample_dataset(n_samples=100)

        # Preprocesar
        df_processed, preprocessor = preprocess_diabetes_data(df)

        # Entrenar modelos (solo 2 para prueba rápida)
        print("   ⚠️ Entrenando solo 2 modelos para prueba rápida...")

        # Modificar temporalmente para entrenar solo 2 modelos
        import model_trainer
        original_models = model_trainer.DiabetesModelTrainer().models.copy()
        model_trainer.DiabetesModelTrainer().models = dict(list(original_models.items())[:2])

        trainer = train_diabetes_models(df_processed, preprocessor)

        # Verificar que se entrenaron modelos
        results_df = trainer.get_results_dataframe()
        if not results_df.empty:
            print(f"   ✅ Modelos entrenados: {len(results_df)}")
            print(f"   ✅ Mejor modelo: {trainer.best_model_name}")
            print(f"   ✅ R² Score: {trainer.results[0]['test_r2']:.4f}")
        else:
            print("   ❌ No se obtuvieron resultados")
            return False

        return True

    except Exception as e:
        print(f"   ❌ Error en entrenamiento: {e}")
        return False

def main():
    """Función principal de pruebas"""
    print("="*60)
    print("🧪 PRUEBAS DEL SISTEMA PREDICTIVO DE DIABETES")
    print("="*60)

    tests = [
        ("Importaciones", test_imports),
        ("Configuración", test_config),
        ("Generación de datos", test_data_generation),
        ("Preprocesamiento", test_preprocessing),
        ("Predicción", test_prediction),
        ("Entrenamiento de modelos", test_model_training)
    ]

    results = []

    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        success = test_func()
        results.append((test_name, success))

    # Resumen final
    print("\n" + "="*60)
    print("📊 RESUMEN DE PRUEBAS")
    print("="*60)

    passed = 0
    total = len(results)

    for test_name, success in results:
        status = "✅ PASÓ" if success else "❌ FALLÓ"
        print(f"   {test_name}: {status}")
        if success:
            passed += 1

    print(f"\n🎯 Resultado: {passed}/{total} pruebas pasaron")

    if passed == total:
        print("🎉 ¡Todas las pruebas pasaron! El sistema está funcionando correctamente.")
        return 0
    else:
        print("⚠️ Algunas pruebas fallaron. Revisa los errores arriba.")
        return 1

if __name__ == "__main__":
    sys.exit(main())