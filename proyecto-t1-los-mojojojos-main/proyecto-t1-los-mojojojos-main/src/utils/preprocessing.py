import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer

# =====================================================================
# CONFIGURACIÓN DE COLUMNAS FINALES (Para el ColumnTransformer)
# =====================================================================

# Features numéricas que serán imputadas y escaladas (resultado del Feature Engineering)
FEATURES_TO_SCALE = [
    'temperature', 'temp_sq', 'hour_temp_interaction',
    'hour_sin', 'hour_cos',
    'month_sin', 'month_cos',
    'is_weekend', 'is_holiday', 'is_non_working',
    'day_of_week', 'day_of_month', 'month', 'hour', 'year'
] 

# Features categóricas para One-Hot Encoding (formato 'zona_Title_Case')
FEATURES_TO_ENCODE = ['zona'] 

# =====================================================================
# PASO 1: Data Cleaner e Interpolación (desde data_cleaning.ipynb)
# =====================================================================

class DataCleanerAndInterpolator(BaseEstimator, TransformerMixin):
    """Aplica limpieza inicial de zona, conversión de tipos e imputación por media histórica."""
    
    def __init__(self, historical_data=None):
        """
        Args:
            historical_data: DataFrame con datos históricos para calcular medias (opcional)
        """
        self.historical_data = historical_data
        self.historical_means = {}
    
    def fit(self, X, y=None):
        # Si tenemos datos históricos, calcular medias para imputación
        if self.historical_data is not None:
            data = self.historical_data.copy()
            
            # Asegurar que timestamp sea datetime
            if 'timestamp' in data.columns:
                data['timestamp'] = pd.to_datetime(data['timestamp'], errors='coerce', utc=True)
                data['month'] = data['timestamp'].dt.month
                data['day_of_month'] = data['timestamp'].dt.day
                data['hour'] = data['timestamp'].dt.hour
            
            # Limpiar zone_name
            if 'zone_name' in data.columns:
                data['zone_name'] = data['zone_name'].str.strip().str.replace(' ', '_').str.title()
                data['zona'] = 'zona_' + data['zone_name']
            
            # Calcular medias por (zona, month, day_of_month, hour)
            for col in ['consumption_kwh', 'temperature']:
                if col in data.columns:
                    self.historical_means[f'{col}_detailed'] = data.groupby(
                        ['zona', 'month', 'day_of_month', 'hour']
                    )[col].mean()
                    
                    # Fallback: media por (zona, hour)
                    self.historical_means[f'{col}_simple'] = data.groupby(
                        ['zona', 'hour']
                    )[col].mean()
        
        return self

    def transform(self, X):
        X_processed = X.copy()
        
        # 0. Asegurar que 'timestamp' sea datetime (con errores='coerce')
        if 'timestamp' in X_processed.columns:
            X_processed['timestamp'] = pd.to_datetime(X_processed['timestamp'], errors='coerce', utc=True)
        
        # 1. Limpieza de nombres de zona (strip, Title Case en cada palabra, prefijo 'zona_')
        if 'zone_name' in X_processed.columns:
            X_processed['zone_name'] = X_processed['zone_name'].str.strip()
            X_processed['zone_name'] = X_processed['zone_name'].str.replace(' ', '_')
            # Formato: zona_Albaicin_Alto (Title Case en cada parte, igual que el dataset)
            X_processed['zona'] = 'zona_' + X_processed['zone_name'].str.title()
            X_processed = X_processed.drop(columns=['zone_name'], errors='ignore')

        # 2. Formato de decimales para consumption_kwh (solo si la columna existe)
        if 'consumption_kwh' in X_processed.columns:
            X_processed['consumption_kwh'] = X_processed['consumption_kwh'].round(3)

        # 3. Separar fecha/hora (solo si es necesario para el FeatureEngineer)
        if 'timestamp' in X_processed.columns:
            X_processed['fecha'] = X_processed['timestamp'].dt.date
            X_processed['hora'] = X_processed['timestamp'].dt.time
            
        # 4. Imputación con media histórica (si tenemos datos históricos)
        if self.historical_means and 'timestamp' in X_processed.columns:
            X_processed['month'] = X_processed['timestamp'].dt.month
            X_processed['day_of_month'] = X_processed['timestamp'].dt.day
            X_processed['hour'] = X_processed['timestamp'].dt.hour
            
            for col in ['consumption_kwh', 'temperature']:
                if col in X_processed.columns and f'{col}_detailed' in self.historical_means:
                    # Intentar imputar con media detallada (zone, month, day, hour)
                    mask = X_processed[col].isna()
                    if mask.any():
                        X_processed.loc[mask, col] = X_processed.loc[mask].apply(
                            lambda row: self.historical_means[f'{col}_detailed'].get(
                                (row['zona'], row['month'], row['day_of_month'], row['hour']),
                                np.nan
                            ), axis=1
                        )
                        
                        # Fallback: media simple (zone, hour)
                        mask = X_processed[col].isna()
                        if mask.any():
                            X_processed.loc[mask, col] = X_processed.loc[mask].apply(
                                lambda row: self.historical_means[f'{col}_simple'].get(
                                    (row['zona'], row['hour']),
                                    np.nan
                                ), axis=1
                            )
            
        return X_processed

