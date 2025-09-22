"""
Gestor de Base de Datos para el Sistema Predictivo de Diabetes
Implementación con SQLAlchemy para integración con bases de datos médicas
"""
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.sql import func
from sqlalchemy.exc import SQLAlchemyError
from typing import Dict, List, Any, Optional, Tuple
import pandas as pd
import numpy as np
from datetime import datetime
import logging
import json
from pathlib import Path

from config import config

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Base = declarative_base()

class Patient(Base):
    """Modelo de paciente"""
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(String, unique=True, index=True, nullable=False)
    edad = Column(Float, nullable=False)
    sexo = Column(String(1), nullable=False)  # M o F
    zona_residencia = Column(String(50))
    estrato = Column(Integer)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

class MedicalData(Base):
    """Datos médicos del paciente"""
    __tablename__ = "medical_data"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(String, index=True, nullable=False)
    talla = Column(Float)  # cm
    peso = Column(Float)  # kg
    imc = Column(Float)
    tas = Column(Float)  # Tensión arterial sistólica
    tad = Column(Float)  # Tensión arterial diastólica
    perimetro_abdominal = Column(Float)  # cm
    frecuencia_cardiaca = Column(Float)
    realiza_ejercicio = Column(Boolean)
    consume_alcohol = Column(String(20))
    fuma = Column(Boolean)
    medicamentos_hta = Column(Boolean)
    historia_familiar_dm = Column(Boolean)
    diabetes_gestacional = Column(Boolean)
    puntaje_findrisc = Column(Float)
    riesgo_cardiovascular = Column(Float)
    recorded_at = Column(DateTime, default=func.now())

class Prediction(Base):
    """Predicciones realizadas"""
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(String, index=True, nullable=False)
    glucose_predicted = Column(Float, nullable=False)
    category = Column(String(20), nullable=False)  # Normal, Prediabetes, Diabetes
    risk_level = Column(String(20), nullable=False)  # Bajo, Moderado, Alto
    confidence = Column(String(20))
    model_version = Column(String(50))
    processing_time_ms = Column(Float)
    predicted_at = Column(DateTime, default=func.now())

    # Información adicional
    input_data = Column(Text)  # JSON con datos de entrada
    model_info = Column(Text)  # JSON con información del modelo

class ModelPerformance(Base):
    """Rendimiento de modelos"""
    __tablename__ = "model_performance"

    id = Column(Integer, primary_key=True, index=True)
    model_name = Column(String(100), nullable=False)
    model_version = Column(String(50))
    r2_score = Column(Float)
    rmse = Column(Float)
    mae = Column(Float)
    training_date = Column(DateTime)
    n_samples = Column(Integer)
    performance_data = Column(Text)  # JSON con métricas detalladas
    recorded_at = Column(DateTime, default=func.now())

