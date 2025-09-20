"""
Módulo de entrenamiento de modelos para predicción de diabetes
"""
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
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
from tqdm import tqdm
import joblib
import json
from datetime import datetime
from typing import Dict, List, Tuple, Any
from config import config, RANDOM_SEED

class DiabetesModelTrainer:
    """Entrenador de modelos para predicción de diabetes"""

    def __init__(self):
        self.models = self._define_models()
        self.results = []
        self.best_model = None
        self.best_model_name = None
        self.preprocessor = None

    def _define_models(self) -> Dict[str, Any]:
        """Definir todos los modelos a entrenar"""
        return {
            'Linear Regression': LinearRegression(),

            'Ridge Regression': Ridge(alpha=1.0, random_state=RANDOM_SEED),

            'Lasso Regression': Lasso(alpha=0.1, random_state=RANDOM_SEED),

            'Elastic Net': ElasticNet(alpha=0.1, random_state=RANDOM_SEED),

            'Random Forest': RandomForestRegressor(
                n_estimators=100, max_depth=10, min_samples_split=5,
                min_samples_leaf=2, random_state=RANDOM_SEED, n_jobs=-1
            ),

            'Extra Trees': ExtraTreesRegressor(
                n_estimators=100, max_depth=10, random_state=RANDOM_SEED, n_jobs=-1
            ),

            'Gradient Boosting': GradientBoostingRegressor(
                n_estimators=200, learning_rate=0.1, max_depth=7,
                min_samples_split=5, min_samples_leaf=3, subsample=0.8,
                random_state=RANDOM_SEED
            ),

            'XGBoost': xgb.XGBRegressor(
                n_estimators=200, learning_rate=0.1, max_depth=7,
                subsample=0.8, colsample_bytree=0.8, random_state=RANDOM_SEED,
                verbosity=0
            ),

            'LightGBM': lgb.LGBMRegressor(
                n_estimators=200, learning_rate=0.1, max_depth=7,
                num_leaves=31, subsample=0.8, colsample_bytree=0.8,
                random_state=RANDOM_SEED, verbosity=-1
            ),

            'AdaBoost': AdaBoostRegressor(
                n_estimators=100, learning_rate=1.0, random_state=RANDOM_SEED
            ),

            'Support Vector Machine': SVR(
                kernel='rbf', C=100, gamma='scale'
            ),

            'K-Nearest Neighbors': KNeighborsRegressor(
                n_neighbors=7, weights='distance'
            ),

            'Neural Network': MLPRegressor(
                hidden_layer_sizes=(100, 50), activation='relu',
                solver='adam', max_iter=1000, random_state=RANDOM_SEED
            )
        }

    def train_model(self, model: Any, X_train: np.ndarray, y_train: np.ndarray,
                   X_test: np.ndarray, y_test: np.ndarray, model_name: str) -> Dict:
        """
        Entrena un modelo individual y retorna métricas

        Args:
            model: Modelo a entrenar
            X_train, X_test: Datos de entrenamiento y prueba
            y_train, y_test: Variables objetivo
            model_name: Nombre del modelo

        Returns:
            Dict: Métricas del modelo entrenado
        """
        # Entrenar
        model.fit(X_train, y_train)

        # Predicciones
        y_pred_train = model.predict(X_train)
        y_pred_test = model.predict(X_test)

        # Métricas
        metrics = {
            'model': model,
            'name': model_name,
            'train_r2': r2_score(y_train, y_pred_train),
            'test_r2': r2_score(y_test, y_pred_test),
            'train_rmse': np.sqrt(mean_squared_error(y_train, y_pred_train)),
            'test_rmse': np.sqrt(mean_squared_error(y_test, y_pred_test)),
            'train_mae': mean_absolute_error(y_train, y_pred_train),
            'test_mae': mean_absolute_error(y_test, y_pred_test),
            'predictions': y_pred_test
        }

        # Cross-validation
        cv_scores = cross_val_score(model, X_train, y_train,
                                   cv=config.CROSS_VAL_FOLDS, scoring=config.OPTIMIZATION_SCORING)
        metrics['cv_r2_mean'] = cv_scores.mean()
        metrics['cv_r2_std'] = cv_scores.std()

        return metrics

    def train_all_models(self, X_train: np.ndarray, y_train: np.ndarray,
                        X_test: np.ndarray, y_test: np.ndarray) -> pd.DataFrame:
        """
        Entrena todos los modelos definidos

        Args:
            X_train, X_test: Datos de entrenamiento y prueba
            y_train, y_test: Variables objetivo

        Returns:
            pd.DataFrame: Resultados de todos los modelos
        """
        print("🤖 ENTRENANDO MODELOS")
        print("="*60)
        print(f"Total de modelos a entrenar: {len(self.models)}")
        print("\nIniciando entrenamiento...\n")

        self.results = []

        for name, model in tqdm(self.models.items(), desc="Entrenando modelos"):
            try:
                metrics = self.train_model(model, X_train, y_train, X_test, y_test, name)
                self.results.append(metrics)
                print(f"✅ {name}: R² Test = {metrics['test_r2']:.4f}")
            except Exception as e:
                print(f"❌ Error en {name}: {e}")

        return self.get_results_dataframe()

    def get_results_dataframe(self) -> pd.DataFrame:
        """Obtener DataFrame con resultados ordenados"""
        if not self.results:
            return pd.DataFrame()

        results_df = pd.DataFrame([
            {
                'Modelo': r['name'],
                'R² Train': r['train_r2'],
                'R² Test': r['test_r2'],
                'RMSE Train': r['train_rmse'],
                'RMSE Test': r['test_rmse'],
                'MAE Train': r['train_mae'],
                'MAE Test': r['test_mae'],
                'CV R² Mean': r['cv_r2_mean'],
                'CV R² Std': r['cv_r2_std'],
                'Overfitting': r['train_r2'] - r['test_r2']
            }
            for r in self.results
        ])

        # Ordenar por R² Test
        results_df = results_df.sort_values('R² Test', ascending=False)
        return results_df

    def get_best_model(self) -> Tuple[Any, str, float]:
        """Obtener el mejor modelo basado en R² Test"""
        if not self.results:
            return None, None, 0.0

        best_result = max(self.results, key=lambda x: x['test_r2'])
        self.best_model = best_result['model']
        self.best_model_name = best_result['name']
        best_r2 = best_result['test_r2']

        print(f"\n🏆 MEJOR MODELO: {self.best_model_name}")
        print(f"   R² Score: {best_r2:.4f}")
        print(f"   RMSE: {best_result['test_rmse']:.2f} mg/dL")
        print(f"   MAE: {best_result['test_mae']:.2f} mg/dL")

        return self.best_model, self.best_model_name, best_r2

    def optimize_hyperparameters(self, X_train: np.ndarray, y_train: np.ndarray) -> Any:
        """Optimizar hiperparámetros del mejor modelo"""
        if not self.best_model_name:
            print("❌ No hay modelo base para optimizar")
            return self.best_model

        print("🔧 OPTIMIZANDO HIPERPARÁMETROS")
        print("="*60)
        print(f"Optimizando: {self.best_model_name}")

        # Definir grids de búsqueda según el modelo
        param_grids = {
            'Gradient Boosting': {
                'n_estimators': [100, 200, 300],
                'learning_rate': [0.05, 0.1, 0.15],
                'max_depth': [5, 7, 9],
                'min_samples_split': [2, 5, 10],
                'subsample': [0.7, 0.8, 0.9]
            },
            'Random Forest': {
                'n_estimators': [100, 200, 300],
                'max_depth': [5, 10, 15, None],
                'min_samples_split': [2, 5, 10],
                'min_samples_leaf': [1, 2, 4]
            },
            'XGBoost': {
                'n_estimators': [100, 200, 300],
                'learning_rate': [0.01, 0.1, 0.3],
                'max_depth': [3, 5, 7],
                'subsample': [0.6, 0.8, 1.0],
                'colsample_bytree': [0.6, 0.8, 1.0]
            },
            'LightGBM': {
                'n_estimators': [100, 200, 300],
                'learning_rate': [0.01, 0.1, 0.3],
                'max_depth': [5, 10, 15],
                'num_leaves': [31, 50, 100],
                'subsample': [0.6, 0.8, 1.0]
            }
        }

        if self.best_model_name not in param_grids:
            print(f"No hay grid de búsqueda definido para {self.best_model_name}")
            return self.best_model

        # GridSearchCV
        grid_search = GridSearchCV(
            self.models[self.best_model_name],
            param_grids[self.best_model_name],
            cv=config.CROSS_VAL_FOLDS,
            scoring=config.OPTIMIZATION_SCORING,
            n_jobs=-1,
            verbose=1
        )

        print("\nIniciando búsqueda...")
        grid_search.fit(X_train, y_train)

        print(f"\n✅ Mejores parámetros encontrados:")
        for param, value in grid_search.best_params_.items():
            print(f"   {param}: {value}")

        print(f"\nMejor score CV: {grid_search.best_score_:.4f}")

        return grid_search.best_estimator_

    def save_models(self, feature_columns: List[str]) -> Dict[str, str]:
        """
        Guardar todos los modelos entrenados

        Args:
            feature_columns: Lista de nombres de características

        Returns:
            Dict[str, str]: Rutas de archivos guardados
        """
        print("💾 GUARDANDO MODELOS")
        print("="*60)

        saved_files = {}

        # Guardar todos los modelos
        for model_result in self.results:
            model_name = model_result['name'].lower().replace(' ', '_')
            model_filename = config.get_model_path(model_name, 'joblib')

            # Guardar modelo
            joblib.dump(model_result['model'], model_filename)
            saved_files[f"{model_name}_joblib"] = str(model_filename)
            print(f"✅ Guardado: {model_filename}")

            # También guardar como pickle
            pickle_filename = config.get_model_path(model_name, 'pkl')
            with open(pickle_filename, 'wb') as f:
                import pickle
                pickle.dump(model_result['model'], f)
            saved_files[f"{model_name}_pkl"] = str(pickle_filename)

        # Guardar el mejor modelo con nombre especial
        if self.best_model:
            best_model_filename = config.get_best_model_path('joblib')
            joblib.dump(self.best_model, best_model_filename)
            saved_files['best_model_joblib'] = str(best_model_filename)
            print(f"\n🏆 Mejor modelo guardado en: {best_model_filename}")

        # Guardar el scaler si existe
        if self.preprocessor and hasattr(self.preprocessor, 'scaler'):
            scaler_filename = config.MODELS_DIR / "scaler.joblib"
            joblib.dump(self.preprocessor.scaler, scaler_filename)
            saved_files['scaler'] = str(scaler_filename)
            print(f"📏 Scaler guardado en: {scaler_filename}")

        # Guardar metadatos del modelo
        metadata = {
            'best_model': self.best_model_name,
            'best_r2_score': self.results[0]['test_r2'] if self.results else 0.0,
            'feature_columns': feature_columns,
            'n_features': len(feature_columns),
            'training_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'n_train_samples': len(self.results[0].get('model', None).__dict__.get('n_samples_', 0)) if self.results else 0,
            'model_results': [
                {
                    'name': r['name'],
                    'r2_test': r['test_r2'],
                    'rmse_test': r['test_rmse'],
                    'mae_test': r['test_mae']
                }
                for r in self.results
            ]
        }

        metadata_filename = config.MODELS_DIR / config.METADATA_FILENAME
        with open(metadata_filename, 'w') as f:
            json.dump(metadata, f, indent=4)
        saved_files['metadata'] = str(metadata_filename)

        return saved_files

