"""
Módulo de Optimización Automática de Hiperparámetros
Implementación con Optuna para optimización bayesiana
"""
import optuna
import numpy as np
import pandas as pd
from sklearn.model_selection import cross_val_score, StratifiedKFold
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
from typing import Dict, Any, Callable, Tuple, Optional
import logging
import time
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
from data_preprocessor import DiabetesDataPreprocessor

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DiabetesHyperparameterOptimizer:
    """Optimizador de hiperparámetros para modelos de diabetes"""

    def __init__(self, X_train: np.ndarray, y_train: np.ndarray, X_test: np.ndarray, y_test: np.ndarray):
        """
        Inicializar optimizador

        Args:
            X_train, X_test: Datos de entrenamiento y prueba
            y_train, y_test: Variables objetivo
        """
        self.X_train = X_train
        self.y_train = y_train
        self.X_test = X_test
        self.y_test = y_test

        self.preprocessor = DiabetesDataPreprocessor()
        self.study = None
        self.best_params = {}
        self.optimization_results = []

    def create_objective_function(self, model_name: str) -> Callable:
        """
        Crear función objetivo para Optuna

        Args:
            model_name: Nombre del modelo a optimizar

        Returns:
            Callable: Función objetivo para Optuna
        """

        def objective(trial):
            try:
                # Definir hiperparámetros según el modelo
                params = self._suggest_hyperparameters(trial, model_name)

                # Crear modelo con hiperparámetros sugeridos
                model = self._create_model(model_name, params)

                # Validación cruzada
                cv_scores = cross_val_score(
                    model,
                    self.X_train,
                    self.y_train,
                    cv=5,
                    scoring='r2',
                    n_jobs=-1
                )

                mean_r2 = cv_scores.mean()

                # Entrenar modelo completo
                model.fit(self.X_train, self.y_train)

                # Evaluar en conjunto de prueba
                y_pred = model.predict(self.X_test)
                test_r2 = r2_score(self.y_test, y_pred)
                test_rmse = np.sqrt(mean_squared_error(self.y_test, y_pred))

                # Guardar resultados de este trial
                trial_result = {
                    'trial': trial.number,
                    'params': params,
                    'cv_r2_mean': mean_r2,
                    'cv_r2_std': cv_scores.std(),
                    'test_r2': test_r2,
                    'test_rmse': test_rmse,
                    'model': model_name,
                    'timestamp': datetime.now().isoformat()
                }

                self.optimization_results.append(trial_result)

                # Optuna maximiza, así que retornamos R²
                return mean_r2

            except Exception as e:
                logger.error(f"Error en trial {trial.number} para {model_name}: {e}")
                return float('-inf')

        return objective

    def _suggest_hyperparameters(self, trial, model_name: str) -> Dict[str, Any]:
        """Sugerir hiperparámetros para un modelo específico"""

        if model_name == "Random Forest":
            return {
                'n_estimators': trial.suggest_int('n_estimators', 50, 300),
                'max_depth': trial.suggest_categorical('max_depth', [5, 10, 15, 20, None]),
                'min_samples_split': trial.suggest_int('min_samples_split', 2, 20),
                'min_samples_leaf': trial.suggest_int('min_samples_leaf', 1, 10),
                'max_features': trial.suggest_categorical('max_features', ['sqrt', 'log2', None]),
                'bootstrap': trial.suggest_categorical('bootstrap', [True, False])
            }

        elif model_name == "XGBoost":
            return {
                'n_estimators': trial.suggest_int('n_estimators', 50, 300),
                'max_depth': trial.suggest_int('max_depth', 3, 10),
                'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.3, log=True),
                'subsample': trial.suggest_float('subsample', 0.6, 1.0),
                'colsample_bytree': trial.suggest_float('colsample_bytree', 0.6, 1.0),
                'reg_alpha': trial.suggest_float('reg_alpha', 0, 1),
                'reg_lambda': trial.suggest_float('reg_lambda', 0, 1)
            }

        elif model_name == "LightGBM":
            return {
                'n_estimators': trial.suggest_int('n_estimators', 50, 300),
                'max_depth': trial.suggest_int('max_depth', 3, 15),
                'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.3, log=True),
                'num_leaves': trial.suggest_int('num_leaves', 20, 100),
                'subsample': trial.suggest_float('subsample', 0.6, 1.0),
                'colsample_bytree': trial.suggest_float('colsample_bytree', 0.6, 1.0),
                'reg_alpha': trial.suggest_float('reg_alpha', 0, 1),
                'reg_lambda': trial.suggest_float('reg_lambda', 0, 1)
            }

        elif model_name == "Gradient Boosting":
            return {
                'n_estimators': trial.suggest_int('n_estimators', 50, 300),
                'max_depth': trial.suggest_int('max_depth', 3, 10),
                'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.3, log=True),
                'subsample': trial.suggest_float('subsample', 0.6, 1.0),
                'min_samples_split': trial.suggest_int('min_samples_split', 2, 20),
                'min_samples_leaf': trial.suggest_int('min_samples_leaf', 1, 10)
            }

        elif model_name == "Ridge":
            return {
                'alpha': trial.suggest_float('alpha', 0.1, 10.0, log=True)
            }

        elif model_name == "Lasso":
            return {
                'alpha': trial.suggest_float('alpha', 0.001, 1.0, log=True)
            }

        elif model_name == "Elastic Net":
            return {
                'alpha': trial.suggest_float('alpha', 0.001, 1.0, log=True),
                'l1_ratio': trial.suggest_float('l1_ratio', 0.1, 0.9)
            }

        elif model_name == "SVR":
            return {
                'C': trial.suggest_float('C', 0.1, 100, log=True),
                'gamma': trial.suggest_categorical('gamma', ['scale', 'auto']),
                'kernel': trial.suggest_categorical('kernel', ['rbf', 'linear', 'poly'])
            }

        elif model_name == "K-Nearest Neighbors":
            return {
                'n_neighbors': trial.suggest_int('n_neighbors', 3, 20),
                'weights': trial.suggest_categorical('weights', ['uniform', 'distance']),
                'p': trial.suggest_categorical('p', [1, 2])  # 1: manhattan, 2: euclidean
            }

        elif model_name == "Neural Network":
            return {
                'hidden_layer_sizes': trial.suggest_categorical(
                    'hidden_layer_sizes',
                    [(50,), (100,), (50, 50), (100, 50), (100, 100)]
                ),
                'activation': trial.suggest_categorical('activation', ['relu', 'tanh', 'logistic']),
                'alpha': trial.suggest_float('alpha', 0.0001, 0.1, log=True),
                'learning_rate_init': trial.suggest_float('learning_rate_init', 0.001, 0.1, log=True)
            }

        else:
            # Para modelos sin hiperparámetros a optimizar
            return {}

    def _create_model(self, model_name: str, params: Dict[str, Any]) -> Any:
        """Crear modelo con hiperparámetros específicos"""

        base_models = {
            "Linear Regression": LinearRegression(),
            "Ridge": Ridge(random_state=RANDOM_SEED, **params),
            "Lasso": Lasso(random_state=RANDOM_SEED, **params),
            "Elastic Net": ElasticNet(random_state=RANDOM_SEED, **params),
            "Random Forest": RandomForestRegressor(random_state=RANDOM_SEED, n_jobs=-1, **params),
            "Extra Trees": ExtraTreesRegressor(random_state=RANDOM_SEED, n_jobs=-1),
            "Gradient Boosting": GradientBoostingRegressor(random_state=RANDOM_SEED, **params),
            "XGBoost": xgb.XGBRegressor(random_state=RANDOM_SEED, verbosity=0, **params),
            "LightGBM": lgb.LGBMRegressor(random_state=RANDOM_SEED, verbosity=-1, **params),
            "AdaBoost": AdaBoostRegressor(random_state=RANDOM_SEED),
            "SVR": SVR(**params),
            "K-Nearest Neighbors": KNeighborsRegressor(**params),
            "Neural Network": MLPRegressor(random_state=RANDOM_SEED, max_iter=1000, **params)
        }

        return base_models[model_name]

    def optimize_model(self, model_name: str, n_trials: int = 50,
                      timeout: Optional[int] = None) -> Dict[str, Any]:
        """
        Optimizar hiperparámetros para un modelo específico

        Args:
            model_name: Nombre del modelo a optimizar
            n_trials: Número de trials para optimización
            timeout: Timeout en segundos

        Returns:
            Dict: Resultados de la optimización
        """

        logger.info(f"🚀 Iniciando optimización de {model_name} con {n_trials} trials")

        # Crear función objetivo
        objective = self.create_objective_function(model_name)

        # Crear estudio Optuna
        study_name = f"{model_name.replace(' ', '_')}_optimization"
        self.study = optuna.create_study(
            study_name=study_name,
            direction='maximize',
            sampler=optuna.samplers.TPESampler(seed=RANDOM_SEED)
        )

        # Ejecutar optimización
        start_time = time.time()

        try:
            self.study.optimize(
                objective,
                n_trials=n_trials,
                timeout=timeout,
                show_progress_bar=True
            )
        except KeyboardInterrupt:
            logger.info("Optimización interrumpida por usuario")

        optimization_time = time.time() - start_time

        # Obtener mejores parámetros
        best_params = self.study.best_params
        best_value = self.study.best_value
        best_trial = self.study.best_trial

        logger.info(f"✅ Optimización completada en {optimization_time:.2f} segundos")
        logger.info(f"🏆 Mejor R² (CV): {best_value:.4f}")
        logger.info(f"📊 Mejor trial: {best_trial.number}")

        # Evaluar modelo final
        final_model = self._create_model(model_name, best_params)
        final_model.fit(self.X_train, self.y_train)

        y_pred_train = final_model.predict(self.X_train)
        y_pred_test = final_model.predict(self.X_test)

        final_metrics = {
            'train_r2': r2_score(self.y_train, y_pred_train),
            'test_r2': r2_score(self.y_test, y_pred_test),
            'train_rmse': np.sqrt(mean_squared_error(self.y_train, y_pred_train)),
            'test_rmse': np.sqrt(mean_squared_error(self.y_test, y_pred_test)),
            'train_mae': mean_absolute_error(self.y_train, y_pred_train),
            'test_mae': mean_absolute_error(self.y_test, y_pred_test)
        }

        # Resultados completos
        results = {
            'model_name': model_name,
            'best_params': best_params,
            'best_cv_r2': best_value,
            'best_trial_number': best_trial.number,
            'optimization_time': optimization_time,
            'n_trials_completed': len(self.study.trials),
            'final_model': final_model,
            'final_metrics': final_metrics,
            'optimization_history': self.optimization_results[-len(self.study.trials):]
        }

        # Guardar resultados
        self._save_optimization_results(results)

        return results

    def optimize_multiple_models(self, model_names: list, n_trials: int = 30,
                               timeout: Optional[int] = None) -> Dict[str, Any]:
        """
        Optimizar múltiples modelos

        Args:
            model_names: Lista de nombres de modelos a optimizar
            n_trials: Número de trials por modelo
            timeout: Timeout total en segundos

        Returns:
            Dict: Resultados de todas las optimizaciones
        """

        all_results = {}
        total_start_time = time.time()

        for model_name in model_names:
            logger.info(f"\n{'='*60}")
            logger.info(f"Optimizando modelo: {model_name}")
            logger.info(f"{'='*60}")

            try:
                # Optimizar modelo individual
                model_results = self.optimize_model(
                    model_name=model_name,
                    n_trials=n_trials,
                    timeout=timeout
                )

                all_results[model_name] = model_results

                # Log de progreso
                logger.info(f"✅ {model_name} optimizado:")
                logger.info(f"   R² (CV): {model_results['best_cv_r2']:.4f}")
                logger.info(f"   R² (Test): {model_results['final_metrics']['test_r2']:.4f}")
                logger.info(f"   RMSE (Test): {model_results['final_metrics']['test_rmse']:.2f}")

            except Exception as e:
                logger.error(f"❌ Error optimizando {model_name}: {e}")
                all_results[model_name] = {"error": str(e)}

        total_time = time.time() - total_start_time

        # Encontrar mejor modelo general
        best_model_name = None
        best_test_r2 = float('-inf')

        for model_name, results in all_results.items():
            if "error" not in results:
                test_r2 = results['final_metrics']['test_r2']
                if test_r2 > best_test_r2:
                    best_test_r2 = test_r2
                    best_model_name = model_name

        summary = {
            'total_time': total_time,
            'models_optimized': len([r for r in all_results.values() if "error" not in r]),
            'best_model': best_model_name,
            'best_test_r2': best_test_r2,
            'all_results': all_results
        }

        # Guardar resumen
        self._save_optimization_summary(summary)

        logger.info(f"\n🎉 Optimización completada en {total_time/60:.2f} minutos")
        logger.info(f"🏆 Mejor modelo: {best_model_name} (R² Test: {best_test_r2:.4f})")

        return summary

    def _save_optimization_results(self, results: Dict[str, Any]):
        """Guardar resultados de optimización"""

        # Crear directorio si no existe
        config.OUTPUTS_DIR.mkdir(exist_ok=True)

        # Guardar resultados detallados
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"optimization_{results['model_name'].replace(' ', '_')}_{timestamp}.json"

        filepath = config.OUTPUTS_DIR / filename

        with open(filepath, 'w') as f:
            json.dump(results, f, indent=2, default=str)

        logger.info(f"💾 Resultados guardados: {filepath}")

    def _save_optimization_summary(self, summary: Dict[str, Any]):
        """Guardar resumen de optimización"""

        filepath = config.OUTPUTS_DIR / "optimization_summary.json"

        with open(filepath, 'w') as f:
            json.dump(summary, f, indent=2, default=str)

        logger.info(f"💾 Resumen guardado: {filepath}")

    def get_optimization_report(self) -> Dict[str, Any]:
        """Generar reporte de optimización"""

        if not self.optimization_results:
            return {"error": "No hay resultados de optimización"}

        # Convertir a DataFrame para análisis
        results_df = pd.DataFrame(self.optimization_results)

        report = {
            'total_trials': len(results_df),
            'models_tested': results_df['model'].unique().tolist(),
            'best_overall_r2': results_df['test_r2'].max(),
            'average_r2': results_df['test_r2'].mean(),
            'r2_std': results_df['test_r2'].std(),
            'best_trial_per_model': {},
            'summary_statistics': results_df.describe().to_dict()
        }

        # Mejor trial por modelo
        for model in results_df['model'].unique():
            model_trials = results_df[results_df['model'] == model]
            best_trial = model_trials.loc[model_trials['test_r2'].idxmax()]
            report['best_trial_per_model'][model] = best_trial.to_dict()

        return report

