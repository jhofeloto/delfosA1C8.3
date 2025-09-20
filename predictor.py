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

class DiabetesPredictor:
    """Sistema de predicción de diabetes usando modelos entrenados"""

    def __init__(self, model_path: str = None, scaler_path: str = None):
        """
        Inicializar el predictor

        Args:
            model_path: Ruta al modelo (opcional, usa el mejor modelo por defecto)
            scaler_path: Ruta al scaler (opcional, busca automáticamente)
        """
        self.model = None
        self.scaler = None
        self.feature_columns = None
        self.metadata = None

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
            # Preparar features
            features = self._prepare_features(patient_data)

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

    def _prepare_features(self, patient_data: Dict[str, Any]) -> np.ndarray:
        """
        Preparar características del paciente para predicción

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
                "feature_columns": self.feature_columns
            }
        else:
            return {"error": "No se pudo cargar la información del modelo"}

def predict_glucose(patient_data: Dict[str, Any],
                   model_path: str = None) -> Dict[str, Any]:
    """
    Función de conveniencia para hacer predicciones

    Args:
        patient_data: Datos del paciente
        model_path: Ruta al modelo (opcional)

    Returns:
        Dict: Resultado de la predicción
    """
    predictor = DiabetesPredictor(model_path=model_path)
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