# =====================================================================
# PASO 2: Feature Engineering (desde eda_features.ipynb)
# =====================================================================

class FeatureEngineer(BaseEstimator, TransformerMixin):
    """
    Aplica la creación de features de tiempo, festivos y climáticas.
    """
    
    # Definición de festivos fijos (tomados del notebook)
    FESTIVOS_FIJOS = [
        (1, 1), (6, 1), (28, 2), (1, 5), (15, 8), 
        (12, 10), (1, 11), (6, 12), (8, 12), (25, 12) 
    ]
    
    def _es_festivo(self, timestamp):
        """Lógica para determinar si una fecha es festiva."""
        if pd.isna(timestamp):
            return 0
        m, d = timestamp.month, timestamp.day
        if (m, d) in self.FESTIVOS_FIJOS: return 1
        if m == 5 and d == 3: return 1 # Día de la Cruz
        if m == 9 and d == 15: return 1 # Virgen de las Angustias (Simplif.)
        return 0

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X_processed = X.copy()
        
        # La limpieza de timestamp ya ocurrió en el paso anterior
        if 'timestamp' not in X_processed.columns or X_processed['timestamp'].dtype == 'object':
             X_processed['timestamp'] = pd.to_datetime(X_processed['timestamp'], errors='coerce', utc=True)
             
        valid_ts = ~X_processed['timestamp'].isna()
        
        if 'timestamp' in X_processed.columns:
            ts = X_processed.loc[valid_ts, 'timestamp']
            
            # 2. Extracción de componentes temporales
            X_processed.loc[valid_ts, 'hour'] = ts.dt.hour
            X_processed.loc[valid_ts, 'month'] = ts.dt.month
            X_processed.loc[valid_ts, 'day_of_week'] = ts.dt.dayofweek
            X_processed.loc[valid_ts, 'day_of_month'] = ts.dt.day
            X_processed.loc[valid_ts, 'year'] = ts.dt.year

            # 3. Transformación Cíclica del Tiempo
            X_processed.loc[valid_ts, 'hour_sin'] = np.sin(2 * np.pi * X_processed.loc[valid_ts, 'hour'] / 24)
            X_processed.loc[valid_ts, 'hour_cos'] = np.cos(2 * np.pi * X_processed.loc[valid_ts, 'hour'] / 24)
            X_processed.loc[valid_ts, 'month_sin'] = np.sin(2 * np.pi * X_processed.loc[valid_ts, 'month'] / 12)
            X_processed.loc[valid_ts, 'month_cos'] = np.cos(2 * np.pi * X_processed.loc[valid_ts, 'month'] / 12)

            # 4. Variables de Calendario
            X_processed.loc[valid_ts, 'is_weekend'] = X_processed.loc[valid_ts, 'day_of_week'].isin([5, 6]).astype(int)
            X_processed['is_holiday'] = X_processed['timestamp'].apply(self._es_festivo)
            X_processed['is_non_working'] = ((X_processed['is_weekend'] == 1) | (X_processed['is_holiday'] == 1)).astype(int)

            # 5. Transformaciones Climáticas e Interacciones
            if 'temperature' in X_processed.columns:
                X_processed['temp_sq'] = X_processed['temperature'] ** 2
                # Interacción hora-temperatura (importante para el modelo)
                if 'hour' in X_processed.columns:
                    X_processed['hour_temp_interaction'] = X_processed['hour'] * X_processed['temperature']
            
            # Rellenar NaNs en features temporales/derivadas con 0
            cols_to_fill_zero = [
                'hour', 'month', 'day_of_week', 'day_of_month', 'year', 'is_weekend', 
                'is_holiday', 'is_non_working', 'temp_sq', 'hour_temp_interaction',
                'hour_sin', 'hour_cos', 'month_sin', 'month_cos'
            ]
            for col in cols_to_fill_zero:
                if col in X_processed.columns:
                    X_processed[col] = X_processed[col].fillna(0) 

        # 7. Borrado de columnas finales que no entran al modelo
        columnas_a_borrar = [
            'timestamp', 'zone_id', 'fecha', 'hora', 'consumption_kwh' # Borramos consumption_kwh si es la target
        ]
        
        # El redondeo selectivo se omite aquí ya que solo es cosmético.
        
        X_processed = X_processed.drop(columns=[col for col in columnas_a_borrar if col in X_processed.columns], errors='ignore')
        
        return X_processed

