#!/usr/bin/env python3
"""
Script principal para el Sistema Predictivo de Diabetes
Ejecuta el pipeline completo: generación de datos, preprocesamiento, entrenamiento y evaluación
"""
import argparse
import sys
from pathlib import Path
from datetime import datetime
import pandas as pd

# Importar módulos del proyecto
from config import config
from data_generator import create_sample_dataset, DiabetesDataGenerator
from data_preprocessor import preprocess_diabetes_data
from model_trainer import train_diabetes_models
from predictor import DiabetesPredictor, predict_glucose

def print_header():
    """Imprimir encabezado del programa"""
    print("="*80)
    print("🏥 SISTEMA PREDICTIVO DE DIABETES MELLITUS TIPO 2".center(80))
    print("="*80)
    print(f"📅 Fecha de ejecución: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📁 Directorio de trabajo: {config.PROJECT_ROOT}")
    print("="*80)

def run_full_pipeline(n_samples: int = 1000, save_data: bool = True) -> bool:
    """
    Ejecutar el pipeline completo del sistema

    Args:
        n_samples: Número de muestras a generar
        save_data: Guardar datos generados

    Returns:
        bool: True si se ejecutó correctamente
    """
    try:
        print_header()

        print("\n🚀 INICIANDO PIPELINE COMPLETO")
        print("="*60)

        # 1. Generar datos sintéticos
        print("\n📊 FASE 1: Generación de datos")
        print("-" * 40)

        if save_data:
            generator = DiabetesDataGenerator(n_samples=n_samples)
            df = generator.generate_synthetic_data()
            data_path = generator.save_data(df)
            print(f"✅ Datos guardados en: {data_path}")
        else:
            df = create_sample_dataset(n_samples=n_samples)
            print("✅ Datos generados en memoria")

        # 2. Preprocesar datos
        print("\n🔧 FASE 2: Preprocesamiento de datos")
        print("-" * 40)

        df_processed, preprocessor = preprocess_diabetes_data(df)

        # 3. Entrenar modelos
        print("\n🤖 FASE 3: Entrenamiento de modelos")
        print("-" * 40)

        trainer = train_diabetes_models(df_processed, preprocessor)

        # 4. Mostrar resumen final
        print("\n📊 FASE 4: Resumen de resultados")
        print("-" * 40)

        results_df = trainer.get_results_dataframe()
        if not results_df.empty:
            print("\n🏆 TOP 5 MODELOS:")
            print(results_df.head().to_string(index=False))

            # Mostrar mejor modelo
            best_model, best_name, best_r2 = trainer.get_best_model()
            print(f"\n🎯 Mejor modelo: {best_name}")
            print(f"   R² Score: {best_r2:.4f}")

        print("\n✅ PIPELINE COMPLETADO EXITOSAMENTE")
        print("="*60)

        return True

    except Exception as e:
        print(f"\n❌ ERROR EN EL PIPELINE: {e}")
        import traceback
        traceback.print_exc()
        return False

def run_prediction_example():
    """Ejecutar ejemplo de predicción"""
    print_header()

    print("\n🔮 EJEMPLO DE PREDICCIÓN")
    print("="*60)

    # Datos de ejemplo de un paciente
    patient_example = {
        'edad': 55,
        'sexo': 'M',
        'imc': 28.5,
        'tas': 135,
        'tad': 85,
        'perimetro_abdominal': 95,
        'frecuencia_cardiaca': 75,
        'realiza_ejercicio': 'No',
        'fuma': 'No',
        'historia_familiar_dm': 'Si',
        'puntaje_findrisc': 12,
        'riesgo_cardiovascular': 0.4
    }

    print(f"📋 Datos del paciente: {patient_example}")

    # Hacer predicción
    try:
        result = predict_glucose(patient_example)

        if "error" not in result:
            print("\n🎯 Resultado de la predicción:")
            print(f"   Glucosa estimada: {result['glucose_mg_dl']} mg/dL")
            print(f"   Categoría: {result['category']}")
            print(f"   Nivel de riesgo: {result['risk_level']}")
            print(f"   Confianza: {result['confidence']}")
            print(f"   Interpretación: {result['interpretation']}")
        else:
            print(f"❌ Error: {result['error']}")

    except Exception as e:
        print(f"❌ Error en predicción: {e}")

def run_data_analysis():
    """Ejecutar análisis exploratorio de datos"""
    print_header()

    print("\n📊 ANÁLISIS EXPLORATORIO DE DATOS")
    print("="*60)

    try:
        # Generar datos
        df = create_sample_dataset(n_samples=500)

        # Mostrar información básica
        print(f"📋 Información del dataset:")
        print(f"   Dimensiones: {df.shape}")
        print(f"   Columnas: {len(df.columns)}")
        print(f"   Registros: {len(df)}")

        print("\n📈 Estadísticas descriptivas:")
        print(df.describe())

        # Análisis de categorías de diabetes
        def categorizar_glucosa(valor):
            if valor < 100:
                return 'Normal'
            elif valor <= 126:
                return 'Prediabetes'
            else:
                return 'Diabetes'

        df['categoria_diabetes'] = df['Resultado'].apply(categorizar_glucosa)

        print("\n🎯 Distribución de categorías:")
        categoria_counts = df['categoria_diabetes'].value_counts()
        for cat, count in categoria_counts.items():
            porcentaje = (count / len(df)) * 100
            print(f"   {cat}: {count} casos ({porcentaje:.1f}%)")

        # Guardar análisis
        analysis_path = config.get_output_path("data_analysis.csv")
        df.to_csv(analysis_path, index=False)
        print(f"\n💾 Análisis guardado en: {analysis_path}")

    except Exception as e:
        print(f"❌ Error en análisis: {e}")

def main():
    """Función principal"""
    parser = argparse.ArgumentParser(
        description="Sistema Predictivo de Diabetes Mellitus Tipo 2",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  python main.py                    # Ejecutar pipeline completo
  python main.py --samples 2000     # Pipeline con 2000 muestras
  python main.py --predict          # Solo ejemplo de predicción
  python main.py --analyze          # Solo análisis de datos
  python main.py --no-save          # No guardar datos generados
        """
    )

    parser.add_argument(
        "--samples", "-s",
        type=int,
        default=1000,
        help="Número de muestras a generar (por defecto: 1000)"
    )

    parser.add_argument(
        "--predict", "-p",
        action="store_true",
        help="Ejecutar solo ejemplo de predicción"
    )

    parser.add_argument(
        "--analyze", "-a",
        action="store_true",
        help="Ejecutar solo análisis exploratorio de datos"
    )

    parser.add_argument(
        "--no-save",
        action="store_true",
        help="No guardar datos generados en disco"
    )

    args = parser.parse_args()

    # Ejecutar según argumentos
    if args.predict:
        run_prediction_example()
    elif args.analyze:
        run_data_analysis()
    else:
        success = run_full_pipeline(
            n_samples=args.samples,
            save_data=not args.no_save
        )

        if success:
            print("\n🎉 ¡Sistema ejecutado exitosamente!")
            print("\n📁 Archivos generados:")
            print(f"   Modelos: {config.MODELS_DIR}")
            print(f"   Salidas: {config.OUTPUTS_DIR}")
            print(f"   Datos: {config.DATA_DIR}")

            print("\n🔮 Para hacer predicciones:")
            print("   from predictor import predict_glucose")
            print("   result = predict_glucose(datos_paciente)")
        else:
            print("\n❌ El sistema terminó con errores")
            sys.exit(1)

if __name__ == "__main__":
    main()