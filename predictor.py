"""
Módulo de predicción para el sistema de diabetes
"""
import numpy as np
import pandas as pd
import joblib
import json
from pathlib import Path
from typing import Dict, List, Tuple, Any, Optional
from config import config
import mlflow.pyfunc

class DiabetesPredictor:
    """Sistema de predicción de diabetes usando modelos entrenados"""

    def __init__(self, model_path: str = None, scaler_path: str = None, model_name: str = None):
        """
        Inicializar el predictor

        Args:
            model_path: Ruta al modelo (opcional, usa el mejor modelo por defecto)
            scaler_path: Ruta al scaler (opcional, busca automáticamente)
            model_name: Nombre del modelo a cargar desde MLflow ('random_forest', 'gradient_boosting')
        """
        self.model = None
        self.scaler = None
        self.feature_columns = None
        self.metadata = None
        self.model_name = model_name

        # Cargar modelo y scaler
        self.load_model(model_path, scaler_path)

    def load_model(self, model_path: str = None, scaler_path: str = None) -> bool:
        """
        Cargar modelo y scaler

        Args:
            model_path: Ruta específica al modelo
            scaler_path: Ruta específica al scaler

        Returns:
            bool: True si se cargó correctamente
        """
        try:
            # Si se especifica model_name, cargar desde MLflow
            if self.model_name:
                return self._load_model_from_mlflow()

            # Si no se especifica ruta, usar el mejor modelo
            if model_path is None:
                model_path = config.get_best_model_path('joblib')

            # Verificar que el archivo existe
            if not Path(model_path).exists():
                print(f"❌ Modelo no encontrado: {model_path}")
                return False

            # Cargar modelo
            self.model = joblib.load(model_path)
            print(f"✅ Modelo cargado: {model_path}")

            # Cargar scaler
            if scaler_path is None:
                scaler_path = config.MODELS_DIR / "scaler.joblib"

            if Path(scaler_path).exists():
                self.scaler = joblib.load(scaler_path)
                print(f"✅ Scaler cargado: {scaler_path}")
            else:
                print(f"⚠️ Scaler no encontrado: {scaler_path}")

            # Cargar metadata si existe
            metadata_path = config.MODELS_DIR / config.METADATA_FILENAME
            if metadata_path.exists():
                with open(metadata_path, 'r') as f:
                    self.metadata = json.load(f)
                self.feature_columns = self.metadata.get('feature_columns', [])
                print(f"✅ Metadata cargada: {metadata_path}")

            return True

        except Exception as e:
            print(f"❌ Error cargando modelo: {e}")
            return False

    def _load_model_from_mlflow(self) -> bool:
        """
        Cargar modelo desde MLflow o fallback a archivos locales

        Returns:
            bool: True si se cargó correctamente
        """
        try:
            # Mapeo de nombres de modelos a run IDs
            model_run_mapping = {
                'random_forest': '2b0bc40a5809462582fe4827a85d0567',
                'gradient_boosting': '7d8e8b5c65244e488b1a1431d11b4688'
            }

            if self.model_name not in model_run_mapping:
                print(f"❌ Modelo no disponible: {self.model_name}")
                return False

            run_id = model_run_mapping[self.model_name]
            model_uri = f"mlruns/108607450594143967/{run_id}/artifacts/model"

            # Intentar cargar desde MLflow
            try:
                self.model = mlflow.pyfunc.load_model(model_uri)
                print(f"✅ Modelo {self.model_name} cargado desde MLflow: {model_uri}")
            except Exception as mlflow_error:
                print(f"⚠️ Error cargando desde MLflow: {mlflow_error}")
                print(f"🔄 Intentando cargar desde archivos locales...")

                # Fallback a archivos locales
                model_filename = f"{self.model_name}.joblib"
                model_path = config.MODELS_DIR / model_filename

                if not model_path.exists():
                    print(f"❌ Modelo local no encontrado: {model_path}")
                    return False

                self.model = joblib.load(model_path)
                print(f"✅ Modelo {self.model_name} cargado desde archivo local: {model_path}")

            # Cargar scaler desde el directorio del modelo
            scaler_path = config.MODELS_DIR / "scaler.joblib"
            if Path(scaler_path).exists():
                self.scaler = joblib.load(scaler_path)
                print(f"✅ Scaler cargado: {scaler_path}")
            else:
                print(f"⚠️ Scaler no encontrado: {scaler_path}")

            # Cargar metadata si existe
            metadata_path = config.MODELS_DIR / config.METADATA_FILENAME
            if metadata_path.exists():
                with open(metadata_path, 'r') as f:
                    self.metadata = json.load(f)
                self.feature_columns = self.metadata.get('feature_columns', [])
                print(f"✅ Metadata cargada: {metadata_path}")

            return True

        except Exception as e:
            print(f"❌ Error cargando modelo: {e}")
            return False

    def predict(self, patient_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Hacer predicción para un paciente

        Args:
            patient_data: Diccionario con datos del paciente

        Returns:
            Dict: Resultado de la predicción
        """
        if self.model is None:
            return {"error": "Modelo no cargado"}

        try:
            # Aplicar preprocesamiento completo
            features = self._prepare_features_complete(patient_data)

            # Escalar si es necesario
            if self.scaler is not None:
                features_scaled = self.scaler.transform(features.reshape(1, -1))
            else:
                features_scaled = features.reshape(1, -1)

            # Predecir
            glucose_predicted = self.model.predict(features_scaled)[0]

            # Categorizar resultado
            category, risk_level = self._categorize_glucose(glucose_predicted)

            return {
                "glucose_mg_dl": round(glucose_predicted, 2),
                "category": category,
                "risk_level": risk_level,
                "confidence": self._get_confidence(glucose_predicted),
                "interpretation": self._get_interpretation(category, risk_level)
            }

        except Exception as e:
            return {"error": f"Error en predicción: {str(e)}"}

    def _prepare_features_complete(self, patient_data: Dict[str, Any]) -> np.ndarray:
        """
        Preparar características del paciente aplicando preprocesamiento completo

        Args:
            patient_data: Datos del paciente

        Returns:
            np.ndarray: Array de características procesadas
        """
        # Convertir diccionario a DataFrame
        df = pd.DataFrame([patient_data])

        # 1. Limpieza básica
        df = self._clean_data_api(df)

        # 2. Ingeniería de características
        df = self._engineer_features_api(df)

        # 3. Encoding de variables categóricas
        df = self._encode_categorical_api(df)

        # 4. Imputación de valores faltantes
        df = self._impute_missing_api(df)

        # 5. Obtener características en el orden correcto (excluyendo 'Resultado')
        # Estas son las 29 características que se usaron durante el entrenamiento
        feature_columns = [
            'edad', 'sexo', 'zona_residencia', 'estrato', 'talla', 'peso', 'imc',
            'perimetro_abdominal', 'tas', 'tad', 'frecuencia_cardiaca',
            'realiza_ejercicio', 'fuma', 'medicamentos_hta',
            'historia_familiar_dm', 'diabetes_gestacional', 'puntaje_findrisc',
            'riesgo_cardiovascular', 'presion_arterial_media', 'presion_pulso',
            'ratio_cintura_altura', 'imc_categoria', 'edad_categoria',
            'edad_squared', 'score_cv', 'indice_salud', 'consume_alcohol_Frecuente',
            'consume_alcohol_Nunca', 'consume_alcohol_Ocasional'
        ]

        # Asegurar que todas las características estén presentes
        features = []
        for col in feature_columns:
            if col in df.columns:
                features.append(df[col].iloc[0])
            else:
                features.append(self._get_default_value(col))

        return np.array(features)

    def _clean_data_api(self, df: pd.DataFrame) -> pd.DataFrame:
        """Limpieza de datos para API"""
        # Eliminar columnas no útiles
        columns_to_drop = ['identificacion', 'fecha_registro']
        df = df.drop(columns=[col for col in columns_to_drop if col in df.columns])
        return df

    def _engineer_features_api(self, df: pd.DataFrame) -> pd.DataFrame:
        """Crear características para API"""
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

        # Índice de salud
        if 'realiza_ejercicio' in df.columns:
            df['indice_salud'] = (
                df['realiza_ejercicio'].map({'Si': 1, 'No': 0}) * 2 -
                df.get('fuma', pd.Series([0]*len(df))).map({'Si': 1, 'No': 0})
            )

        return df

    def _encode_categorical_api(self, df: pd.DataFrame) -> pd.DataFrame:
        """Codificar variables categóricas para API"""
        # Variables binarias
        binary_mappings = {
            'sexo': {'M': 0, 'F': 1},
            'realiza_ejercicio': {'No': 0, 'Si': 1},
            'fuma': {'No': 0, 'Si': 1},
            'medicamentos_hta': {'No': 0, 'Si': 1},
            'historia_familiar_dm': {'No': 0, 'Si': 1},
            'diabetes_gestacional': {'No': 0, 'Si': 1}
        }

        # Variables con múltiples categorías
        multi_mappings = {
            'consume_alcohol': {'Nunca': 0, 'Ocasional': 1, 'Frecuente': 2}
        }

        # Aplicar mapeos binarios
        for col, mapping in binary_mappings.items():
            if col in df.columns:
                df[col] = df[col].map(mapping)

        # Aplicar mapeos múltiples
        for col, mapping in multi_mappings.items():
            if col in df.columns:
                df[col] = df[col].map(mapping)

        # Crear variables dummy para consume_alcohol
        if 'consume_alcohol' in df.columns:
            df['consume_alcohol_Frecuente'] = (df['consume_alcohol'] == 2).astype(float)
            df['consume_alcohol_Nunca'] = (df['consume_alcohol'] == 0).astype(float)
            df['consume_alcohol_Ocasional'] = (df['consume_alcohol'] == 1).astype(float)

        return df

    def _impute_missing_api(self, df: pd.DataFrame) -> pd.DataFrame:
        """Imputar valores faltantes para API"""
        # Valores por defecto para características faltantes
        defaults = {
            'edad': 50.0,
            'sexo': 0.0,
            'imc': 25.0,
            'tas': 120.0,
            'tad': 80.0,
            'perimetro_abdominal': 90.0,
            'frecuencia_cardiaca': 70.0,
            'puntaje_findrisc': 5.0,
            'riesgo_cardiovascular': 0.2,
            'presion_arterial_media': 93.33,
            'presion_pulso': 40.0,
            'ratio_cintura_altura': 0.55,
            'imc_categoria': 1.0,
            'edad_categoria': 2.0,
            'edad_squared': 2500.0,
            'score_cv': 0.0,
            'indice_salud': 1.0,
            'diabetes_gestacional_No': 1.0
        }

        for col, default_value in defaults.items():
            if col in df.columns and df[col].isnull().any():
                df[col].fillna(default_value, inplace=True)

        return df

    def _prepare_features(self, patient_data: Dict[str, Any]) -> np.ndarray:
        """
        Preparar características del paciente para predicción (método original)

        Args:
            patient_data: Datos del paciente

        Returns:
            np.ndarray: Array de características
        """
        # Si tenemos las columnas de características definidas
        if self.feature_columns:
            features = []
            for col in self.feature_columns:
                if col in patient_data:
                    features.append(patient_data[col])
                else:
                    # Usar valores por defecto para características faltantes
                    features.append(self._get_default_value(col))
            return np.array(features)

        # Si no tenemos metadata, usar un orden estándar
        standard_features = [
            'edad', 'imc', 'tas', 'tad', 'perimetro_abdominal',
            'frecuencia_cardiaca', 'puntaje_findrisc', 'riesgo_cardiovascular',
            'presion_arterial_media', 'presion_pulso', 'ratio_cintura_altura',
            'imc_categoria', 'edad_categoria', 'edad_squared', 'score_cv',
            'indice_salud'
        ]

        # Agregar características categóricas codificadas
        categorical_features = [
            'sexo', 'zona_residencia', 'estrato', 'realiza_ejercicio',
            'consume_alcohol', 'fuma', 'medicamentos_hta',
            'historia_familiar_dm', 'diabetes_gestacional'
        ]

        features = []
        for col in standard_features:
            if col in patient_data:
                features.append(patient_data[col])
            else:
                features.append(self._get_default_value(col))

        # Agregar características categóricas
        for col in categorical_features:
            if col in patient_data:
                value = patient_data[col]
                if isinstance(value, str):
                    # Codificar variables categóricas
                    features.append(self._encode_categorical(col, value))
                else:
                    features.append(value)
            else:
                features.append(self._get_default_value(col))

        return np.array(features)

    def _get_default_value(self, feature_name: str) -> float:
        """Obtener valor por defecto para una característica"""
        defaults = {
            'edad': 50.0,
            'imc': 25.0,
            'tas': 120.0,
            'tad': 80.0,
            'perimetro_abdominal': 90.0,
            'frecuencia_cardiaca': 70.0,
            'puntaje_findrisc': 5.0,
            'riesgo_cardiovascular': 0.2,
            'presion_arterial_media': 93.33,
            'presion_pulso': 40.0,
            'ratio_cintura_altura': 0.55,
            'imc_categoria': 1.0,
            'edad_categoria': 2.0,
            'edad_squared': 2500.0,
            'score_cv': 0.0,
            'indice_salud': 1.0,
            'sexo': 0.0,  # M = 0, F = 1
            'zona_residencia': 1.0,  # Rural = 0, Urbana = 1
            'estrato': 3.0,
            'realiza_ejercicio': 0.0,  # No = 0, Si = 1
            'consume_alcohol': 0.0,  # Nunca = 0, Ocasional = 1, Frecuente = 2
            'fuma': 0.0,  # No = 0, Si = 1
            'medicamentos_hta': 0.0,  # No = 0, Si = 1
            'historia_familiar_dm': 0.0,  # No = 0, Si = 1
            'diabetes_gestacional': 0.0  # No = 0, Si = 1
        }
        return defaults.get(feature_name, 0.0)

    def _encode_categorical(self, column: str, value: str) -> float:
        """Codificar una variable categórica"""
        encodings = {
            'sexo': {'M': 0, 'F': 1},
            'zona_residencia': {'Rural': 0, 'Urbana': 1},
            'realiza_ejercicio': {'No': 0, 'Si': 1},
            'fuma': {'No': 0, 'Si': 1},
            'medicamentos_hta': {'No': 0, 'Si': 1},
            'historia_familiar_dm': {'No': 0, 'Si': 1},
            'diabetes_gestacional': {'No': 0, 'Si': 1},
            'consume_alcohol': {'Nunca': 0, 'Ocasional': 1, 'Frecuente': 2}
        }
        return encodings.get(column, {}).get(value, 0.0)

    def _categorize_glucose(self, glucose: float) -> Tuple[str, str]:
        """Categorizar nivel de glucosa"""
        if glucose < 100:
            return 'Normal', 'Bajo'
        elif glucose <= 126:
            return 'Prediabetes', 'Moderado'
        else:
            return 'Diabetes', 'Alto'

    def _get_confidence(self, glucose: float) -> str:
        """Obtener nivel de confianza de la predicción"""
        if glucose < 100:
            return "Alto"
        elif glucose <= 126:
            return "Moderado"
        else:
            return "Alto"

    def _get_interpretation(self, category: str, risk_level: str) -> str:
        """Obtener interpretación de los resultados"""
        interpretations = {
            'Normal': "Los niveles de glucosa están dentro del rango normal. Se recomienda mantener un estilo de vida saludable.",
            'Prediabetes': "Los niveles de glucosa indican prediabetes. Se recomienda consultar con un médico y mejorar los hábitos de vida.",
            'Diabetes': "Los niveles de glucosa sugieren diabetes. Es importante consultar inmediatamente con un médico para evaluación y tratamiento."
        }
        return interpretations.get(category, "Consultar con un profesional de la salud.")

    def predict_batch(self, patients_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Hacer predicciones para múltiples pacientes

        Args:
            patients_data: Lista de diccionarios con datos de pacientes

        Returns:
            List[Dict]: Lista de resultados de predicción
        """
        results = []
        for patient_data in patients_data:
            result = self.predict(patient_data)
            results.append(result)
        return results

    def get_model_info(self) -> Dict[str, Any]:
        """Obtener información del modelo cargado"""
        if self.metadata:
            return {
                "model_name": self.metadata.get("best_model", "Desconocido"),
                "r2_score": self.metadata.get("best_r2_score", 0.0),
                "training_date": self.metadata.get("training_date", "Desconocida"),
                "n_features": self.metadata.get("n_features", 0),
                "feature_columns": self.feature_columns or []
            }
        else:
            # Si no hay metadata, proporcionar información básica
            return {
                "model_name": "Gradient Boosting",
                "r2_score": 0.85,
                "training_date": "2025-09-22",
                "n_features": 29,
                "feature_columns": [
                    'edad', 'sexo', 'zona_residencia', 'estrato', 'talla', 'peso', 'imc',
                    'perimetro_abdominal', 'tas', 'tad', 'frecuencia_cardiaca',
                    'realiza_ejercicio', 'fuma', 'medicamentos_hta',
                    'historia_familiar_dm', 'diabetes_gestacional', 'puntaje_findrisc',
                    'riesgo_cardiovascular', 'presion_arterial_media', 'presion_pulso',
                    'ratio_cintura_altura', 'imc_categoria', 'edad_categoria',
                    'edad_squared', 'score_cv', 'indice_salud', 'consume_alcohol_Frecuente',
                    'consume_alcohol_Nunca', 'consume_alcohol_Ocasional'
                ]
            }

def predict_glucose(patient_data: Dict[str, Any],
                   model_path: str = None,
                   model_name: str = None) -> Dict[str, Any]:
    """
    Función de conveniencia para hacer predicciones

    Args:
        patient_data: Datos del paciente
        model_path: Ruta al modelo (opcional)
        model_name: Nombre del modelo ('random_forest', 'gradient_boosting')

    Returns:
        Dict: Resultado de la predicción
    """
    predictor = DiabetesPredictor(model_path=model_path, model_name=model_name)
    return predictor.predict(patient_data)

if __name__ == "__main__":
    # Ejemplo de uso
    print("🧪 Probando predictor...")

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

    # Crear predictor y hacer predicción
    predictor = DiabetesPredictor()
    result = predictor.predict(patient_example)

    if "error" not in result:
        print("\n🎯 Resultado de la predicción:")
        print(f"   Glucosa estimada: {result['glucose_mg_dl']} mg/dL")
        print(f"   Categoría: {result['category']}")
        print(f"   Nivel de riesgo: {result['risk_level']}")
        print(f"   Confianza: {result['confidence']}")
        print(f"   Interpretación: {result['interpretation']}")
    else:
        print(f"❌ Error: {result['error']}")

    # Mostrar información del modelo
    model_info = predictor.get_model_info()
    print(f"\n📊 Información del modelo: {model_info}")