class DatabaseManager:
    """Gestor de base de datos para el sistema predictivo"""

    def __init__(self, database_url: Optional[str] = None):
        """
        Inicializar gestor de base de datos

        Args:
            database_url: URL de conexión a la base de datos
                         Si es None, usa SQLite local
        """
        if database_url is None:
            # Crear directorio de datos si no existe
            config.DATA_DIR.mkdir(exist_ok=True)
            db_path = config.DATA_DIR / "diabetes_medical.db"
            database_url = f"sqlite:///{db_path}"

        self.database_url = database_url
        self.engine = create_engine(database_url, echo=False)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

        # Crear tablas
        self._create_tables()

        logger.info(f"✅ Base de datos configurada: {database_url}")

    def _create_tables(self):
        """Crear tablas en la base de datos"""
        try:
            Base.metadata.create_all(bind=self.engine)
            logger.info("✅ Tablas creadas/verficadas en la base de datos")
        except Exception as e:
            logger.error(f"❌ Error creando tablas: {e}")

    def get_session(self) -> Session:
        """Obtener sesión de base de datos"""
        return self.SessionLocal()

    def save_patient(self, patient_data: Dict[str, Any]) -> str:
        """
        Guardar información de paciente

        Args:
            patient_data: Diccionario con datos del paciente

        Returns:
            str: ID del paciente guardado
        """
        session = self.get_session()

        try:
            # Crear paciente
            patient = Patient(
                patient_id=patient_data.get('patient_id', f"PAT_{datetime.now().strftime('%Y%m%d_%H%M%S')}"),
                edad=patient_data['edad'],
                sexo=patient_data['sexo'],
                zona_residencia=patient_data.get('zona_residencia'),
                estrato=patient_data.get('estrato')
            )

            session.add(patient)
            session.flush()  # Para obtener el ID

            # Crear datos médicos
            medical_data = MedicalData(
                patient_id=patient.patient_id,
                talla=patient_data.get('talla'),
                peso=patient_data.get('peso'),
                imc=patient_data.get('imc'),
                tas=patient_data.get('tas'),
                tad=patient_data.get('tad'),
                perimetro_abdominal=patient_data.get('perimetro_abdominal'),
                frecuencia_cardiaca=patient_data.get('frecuencia_cardiaca'),
                realiza_ejercicio=patient_data.get('realiza_ejercicio') == 'Si',
                consume_alcohol=patient_data.get('consume_alcohol'),
                fuma=patient_data.get('fuma') == 'Si',
                medicamentos_hta=patient_data.get('medicamentos_hta') == 'Si',
                historia_familiar_dm=patient_data.get('historia_familiar_dm') == 'Si',
                diabetes_gestacional=patient_data.get('diabetes_gestacional') == 'Si',
                puntaje_findrisc=patient_data.get('puntaje_findrisc'),
                riesgo_cardiovascular=patient_data.get('riesgo_cardiovascular')
            )

            session.add(medical_data)
            session.commit()

            patient_id = patient.patient_id
            logger.info(f"✅ Paciente guardado: {patient_id}")

            return patient_id

        except SQLAlchemyError as e:
            session.rollback()
            logger.error(f"❌ Error guardando paciente: {e}")
            raise
        finally:
            session.close()

    def save_prediction(self, patient_id: str, prediction_data: Dict[str, Any],
                       input_data: Dict[str, Any], model_info: Optional[Dict[str, Any]] = None) -> int:
        """
        Guardar predicción realizada

        Args:
            patient_id: ID del paciente
            prediction_data: Datos de la predicción
            input_data: Datos de entrada utilizados
            model_info: Información del modelo usado

        Returns:
            int: ID de la predicción guardada
        """
        session = self.get_session()

        try:
            prediction = Prediction(
                patient_id=patient_id,
                glucose_predicted=prediction_data['glucose_mg_dl'],
                category=prediction_data['category'],
                risk_level=prediction_data['risk_level'],
                confidence=prediction_data.get('confidence', 'Desconocido'),
                model_version=prediction_data.get('model_version', '1.0.0'),
                processing_time_ms=prediction_data.get('processing_time_ms'),
                input_data=json.dumps(input_data),
                model_info=json.dumps(model_info) if model_info else None
            )

            session.add(prediction)
            session.commit()

            prediction_id = prediction.id
            logger.info(f"✅ Predicción guardada: {prediction_id} para paciente {patient_id}")

            return prediction_id

        except SQLAlchemyError as e:
            session.rollback()
            logger.error(f"❌ Error guardando predicción: {e}")
            raise
        finally:
            session.close()

    def save_model_performance(self, model_name: str, model_version: str,
                             performance_data: Dict[str, Any]) -> int:
        """
        Guardar rendimiento de un modelo

        Args:
            model_name: Nombre del modelo
            model_version: Versión del modelo
            performance_data: Métricas de rendimiento

        Returns:
            int: ID del registro guardado
        """
        session = self.get_session()

        try:
            performance = ModelPerformance(
                model_name=model_name,
                model_version=model_version,
                r2_score=performance_data.get('r2_score'),
                rmse=performance_data.get('rmse'),
                mae=performance_data.get('mae'),
                training_date=performance_data.get('training_date'),
                n_samples=performance_data.get('n_samples'),
                performance_data=json.dumps(performance_data)
            )

            session.add(performance)
            session.commit()

            performance_id = performance.id
            logger.info(f"✅ Rendimiento de modelo guardado: {model_name} v{model_version}")

            return performance_id

        except SQLAlchemyError as e:
            session.rollback()
            logger.error(f"❌ Error guardando rendimiento de modelo: {e}")
            raise
        finally:
            session.close()

    def get_patient_history(self, patient_id: str) -> Dict[str, Any]:
        """
        Obtener historial de un paciente

        Args:
            patient_id: ID del paciente

        Returns:
            Dict: Historial del paciente
        """
        session = self.get_session()

        try:
            # Obtener paciente
            patient = session.query(Patient).filter(Patient.patient_id == patient_id).first()

            if not patient:
                return {"error": f"Paciente {patient_id} no encontrado"}

            # Obtener datos médicos
            medical_data = session.query(MedicalData).filter(
                MedicalData.patient_id == patient_id
            ).order_by(MedicalData.recorded_at.desc()).all()

            # Obtener predicciones
            predictions = session.query(Prediction).filter(
                Prediction.patient_id == patient_id
            ).order_by(Prediction.predicted_at.desc()).all()

            return {
                "patient_info": {
                    "patient_id": patient.patient_id,
                    "edad": patient.edad,
                    "sexo": patient.sexo,
                    "zona_residencia": patient.zona_residencia,
                    "estrato": patient.estrato,
                    "created_at": patient.created_at.isoformat(),
                    "updated_at": patient.updated_at.isoformat()
                },
                "medical_data": [
                    {
                        "recorded_at": data.recorded_at.isoformat(),
                        "talla": data.talla,
                        "peso": data.peso,
                        "imc": data.imc,
                        "tas": data.tas,
                        "tad": data.tad,
                        "perimetro_abdominal": data.perimetro_abdominal,
                        "frecuencia_cardiaca": data.frecuencia_cardiaca,
                        "realiza_ejercicio": data.realiza_ejercicio,
                        "consume_alcohol": data.consume_alcohol,
                        "fuma": data.fuma,
                        "medicamentos_hta": data.medicamentos_hta,
                        "historia_familiar_dm": data.historia_familiar_dm,
                        "diabetes_gestacional": data.diabetes_gestacional,
                        "puntaje_findrisc": data.puntaje_findrisc,
                        "riesgo_cardiovascular": data.riesgo_cardiovascular
                    }
                    for data in medical_data
                ],
                "predictions": [
                    {
                        "predicted_at": pred.predicted_at.isoformat(),
                        "glucose_predicted": pred.glucose_predicted,
                        "category": pred.category,
                        "risk_level": pred.risk_level,
                        "confidence": pred.confidence,
                        "model_version": pred.model_version,
                        "processing_time_ms": pred.processing_time_ms
                    }
                    for pred in predictions
                ]
            }

        except SQLAlchemyError as e:
            logger.error(f"❌ Error obteniendo historial del paciente: {e}")
            return {"error": str(e)}
        finally:
            session.close()

    def get_predictions_summary(self, limit: int = 100) -> Dict[str, Any]:
        """
        Obtener resumen de predicciones

        Args:
            limit: Número máximo de registros a obtener

        Returns:
            Dict: Resumen de predicciones
        """
        session = self.get_session()

        try:
            # Obtener estadísticas generales
            total_predictions = session.query(func.count(Prediction.id)).scalar()

            # Distribución por categoría
            category_stats = session.query(
                Prediction.category,
                func.count(Prediction.id).label('count')
            ).group_by(Prediction.category).all()

            # Promedio de glucosa por categoría
            glucose_stats = session.query(
                Prediction.category,
                func.avg(Prediction.glucose_predicted).label('avg_glucose'),
                func.min(Prediction.glucose_predicted).label('min_glucose'),
                func.max(Prediction.glucose_predicted).label('max_glucose')
            ).group_by(Prediction.category).all()

            # Predicciones recientes
            recent_predictions = session.query(Prediction).order_by(
                Prediction.predicted_at.desc()
            ).limit(limit).all()

            return {
                "total_predictions": total_predictions,
                "category_distribution": [
                    {"category": cat, "count": count}
                    for cat, count in category_stats
                ],
                "glucose_by_category": [
                    {
                        "category": cat,
                        "avg_glucose": float(avg_glucose),
                        "min_glucose": float(min_glucose),
                        "max_glucose": float(max_glucose)
                    }
                    for cat, avg_glucose, min_glucose, max_glucose in glucose_stats
                ],
                "recent_predictions": [
                    {
                        "patient_id": pred.patient_id,
                        "glucose_predicted": pred.glucose_predicted,
                        "category": pred.category,
                        "risk_level": pred.risk_level,
                        "predicted_at": pred.predicted_at.isoformat()
                    }
                    for pred in recent_predictions
                ]
            }

        except SQLAlchemyError as e:
            logger.error(f"❌ Error obteniendo resumen de predicciones: {e}")
            return {"error": str(e)}
        finally:
            session.close()

    def export_data_to_csv(self, output_dir: Optional[str] = None) -> Dict[str, str]:
        """
        Exportar datos a archivos CSV

        Args:
            output_dir: Directorio de salida (opcional)

        Returns:
            Dict: Rutas de archivos exportados
        """
        if output_dir is None:
            output_dir = config.OUTPUTS_DIR
        else:
            output_dir = Path(output_dir)
            output_dir.mkdir(exist_ok=True)

        session = self.get_session()
        exported_files = {}

        try:
            # Exportar pacientes
            patients = session.query(Patient).all()
            if patients:
                patients_df = pd.DataFrame([
                    {
                        "patient_id": p.patient_id,
                        "edad": p.edad,
                        "sexo": p.sexo,
                        "zona_residencia": p.zona_residencia,
                        "estrato": p.estrato,
                        "created_at": p.created_at,
                        "updated_at": p.updated_at
                    }
                    for p in patients
                ])
                patients_file = output_dir / "patients.csv"
                patients_df.to_csv(patients_file, index=False)
                exported_files["patients"] = str(patients_file)

            # Exportar datos médicos
            medical_data = session.query(MedicalData).all()
            if medical_data:
                medical_df = pd.DataFrame([
                    {
                        "patient_id": m.patient_id,
                        "talla": m.talla,
                        "peso": m.peso,
                        "imc": m.imc,
                        "tas": m.tas,
                        "tad": m.tad,
                        "perimetro_abdominal": m.perimetro_abdominal,
                        "frecuencia_cardiaca": m.frecuencia_cardiaca,
                        "realiza_ejercicio": m.realiza_ejercicio,
                        "consume_alcohol": m.consume_alcohol,
                        "fuma": m.fuma,
                        "medicamentos_hta": m.medicamentos_hta,
                        "historia_familiar_dm": m.historia_familiar_dm,
                        "diabetes_gestacional": m.diabetes_gestacional,
                        "puntaje_findrisc": m.puntaje_findrisc,
                        "riesgo_cardiovascular": m.riesgo_cardiovascular,
                        "recorded_at": m.recorded_at
                    }
                    for m in medical_data
                ])
                medical_file = output_dir / "medical_data.csv"
                medical_df.to_csv(medical_file, index=False)
                exported_files["medical_data"] = str(medical_file)

            # Exportar predicciones
            predictions = session.query(Prediction).all()
            if predictions:
                predictions_df = pd.DataFrame([
                    {
                        "patient_id": p.patient_id,
                        "glucose_predicted": p.glucose_predicted,
                        "category": p.category,
                        "risk_level": p.risk_level,
                        "confidence": p.confidence,
                        "model_version": p.model_version,
                        "processing_time_ms": p.processing_time_ms,
                        "predicted_at": p.predicted_at
                    }
                    for p in predictions
                ])
                predictions_file = output_dir / "predictions.csv"
                predictions_df.to_csv(predictions_file, index=False)
                exported_files["predictions"] = str(predictions_file)

            logger.info(f"✅ Datos exportados a {len(exported_files)} archivos")
            return exported_files

        except SQLAlchemyError as e:
            logger.error(f"❌ Error exportando datos: {e}")
            return {"error": str(e)}
        finally:
            session.close()

    def get_database_stats(self) -> Dict[str, Any]:
        """Obtener estadísticas de la base de datos"""
        session = self.get_session()

        try:
            stats = {}

            # Estadísticas de pacientes
            patient_count = session.query(func.count(Patient.id)).scalar()
            stats["total_patients"] = patient_count

            if patient_count > 0:
                age_stats = session.query(
                    func.avg(Patient.edad),
                    func.min(Patient.edad),
                    func.max(Patient.edad)
                ).first()
                stats["avg_age"] = float(age_stats[0])
                stats["min_age"] = float(age_stats[1])
                stats["max_age"] = float(age_stats[2])

                gender_dist = session.query(
                    Patient.sexo,
                    func.count(Patient.id)
                ).group_by(Patient.sexo).all()
                stats["gender_distribution"] = {sex: count for sex, count in gender_dist}

            # Estadísticas de datos médicos
            medical_count = session.query(func.count(MedicalData.id)).scalar()
            stats["total_medical_records"] = medical_count

            # Estadísticas de predicciones
            prediction_count = session.query(func.count(Prediction.id)).scalar()
            stats["total_predictions"] = prediction_count

            if prediction_count > 0:
                category_dist = session.query(
                    Prediction.category,
                    func.count(Prediction.id)
                ).group_by(Prediction.category).all()
                stats["prediction_categories"] = {cat: count for cat, count in category_dist}

                glucose_stats = session.query(
                    func.avg(Prediction.glucose_predicted),
                    func.min(Prediction.glucose_predicted),
                    func.max(Prediction.glucose_predicted)
                ).first()
                stats["avg_predicted_glucose"] = float(glucose_stats[0])
                stats["min_predicted_glucose"] = float(glucose_stats[1])
                stats["max_predicted_glucose"] = float(glucose_stats[2])

            # Estadísticas de rendimiento de modelos
            performance_count = session.query(func.count(ModelPerformance.id)).scalar()
            stats["total_model_performances"] = performance_count

            return stats

        except SQLAlchemyError as e:
            logger.error(f"❌ Error obteniendo estadísticas: {e}")
            return {"error": str(e)}
        finally:
            session.close()

