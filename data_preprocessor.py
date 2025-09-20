"""
Módulo de preprocesamiento de datos para el sistema de diabetes
"""
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, RobustScaler, MinMaxScaler
from sklearn.impute import SimpleImputer
from typing import Dict, List, Tuple, Optional
from config import config

class DiabetesDataPreprocessor:
    """
    Pipeline completo de preprocesamiento para datos de diabetes
    """

    def __init__(self):
        self.scaler = None
        self.imputer_numeric = None
        self.imputer_categorical = None
        self.feature_names = None
        self.encoded_columns = None

    def prepare_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Pipeline completo de preparación de datos

        Args:
            df: DataFrame con datos crudos

        Returns:
            pd.DataFrame: Datos procesados
        """
        df_processed = df.copy()

        # 1. Limpieza básica
        df_processed = self.clean_data(df_processed)

        # 2. Ingeniería de características
        df_processed = self.engineer_features(df_processed)

        # 3. Encoding de variables categóricas
        df_processed = self.encode_categorical(df_processed)

        # 4. Imputación de valores faltantes
        df_processed = self.impute_missing(df_processed)

        return df_processed

    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Limpieza de datos"""
        print("🧹 Limpiando datos...")

        # Eliminar duplicados
        initial_rows = len(df)
        df = df.drop_duplicates()

        if initial_rows > len(df):
            print(f"   Eliminados {initial_rows - len(df)} duplicados")

        # Eliminar columnas no útiles
        columns_to_drop = ['identificacion', 'fecha_registro']
        df = df.drop(columns=[col for col in columns_to_drop if col in df.columns])

        return df

    def engineer_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Crear nuevas características"""
        print("⚙️ Creando nuevas características...")

        # Presión arterial media
        if 'tas' in df.columns and 'tad' in df.columns:
            df['presion_arterial_media'] = (df['tas'] + 2 * df['tad']) / 3
            df['presion_pulso'] = df['tas'] - df['tad']

        # Ratios antropométricos
        if 'perimetro_abdominal' in df.columns and 'talla' in df.columns:
            df['ratio_cintura_altura'] = df['perimetro_abdominal'] / df['talla']

        # Categorización del IMC
        if 'imc' in df.columns:
            df['imc_categoria'] = pd.cut(df['imc'],
                                         bins=[0, 18.5, 25, 30, 35, 100],
                                         labels=[0, 1, 2, 3, 4]).astype(float)

        # Categorización de edad
        if 'edad' in df.columns:
            df['edad_categoria'] = pd.cut(df['edad'],
                                          bins=[0, 30, 45, 60, 75, 100],
                                          labels=[0, 1, 2, 3, 4]).astype(float)
            df['edad_squared'] = df['edad'] ** 2

        # Score de riesgo cardiovascular
        if all(col in df.columns for col in ['tas', 'imc', 'edad', 'fuma']):
            df['score_cv'] = (
                (df['tas'] - 120) / 20 +
                (df['imc'] - 25) / 5 +
                (df['edad'] - 40) / 20 +
                df['fuma'].map({'Si': 1, 'No': 0})
            )

        # Índice de salud (inverso del riesgo)
        if 'realiza_ejercicio' in df.columns:
            df['indice_salud'] = (
                df['realiza_ejercicio'].map({'Si': 1, 'No': 0}) * 2 -
                df.get('fuma', pd.Series([0]*len(df))).map({'Si': 1, 'No': 0})
            )

        print(f"   Creadas {len([col for col in df.columns if col not in ['Resultado']])} características")
        return df

    def encode_categorical(self, df: pd.DataFrame) -> pd.DataFrame:
        """Codificar variables categóricas"""
        print("🔢 Codificando variables categóricas...")

        categorical_columns = df.select_dtypes(include=['object']).columns
        categorical_columns = [col for col in categorical_columns if col != 'Resultado']

        for col in categorical_columns:
            if df[col].nunique() == 2:
                # Binary encoding
                df[col] = pd.get_dummies(df[col], drop_first=True).astype(float)
            elif df[col].nunique() <= 5:
                # One-hot encoding para pocas categorías
                dummies = pd.get_dummies(df[col], prefix=col, drop_first=False)
                df = pd.concat([df, dummies], axis=1)
                df = df.drop(col, axis=1)

        print(f"   Codificadas {len(categorical_columns)} variables categóricas")
        return df

    def impute_missing(self, df: pd.DataFrame) -> pd.DataFrame:
        """Imputar valores faltantes"""
        if df.isnull().sum().sum() > 0:
            print("🔧 Imputando valores faltantes...")

            numeric_cols = df.select_dtypes(include=[np.number]).columns

            for col in numeric_cols:
                if df[col].isnull().any():
                    df[col].fillna(df[col].median(), inplace=True)

        return df

    def scale_features(self, X_train: pd.DataFrame, X_test: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray]:
        """Escalar características"""
        print("📏 Escalando características...")

        self.scaler = StandardScaler()
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)

        return X_train_scaled, X_test_scaled

    def get_feature_names(self, df: pd.DataFrame) -> List[str]:
        """Obtener nombres de características después del preprocesamiento"""
        feature_columns = [col for col in df.columns if col != 'Resultado']
        return feature_columns

def preprocess_diabetes_data(df: pd.DataFrame) -> Tuple[pd.DataFrame, DiabetesDataPreprocessor]:
    """
    Función de conveniencia para preprocesar datos de diabetes

    Args:
        df: DataFrame con datos crudos

    Returns:
        Tuple[pd.DataFrame, DiabetesDataPreprocessor]: Datos procesados y preprocesador
    """
    preprocessor = DiabetesDataPreprocessor()
    df_processed = preprocessor.prepare_data(df)

    print(f"\n✅ Preprocesamiento completado:")
    print(f"   Dimensiones finales: {df_processed.shape}")
    print(f"   Características: {list(df_processed.columns)}")

    return df_processed, preprocessor

if __name__ == "__main__":
    # Ejemplo de uso
    from data_generator import create_sample_dataset

    print("🧪 Probando preprocesador...")

    # Generar datos de ejemplo
    df = create_sample_dataset(n_samples=100)

    # Preprocesar
    df_processed, preprocessor = preprocess_diabetes_data(df)

    print(f"\n📊 Resumen del preprocesamiento:")
    print(f"   Registros originales: {len(df)}")
    print(f"   Registros procesados: {len(df_processed)}")
    print(f"   Características originales: {len(df.columns)}")
    print(f"   Características finales: {len(df_processed.columns)}")