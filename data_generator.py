"""
Módulo para generación de datos sintéticos de diabetes
"""
import numpy as np
import pandas as pd
from datetime import datetime
import random
from typing import Dict, List, Optional
from config import config, RANDOM_SEED

class DiabetesDataGenerator:
    """Generador de datos sintéticos para diabetes"""

    def __init__(self, n_samples: int = None, random_state: int = None):
        self.n_samples = n_samples or config.DEFAULT_N_SAMPLES
        self.random_state = random_state or RANDOM_SEED

        # Configurar semillas para reproducibilidad
        np.random.seed(self.random_state)
        random.seed(self.random_state)

    def generate_synthetic_data(self) -> pd.DataFrame:
        """
        Genera un dataset sintético de diabetes con características realistas

        Returns:
            pd.DataFrame: Dataset sintético con características médicas
        """
        print(f"🔄 Generando dataset sintético con {self.n_samples} registros...")

        data = []

        for i in range(self.n_samples):
            # Determinar categoría de diabetes primero
            rand = np.random.random()

            if rand < 0.40:  # 40% Normal
                category = 0
                glucose_base = np.random.uniform(70, 99)
            elif rand < 0.75:  # 35% Prediabetes
                category = 1
                glucose_base = np.random.uniform(100, 126)
            else:  # 25% Diabetes
                category = 2
                glucose_base = np.random.uniform(127, 200)

            # Generar características correlacionadas con la categoría
            record = self._generate_patient_record(i, category, glucose_base)
            data.append(record)

        df = pd.DataFrame(data)

        # Redondear valores numéricos
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        for col in numeric_columns:
            if col != 'identificacion':
                df[col] = df[col].round(2)

        print(f"✅ Dataset generado: {df.shape[0]} registros, {df.shape[1]} columnas")
        return df

    def _generate_patient_record(self, patient_id: int, category: int, glucose_base: float) -> Dict:
        """Genera un registro individual de paciente"""

        # Características demográficas
        edad = max(config.MIN_AGE, min(config.MAX_AGE,
            30 + category * 10 + np.random.normal(0, 15)))
        sexo = random.choice(['M', 'F'])
        zona_residencia = random.choice(['Urbana', 'Rural'])
        estrato = random.choice([1, 2, 3, 4, 5, 6])

        # Características antropométricas
        talla = max(140, min(200, np.random.normal(165, 10)))  # cm
        peso = max(40, min(150, 60 + category * 10 + np.random.normal(0, 15)))  # kg
        imc = max(16, min(45, 22 + category * 4 + np.random.normal(0, 3)))
        perimetro_abdominal = max(60, min(150, 80 + category * 10 + np.random.normal(0, 10)))

        # Características clínicas
        tas = max(90, min(200, 110 + category * 15 + np.random.normal(0, 10)))  # Presión sistólica
        tad = max(60, min(120, 70 + category * 10 + np.random.normal(0, 7)))   # Presión diastólica
        frecuencia_cardiaca = max(50, min(110, 70 + category * 5 + np.random.normal(0, 10)))

        # Factores de riesgo
        realiza_ejercicio = random.choices(['Si', 'No'],
            weights=[0.4-category*0.1, 0.6+category*0.1])[0]
        consume_alcohol = random.choice(['Nunca', 'Ocasional', 'Frecuente'])
        fuma = random.choices(['Si', 'No'],
            weights=[0.2+category*0.1, 0.8-category*0.1])[0]
        medicamentos_hta = random.choices(['Si', 'No'],
            weights=[category*0.3, 1-category*0.3])[0]

        # Antecedentes
        historia_familiar_dm = random.choices(['Si', 'No'],
            weights=[0.3+category*0.2, 0.7-category*0.2])[0]
        diabetes_gestacional = 'No' if sexo == 'M' else random.choice(['Si', 'No'])

        # Scores de riesgo
        puntaje_findrisc = max(0, min(26, 5 + category * 7 + np.random.normal(0, 3)))
        riesgo_cardiovascular = category * 0.35 + np.random.random() * 0.3

        # Variable objetivo (glucosa en ayunas mg/dL)
        resultado = max(50, min(400, glucose_base + np.random.normal(0, 5)))

        # Ajustar peso según IMC y talla
        peso = imc * (talla / 100) ** 2

        return {
            'identificacion': 1000000 + patient_id,
            'fecha_registro': datetime.now().strftime('%Y-%m-%d'),

            # Características demográficas
            'edad': edad,
            'sexo': sexo,
            'zona_residencia': zona_residencia,
            'estrato': estrato,

            # Características antropométricas
            'talla': talla,
            'peso': peso,
            'imc': imc,
            'perimetro_abdominal': perimetro_abdominal,

            # Características clínicas
            'tas': tas,
            'tad': tad,
            'frecuencia_cardiaca': frecuencia_cardiaca,

            # Factores de riesgo
            'realiza_ejercicio': realiza_ejercicio,
            'consume_alcohol': consume_alcohol,
            'fuma': fuma,
            'medicamentos_hta': medicamentos_hta,

            # Antecedentes
            'historia_familiar_dm': historia_familiar_dm,
            'diabetes_gestacional': diabetes_gestacional,

            # Scores de riesgo
            'puntaje_findrisc': puntaje_findrisc,
            'riesgo_cardiovascular': riesgo_cardiovascular,

            # Variable objetivo
            'Resultado': resultado
        }

    def save_data(self, df: pd.DataFrame, filename: str = None) -> str:
        """
        Guarda el dataset generado en un archivo

        Args:
            df: DataFrame a guardar
            filename: Nombre del archivo (opcional)

        Returns:
            str: Ruta del archivo guardado
        """
        if filename is None:
            filename = config.get_timestamped_filename("diabetes_dataset", "csv")

        filepath = config.DATA_DIR / filename
        df.to_csv(filepath, index=False)

        print(f"💾 Dataset guardado en: {filepath}")
        return str(filepath)

def create_sample_dataset(n_samples: int = 1000) -> pd.DataFrame:
    """
    Función de conveniencia para crear un dataset de muestra

    Args:
        n_samples: Número de muestras a generar

    Returns:
        pd.DataFrame: Dataset generado
    """
    generator = DiabetesDataGenerator(n_samples=n_samples)
    return generator.generate_synthetic_data()

if __name__ == "__main__":
    # Ejemplo de uso
    generator = DiabetesDataGenerator(n_samples=500)
    df = generator.generate_synthetic_data()
    generator.save_data(df)

    print(f"\n📊 Información del dataset:")
    print(f"   Dimensiones: {df.shape}")
    print(f"   Columnas: {list(df.columns)}")
    print(f"   Tipos de datos:\n{df.dtypes.value_counts()}")