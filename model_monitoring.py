"""
Sistema de Monitoreo de Modelos con MLflow
Implementación para tracking de experimentos, métricas y modelos
"""
import mlflow
import mlflow.sklearn
import mlflow.xgboost
import mlflow.lightgbm
import numpy as np
import pandas as pd
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
from sklearn.model_selection import cross_val_score
from typing import Dict, Any, List, Optional
import logging
from datetime import datetime
import json
from pathlib import Path

# Importar modelos
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet
from sklearn.ensemble import (
    RandomForestRegressor, GradientBoostingRegressor,
    ExtraTreesRegressor, AdaBoostRegressor
)
from sklearn.svm import SVR
from sklearn.neural_network import MLPRegressor
from sklearn.neighbors import KNeighborsRegressor
import xgboost as xgb
import lightgbm as lgb

from config import config, RANDOM_SEED

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DiabetesModelMonitor:
    """Sistema de monitoreo para modelos de diabetes usando MLflow"""

    def __init__(self, experiment_name: str = "diabetes_prediction"):
        """
        Inicializar monitor de modelos

        Args:
            experiment_name: Nombre del experimento en MLflow
        """
        self.experiment_name = experiment_name
        self.experiment_id = None
        self.run_id = None

        # Configurar MLflow
        mlflow.set_tracking_uri(f"file://{config.OUTPUTS_DIR / 'mlruns'}")
        self._setup_experiment()

    def _setup_experiment(self):
        """Configurar experimento en MLflow"""
        try:
            # Crear experimento si no existe
            experiment = mlflow.get_experiment_by_name(self.experiment_name)
            if experiment is None:
                self.experiment_id = mlflow.create_experiment(self.experiment_name)
                logger.info(f"✅ Experimento creado: {self.experiment_name}")
            else:
                self.experiment_id = experiment.experiment_id
                logger.info(f"✅ Experimento existente: {self.experiment_name}")

            # Configurar experimento activo
            mlflow.set_experiment(self.experiment_name)

        except Exception as e:
            logger.error(f"❌ Error configurando experimento: {e}")

    def log_model_training(self, model_name: str, model: Any, params: Dict[str, Any],
                         X_train: np.ndarray, y_train: np.ndarray,
                         X_test: np.ndarray, y_test: np.ndarray,
                         cv_scores: Optional[np.ndarray] = None) -> str:
        """
        Registrar entrenamiento de un modelo

        Args:
            model_name: Nombre del modelo
            model: Modelo entrenado
            params: Hiperparámetros del modelo
            X_train, X_test: Datos de entrenamiento y prueba
            y_train, y_test: Variables objetivo
            cv_scores: Scores de validación cruzada

        Returns:
            str: ID del run de MLflow
        """

        with mlflow.start_run(run_name=f"{model_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}") as run:

            # Log de hiperparámetros
            if params:
                mlflow.log_params(params)

            # Log de métricas de entrenamiento
            y_pred_train = model.predict(X_train)
            train_metrics = self._calculate_metrics(y_train, y_pred_train)
            mlflow.log_metrics({f"train_{k}": v for k, v in train_metrics.items()})

            # Log de métricas de prueba
            y_pred_test = model.predict(X_test)
            test_metrics = self._calculate_metrics(y_test, y_pred_test)
            mlflow.log_metrics({f"test_{k}": v for k, v in test_metrics.items()})

            # Log de métricas de validación cruzada
            if cv_scores is not None:
                mlflow.log_metric("cv_r2_mean", cv_scores.mean())
                mlflow.log_metric("cv_r2_std", cv_scores.std())

            # Log de información adicional
            mlflow.log_param("model_type", model_name)
            mlflow.log_param("training_date", datetime.now().isoformat())
            mlflow.log_param("n_train_samples", len(X_train))
            mlflow.log_param("n_test_samples", len(X_test))
            mlflow.log_param("n_features", X_train.shape[1])

            # Log del modelo
            try:
                if "XGBoost" in model_name:
                    mlflow.xgboost.log_model(model, "model")
                elif "LightGBM" in model_name:
                    mlflow.lightgbm.log_model(model, "model")
                else:
                    mlflow.sklearn.log_model(model, "model")

                logger.info(f"✅ Modelo {model_name} registrado en MLflow")

            except Exception as e:
                logger.error(f"❌ Error registrando modelo {model_name}: {e}")

            # Log de artefactos adicionales
            self._log_artifacts(model_name, X_train, y_train, X_test, y_test, y_pred_test)

            run_id = run.info.run_id
            logger.info(f"📊 Run ID: {run_id}")

            return run_id

    def _calculate_metrics(self, y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, float]:
        """Calcular métricas de rendimiento"""
        return {
            'r2_score': r2_score(y_true, y_pred),
            'rmse': np.sqrt(mean_squared_error(y_true, y_pred)),
            'mae': mean_absolute_error(y_true, y_pred),
            'mse': mean_squared_error(y_true, y_pred)
        }

    def _log_artifacts(self, model_name: str, X_train: np.ndarray, y_train: np.ndarray,
                      X_test: np.ndarray, y_test: np.ndarray, y_pred: np.ndarray):
        """Registrar artefactos adicionales"""

        # Crear directorio temporal para artefactos
        artifacts_dir = Path("temp_artifacts")
        artifacts_dir.mkdir(exist_ok=True)

        try:
            # Gráfico de predicciones vs valores reales
            plt = self._create_prediction_plot(y_test, y_pred, model_name)
            plt.savefig(artifacts_dir / f"{model_name}_predictions.png")
            mlflow.log_artifact(artifacts_dir / f"{model_name}_predictions.png")

            # Métricas detalladas
            metrics_data = {
                'model_name': model_name,
                'training_samples': len(X_train),
                'test_samples': len(X_test),
                'features': X_train.shape[1],
                'metrics': self._calculate_metrics(y_test, y_pred),
                'timestamp': datetime.now().isoformat()
            }

            with open(artifacts_dir / f"{model_name}_metrics.json", 'w') as f:
                json.dump(metrics_data, f, indent=2)

            mlflow.log_artifact(artifacts_dir / f"{model_name}_metrics.json")

            # Distribución de errores
            errors = y_test - y_pred
            error_data = {
                'mean_error': errors.mean(),
                'std_error': errors.std(),
                'min_error': errors.min(),
                'max_error': errors.max(),
                'percentile_25': np.percentile(errors, 25),
                'percentile_75': np.percentile(errors, 75)
            }

            with open(artifacts_dir / f"{model_name}_error_analysis.json", 'w') as f:
                json.dump(error_data, f, indent=2)

            mlflow.log_artifact(artifacts_dir / f"{model_name}_error_analysis.json")

        except Exception as e:
            logger.error(f"❌ Error creando artefactos para {model_name}: {e}")
        finally:
            # Limpiar archivos temporales
            if artifacts_dir.exists():
                import shutil
                shutil.rmtree(artifacts_dir)

    def _create_prediction_plot(self, y_true: np.ndarray, y_pred: np.ndarray, model_name: str):
        """Crear gráfico de predicciones vs valores reales"""
        try:
            import matplotlib.pyplot as plt

            fig, axes = plt.subplots(2, 2, figsize=(12, 10))

            # Scatter plot: Predicciones vs Reales
            axes[0, 0].scatter(y_true, y_pred, alpha=0.5)
            axes[0, 0].plot([y_true.min(), y_true.max()], [y_true.min(), y_true.max()],
                           'r--', alpha=0.8)
            axes[0, 0].set_xlabel('Valores Reales')
            axes[0, 0].set_ylabel('Predicciones')
            axes[0, 0].set_title(f'{model_name}: Predicciones vs Reales')
            axes[0, 0].grid(True, alpha=0.3)

            # Histograma de residuos
            residuals = y_true - y_pred
            axes[0, 1].hist(residuals, bins=30, alpha=0.7, edgecolor='black')
            axes[0, 1].axvline(x=0, color='red', linestyle='--', alpha=0.8)
            axes[0, 1].set_xlabel('Residuos')
            axes[0, 1].set_ylabel('Frecuencia')
            axes[0, 1].set_title('Distribución de Residuos')
            axes[0, 1].grid(True, alpha=0.3)

            # Q-Q plot
            from scipy import stats
            stats.probplot(residuals, dist="norm", plot=axes[1, 0])
            axes[1, 0].set_title('Q-Q Plot de Residuos')

            # Residuos vs Predicciones
            axes[1, 1].scatter(y_pred, residuals, alpha=0.5)
            axes[1, 1].axhline(y=0, color='red', linestyle='--', alpha=0.8)
            axes[1, 1].set_xlabel('Predicciones')
            axes[1, 1].set_ylabel('Residuos')
            axes[1, 1].set_title('Residuos vs Predicciones')
            axes[1, 1].grid(True, alpha=0.3)

            plt.tight_layout()
            return fig

        except ImportError:
            logger.warning("matplotlib no disponible para gráficos")
            return None

    def log_experiment_comparison(self, model_results: List[Dict[str, Any]]):
        """
        Registrar comparación de múltiples modelos

        Args:
            model_results: Lista de resultados de modelos
        """

        with mlflow.start_run(run_name=f"model_comparison_{datetime.now().strftime('%Y%m%d_%H%M%S')}") as run:

            # Crear DataFrame con resultados
            results_df = pd.DataFrame([
                {
                    'model_name': r['name'],
                    'train_r2': r['train_r2'],
                    'test_r2': r['test_r2'],
                    'train_rmse': r['train_rmse'],
                    'test_rmse': r['test_rmse'],
                    'train_mae': r['train_mae'],
                    'test_mae': r['test_mae'],
                    'cv_r2_mean': r.get('cv_r2_mean', 0),
                    'cv_r2_std': r.get('cv_r2_std', 0)
                }
                for r in model_results
            ])

            # Log de métricas agregadas
            best_model = results_df.loc[results_df['test_r2'].idxmax()]
            mlflow.log_metric("best_test_r2", best_model['test_r2'])
            mlflow.log_metric("best_test_rmse", best_model['test_rmse'])
            mlflow.log_metric("best_test_mae", best_model['test_mae'])
            mlflow.log_metric("models_compared", len(results_df))

            # Log de parámetros
            mlflow.log_param("comparison_date", datetime.now().isoformat())
            mlflow.log_param("total_models", len(results_df))

            # Guardar tabla de comparación como artefacto
            comparison_file = config.OUTPUTS_DIR / "model_comparison.csv"
            results_df.to_csv(comparison_file, index=False)
            mlflow.log_artifact(comparison_file)

            # Log de mejor modelo
            mlflow.log_param("best_model_name", best_model['model_name'])

            logger.info(f"✅ Comparación de modelos registrada: {len(results_df)} modelos")
            logger.info(f"🏆 Mejor modelo: {best_model['model_name']}")

    def log_hyperparameter_optimization(self, optimization_results: Dict[str, Any]):
        """
        Registrar resultados de optimización de hiperparámetros

        Args:
            optimization_results: Resultados de la optimización
        """

        with mlflow.start_run(run_name=f"hyperopt_{datetime.now().strftime('%Y%m%d_%H%M%S')}") as run:

            # Log de métricas principales
            best_model = optimization_results.get('best_model')
            best_r2 = optimization_results.get('best_test_r2', 0)

            mlflow.log_metric("best_optimized_r2", best_r2)
            mlflow.log_metric("optimization_time_minutes", optimization_results.get('total_time', 0) / 60)
            mlflow.log_metric("models_optimized", optimization_results.get('models_optimized', 0))

            # Log de parámetros
            mlflow.log_param("optimization_date", datetime.now().isoformat())
            mlflow.log_param("best_model", best_model)

            # Guardar resultados detallados
            results_file = config.OUTPUTS_DIR / "optimization_results.json"
            with open(results_file, 'w') as f:
                json.dump(optimization_results, f, indent=2, default=str)

            mlflow.log_artifact(results_file)

            logger.info(f"✅ Optimización registrada: {best_model} (R²: {best_r2:.4f})")

    def get_experiment_history(self) -> Dict[str, Any]:
        """Obtener historial del experimento"""
        try:
            experiment = mlflow.get_experiment(self.experiment_id)

            # Obtener todas las runs
            runs = mlflow.search_runs(experiment_ids=[self.experiment_id])

            if runs.empty:
                return {"error": "No hay runs en el experimento"}

            # Resumen de métricas
            summary = {
                'experiment_name': experiment.name,
                'experiment_id': experiment.experiment_id,
                'total_runs': len(runs),
                'best_r2_score': runs['metrics.test_r2'].max() if 'metrics.test_r2' in runs.columns else None,
                'best_rmse': runs['metrics.test_rmse'].min() if 'metrics.test_rmse' in runs.columns else None,
                'runs_summary': runs[['run_id', 'start_time', 'metrics.test_r2', 'metrics.test_rmse']].head(10).to_dict()
            }

            return summary

        except Exception as e:
            logger.error(f"Error obteniendo historial: {e}")
            return {"error": str(e)}

    def load_model_from_mlflow(self, run_id: str) -> Any:
        """
        Cargar modelo desde MLflow

        Args:
            run_id: ID del run de MLflow

        Returns:
            Modelo cargado
        """
        try:
            model_uri = f"runs:/{run_id}/model"
            model = mlflow.sklearn.load_model(model_uri)
            logger.info(f"✅ Modelo cargado desde MLflow: {run_id}")
            return model

        except Exception as e:
            logger.error(f"❌ Error cargando modelo {run_id}: {e}")
            return None

    def compare_models_mlflow(self, run_ids: List[str]) -> pd.DataFrame:
        """
        Comparar modelos desde MLflow

        Args:
            run_ids: Lista de IDs de runs a comparar

        Returns:
            DataFrame con comparación
        """
        comparison_data = []

        for run_id in run_ids:
            try:
                run = mlflow.get_run(run_id)

                # Extraer métricas
                metrics = run.data.metrics
                params = run.data.params

                comparison_data.append({
                    'run_id': run_id,
                    'model_name': params.get('model_type', 'Unknown'),
                    'test_r2': metrics.get('test_r2', 0),
                    'test_rmse': metrics.get('test_rmse', 0),
                    'test_mae': metrics.get('test_mae', 0),
                    'train_r2': metrics.get('train_r2', 0),
                    'training_date': params.get('training_date', 'Unknown')
                })

            except Exception as e:
                logger.error(f"Error procesando run {run_id}: {e}")

        return pd.DataFrame(comparison_data)