def create_database_manager(database_url: Optional[str] = None) -> DatabaseManager:
    """
    Función de conveniencia para crear gestor de base de datos

    Args:
        database_url: URL de conexión a la base de datos

    Returns:
        DatabaseManager: Instancia configurada
    """
    return DatabaseManager(database_url)

if __name__ == "__main__":
    # Ejemplo de uso
    logger.info("🧪 Probando gestor de base de datos...")

    # Crear gestor
    db_manager = create_database_manager()

    # Datos de ejemplo
    patient_data = {
        'patient_id': 'TEST_001',
        'edad': 45,
        'sexo': 'M',
        'imc': 25.5,
        'tas': 120,
        'tad': 80,
        'perimetro_abdominal': 90,
        'realiza_ejercicio': 'Si',
        'fuma': 'No',
        'consume_alcohol': 'Ocasional',
        'medicamentos_hta': 'No',
        'historia_familiar_dm': 'Si',
        'diabetes_gestacional': 'No',
        'puntaje_findrisc': 8,
        'riesgo_cardiovascular': 0.3
    }

    prediction_data = {
        'glucose_mg_dl': 95.5,
        'category': 'Normal',
        'risk_level': 'Bajo',
        'confidence': 'Alto',
        'model_version': '1.0.0',
        'processing_time_ms': 45.2
    }

    try:
        # Guardar paciente
        patient_id = db_manager.save_patient(patient_data)
        logger.info(f"✅ Paciente guardado: {patient_id}")

        # Guardar predicción
        prediction_id = db_manager.save_prediction(patient_id, prediction_data, patient_data)
        logger.info(f"✅ Predicción guardada: {prediction_id}")

        # Obtener estadísticas
        stats = db_manager.get_database_stats()
        logger.info(f"📊 Estadísticas: {stats}")

        # Exportar datos
        exported_files = db_manager.export_data_to_csv()
        logger.info(f"💾 Archivos exportados: {exported_files}")

    except Exception as e:
        logger.error(f"❌ Error en prueba: {e}")