def optimize_diabetes_models(X_train: np.ndarray, y_train: np.ndarray,
                           X_test: np.ndarray, y_test: np.ndarray,
                           models_to_optimize: list = None,
                           n_trials: int = 30) -> Dict[str, Any]:
    """
    Función de conveniencia para optimizar modelos de diabetes

    Args:
        X_train, X_test: Datos de entrenamiento y prueba
        y_train, y_test: Variables objetivo
        models_to_optimize: Lista de modelos a optimizar (opcional)
        n_trials: Número de trials por modelo

    Returns:
        Dict: Resultados de la optimización
    """

    if models_to_optimize is None:
        models_to_optimize = [
            "Random Forest", "XGBoost", "LightGBM", "Gradient Boosting",
            "Ridge", "Lasso", "SVR", "Neural Network"
        ]

    logger.info("🔬 Iniciando optimización automática de hiperparámetros")
    logger.info(f"Modelos a optimizar: {models_to_optimize}")
    logger.info(f"Trials por modelo: {n_trials}")

    # Crear optimizador
    optimizer = DiabetesHyperparameterOptimizer(X_train, y_train, X_test, y_test)

    # Ejecutar optimización
    results = optimizer.optimize_multiple_models(
        model_names=models_to_optimize,
        n_trials=n_trials
    )

    # Generar reporte
    report = optimizer.get_optimization_report()

    return {
        'optimization_results': results,
        'report': report,
        'optimizer': optimizer
    }

if __name__ == "__main__":
    # Ejemplo de uso
    from data_generator import create_sample_dataset
    from data_preprocessor import preprocess_diabetes_data
    from sklearn.model_selection import train_test_split

    logger.info("🧪 Probando optimizador de hiperparámetros...")

    # Generar datos
    df = create_sample_dataset(n_samples=500)

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

    # Optimizar modelos
    results = optimize_diabetes_models(
        X_train_scaled, y_train, X_test_scaled, y_test,
        models_to_optimize=["Random Forest", "XGBoost"],
        n_trials=10  # Solo 10 trials para prueba rápida
    )

    logger.info("✅ Optimización completada")
    logger.info(f"Mejor modelo: {results['optimization_results']['best_model']}")