def setup_mlflow_tracking():
    """Configurar tracking de MLflow"""
    tracking_dir = config.OUTPUTS_DIR / "mlruns"
    tracking_dir.mkdir(exist_ok=True)

    mlflow.set_tracking_uri(f"file://{tracking_dir}")

    logger.info(f"📊 MLflow tracking configurado en: {tracking_dir}")

def log_training_session(X_train: np.ndarray, y_train: np.ndarray,
                        X_test: np.ndarray, y_test: np.ndarray,
                        model_results: List[Dict[str, Any]]) -> DiabetesModelMonitor:
    """
    Función de conveniencia para registrar sesión de entrenamiento

    Args:
        X_train, X_test: Datos de entrenamiento y prueba
        y_train, y_test: Variables objetivo
        model_results: Resultados de modelos

    Returns:
        DiabetesModelMonitor: Instancia del monitor
    """

    # Configurar MLflow
    setup_mlflow_tracking()

    # Crear monitor
    monitor = DiabetesModelMonitor("diabetes_training_session")

    # Registrar cada modelo
    for result in model_results:
        try:
            model = result['model']
            model_name = result['name']

            # Preparar parámetros para logging
            params = {}
            if hasattr(model, 'get_params'):
                params = model.get_params()

            # Registrar modelo
            monitor.log_model_training(
                model_name=model_name,
                model=model,
                params=params,
                X_train=X_train,
                y_train=y_train,
                X_test=X_test,
                y_test=y_test
            )

        except Exception as e:
            logger.error(f"Error registrando modelo {result['name']}: {e}")

    # Registrar comparación
    monitor.log_experiment_comparison(model_results)

    logger.info("✅ Sesión de entrenamiento registrada en MLflow")

    return monitor

