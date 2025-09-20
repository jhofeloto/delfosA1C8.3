"""
Configuración del Sistema Predictivo de Diabetes
"""
import os
from pathlib import Path
from datetime import datetime

class Config:
    """Configuración centralizada del proyecto"""

    def __init__(self):
        # Rutas base del proyecto
        self.PROJECT_ROOT = Path(__file__).parent
        self.MODELS_DIR = self.PROJECT_ROOT / "models"
        self.OUTPUTS_DIR = self.PROJECT_ROOT / "outputs"
        self.DATA_DIR = self.PROJECT_ROOT / "data"

        # Configuración de modelos
        self.RANDOM_SEED = 42
        self.TEST_SIZE = 0.2

        # Configuración de datos
        self.DEFAULT_N_SAMPLES = 1000
        self.MIN_AGE = 18
        self.MAX_AGE = 90

        # Configuración de entrenamiento
        self.CROSS_VAL_FOLDS = 5
        self.OPTIMIZATION_SCORING = 'r2'

        # Configuración de exportación
        self.MODEL_EXPORT_FORMATS = ['joblib', 'pkl']
        self.METADATA_FILENAME = "model_metadata.json"

        # Crear directorios necesarios
        self._create_directories()

    def _create_directories(self):
        """Crear directorios necesarios si no existen"""
        directories = [
            self.MODELS_DIR,
            self.OUTPUTS_DIR,
            self.DATA_DIR
        ]

        for directory in directories:
            directory.mkdir(exist_ok=True)
            print(f"✅ Directorio creado/verificado: {directory}")

    def get_model_path(self, model_name: str, format: str = 'joblib') -> Path:
        """Obtener ruta completa para un modelo específico"""
        filename = f"{model_name.lower().replace(' ', '_')}.{format}"
        return self.MODELS_DIR / filename

    def get_best_model_path(self, format: str = 'joblib') -> Path:
        """Obtener ruta del mejor modelo"""
        filename = f"best_model.{format}"
        return self.MODELS_DIR / filename

    def get_output_path(self, filename: str) -> Path:
        """Obtener ruta para archivos de salida"""
        return self.OUTPUTS_DIR / filename

    def get_timestamped_filename(self, base_name: str, extension: str) -> str:
        """Generar nombre de archivo con timestamp"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{base_name}_{timestamp}.{extension}"

# Instancia global de configuración
config = Config()

# Variables de conveniencia para importación directa
PROJECT_ROOT = config.PROJECT_ROOT
MODELS_DIR = config.MODELS_DIR
OUTPUTS_DIR = config.OUTPUTS_DIR
DATA_DIR = config.DATA_DIR
RANDOM_SEED = config.RANDOM_SEED