# =====================================================================
# PASO 3: Pipeline Simplificado para Producción (SIN Interpolación)
# =====================================================================

class ProductionDataCleaner(BaseEstimator, TransformerMixin):
    """
    Limpieza básica para predicciones en tiempo real (API).
    Usa Title Case con prefijo 'zona_' para coincidir con los datos de entrenamiento.
    """
    
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X_processed = X.copy()
        
        # 0. Convertir timestamp a datetime
        if 'timestamp' in X_processed.columns:
            X_processed['timestamp'] = pd.to_datetime(X_processed['timestamp'], errors='coerce', utc=True)
        
        # 1. Limpiar zona (strip, Title Case en cada palabra, prefijo 'zona_')
        if 'zone_name' in X_processed.columns:
            X_processed['zone_name'] = X_processed['zone_name'].str.strip()
            X_processed['zone_name'] = X_processed['zone_name'].str.replace(' ', '_')
            # Formato: zona_Albaicin_Alto (Title Case, igual que el dataset)
            X_processed['zona'] = 'zona_' + X_processed['zone_name'].str.title()
            X_processed = X_processed.drop(columns=['zone_name'], errors='ignore')

        # 2. Redondeo de consumption_kwh si existe
        if 'consumption_kwh' in X_processed.columns:
            X_processed['consumption_kwh'] = X_processed['consumption_kwh'].round(3)
        
        return X_processed

def build_production_pipeline(model):
    """
    Pipeline para predicciones en tiempo real (API).
    Replica exactamente el preprocesamiento de los notebooks.
    
    Entrada esperada: DataFrame con columnas [timestamp, zone_name, temperature]
    """
    
    # 1. Transformadores secundarios
    numerical_pipeline = Pipeline([
        ('imputer', SimpleImputer(strategy='mean')),  # Cambiado a 'mean' para aproximar media histórica
        ('scaler', StandardScaler())
    ])

    categorical_pipeline = Pipeline([
        ('imputer', SimpleImputer(strategy='constant', fill_value='zona_Desconocida')),  # Title Case
        ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False)) 
    ])

    # 2. Combinar en un ColumnTransformer
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numerical_pipeline, FEATURES_TO_SCALE),
            ('cat', categorical_pipeline, FEATURES_TO_ENCODE) 
        ],
        remainder='drop' 
    )

    # 3. Ensamblar el Pipeline para Producción
    production_pipeline = Pipeline([
        # Paso 1: Limpieza básica (title case, igual que notebook)
        ('cleaner', ProductionDataCleaner()),
        # Paso 2: Feature Engineering
        ('feature_engineer', FeatureEngineer()),
        # Paso 3: Transformación final
        ('preprocessor', preprocessor),
        # Paso 4: Modelo
        ('model', model)
    ])
    
    return production_pipeline