if __name__ == "__main__":
    # Ejemplo de uso
    from data_generator import create_sample_dataset
    from data_preprocessor import preprocess_diabetes_data
    from model_trainer import train_diabetes_models
    from sklearn.model_selection import train_test_split

    logger.info("🧪 Probando sistema de monitoreo MLflow...")

    # Generar datos
    df = create_sample_dataset(n_samples=200)

    # Preprocesar
    df_processed, preprocessor = preprocess_diabetes_data(df)

    # Dividir datos
    feature_columns = [col for col in df_processed.columns if col != 'Resultado']
    X = df_processed[feature_columns]
    y = df_processed['Resultado']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=RANDOM_SEED
    )

    # Escalar
    X_train_scaled, X_test_scaled = preprocessor.scale_features(X_train, X_test)

    # Entrenar modelos (solo 2 para prueba rápida)
    from model_trainer import DiabetesModelTrainer
    trainer = DiabetesModelTrainer()
    trainer.models = dict(list(trainer.models.items())[:2])  # Solo 2 modelos

    results_df = trainer.train_all_models(X_train_scaled, y_train, X_test_scaled, y_test)

    # Configurar monitoreo
    monitor = log_training_session(X_train_scaled, y_train, X_test_scaled, y_test, trainer.results)

    # Mostrar historial
    history = monitor.get_experiment_history()
    logger.info(f"📊 Historial del experimento: {history}")