def train_diabetes_models(df_processed: pd.DataFrame,
                         preprocessor: Any = None) -> DiabetesModelTrainer:
    """
    Función de conveniencia para entrenar modelos de diabetes

    Args:
        df_processed: DataFrame con datos preprocesados
        preprocessor: Preprocesador de datos (opcional)

    Returns:
        DiabetesModelTrainer: Entrenador con modelos entrenados
    """
    # Separar características y variable objetivo
    feature_columns = [col for col in df_processed.columns if col != 'Resultado']
    X = df_processed[feature_columns]
    y = df_processed['Resultado']

    # Crear bins para estratificación
    y_bins = pd.cut(y, bins=3, labels=['Low', 'Medium', 'High'])

    # División estratificada
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=config.TEST_SIZE, random_state=RANDOM_SEED, stratify=y_bins
    )

    print("📊 DIVISIÓN DE DATOS")
    print("="*60)
    print(f"Total de características: {X.shape[1]}")
    print(f"Total de registros: {len(X)}")
    print(f"Entrenamiento: {len(X_train)} registros ({len(X_train)/len(X)*100:.1f}%)")
    print(f"Prueba: {len(X_test)} registros ({len(X_test)/len(X)*100:.1f}%)")

    # Escalar características
    if preprocessor:
        X_train_scaled, X_test_scaled = preprocessor.scale_features(X_train, X_test)
        trainer = DiabetesModelTrainer()
        trainer.preprocessor = preprocessor
    else:
        from data_preprocessor import DiabetesDataPreprocessor
        temp_preprocessor = DiabetesDataPreprocessor()
        X_train_scaled, X_test_scaled = temp_preprocessor.scale_features(X_train, X_test)
        trainer = DiabetesModelTrainer()
        trainer.preprocessor = temp_preprocessor

    # Entrenar modelos
    results_df = trainer.train_all_models(X_train_scaled, y_train, X_test_scaled, y_test)

    # Obtener mejor modelo
    trainer.get_best_model()

    # Guardar modelos
    saved_files = trainer.save_models(feature_columns)

    print("\n💾 Archivos guardados:")
    for name, path in saved_files.items():
        print(f"   {name}: {path}")

    return trainer