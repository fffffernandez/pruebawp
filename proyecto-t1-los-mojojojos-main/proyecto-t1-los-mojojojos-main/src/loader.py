"""
Cargador del modelo de Machine Learning.
Maneja la carga del pipeline entrenado y las predicciones.
Obtiene temperatura automáticamente desde Open-Meteo o históricos.
"""
import pandas as pd
from joblib import load
from pathlib import Path
from datetime import datetime
from typing import Dict, Tuple

# Importar configuración (ruta del modelo y datos)
from src.config import MODEL_PATH, CSV_DATA_PATH

# Importar build_production_pipeline para construir el pipeline dinámicamente
from src.utils.preprocessing import build_production_pipeline

# Importar servicio de temperatura
from src.services.weather_service import get_temperature_for_prediction

# Importar servicio de datos históricos
from src.services.historical_service import get_historical_consumption

# --- 1. CONFIGURACIÓN Y CARGA GLOBAL DEL MODELO ---

GLOBAL_MODEL = None
GLOBAL_PIPELINE = None  # Pipeline entrenado (fitted)

def load_model():
    """
    Carga el modelo entrenado y construye el pipeline entrenado (fitted) una sola vez.
    Usa una muestra de datos históricos para entrenar los transformadores del pipeline.
    Se ejecuta automáticamente al importar este módulo (inicio de FastAPI).
    """
    global GLOBAL_MODEL, GLOBAL_PIPELINE
    if GLOBAL_MODEL is None:
        try:
            if not MODEL_PATH.exists():
                print(f"⚠️ ADVERTENCIA: Modelo no encontrado en {MODEL_PATH}")
                print(f"   La API funcionará, pero las predicciones no estarán disponibles.")
                print(f"   Entrena y guarda el modelo primero.")
                return
            
            # 1. Cargar el modelo
            GLOBAL_MODEL = load(MODEL_PATH)
            print(f"✅ Modelo Random Forest cargado desde: {MODEL_PATH}")
            
            # 2. Construir el pipeline con el modelo
            pipeline = build_production_pipeline(GLOBAL_MODEL)
            
            # 3. Entrenar el pipeline con datos históricos (necesario para OneHotEncoder y Scaler)
            if CSV_DATA_PATH.exists():
                print(f"🔧 Entrenando transformadores del pipeline con datos históricos...")
                
                # Leer TODO el CSV limpio para asegurar que el OneHotEncoder aprende TODAS las zonas
                df_sample = pd.read_csv(CSV_DATA_PATH)  # SIN nrows - leer todo
                print(f"   Cargadas {len(df_sample)} filas para entrenamiento del pipeline")
                
                # Preparar timestamp si no existe
                if 'timestamp' not in df_sample.columns and 'fecha' in df_sample.columns and 'hora' in df_sample.columns:
                    df_sample['timestamp'] = pd.to_datetime(df_sample['fecha'].astype(str) + ' ' + df_sample['hora'].astype(str))
                
                # Verificar columnas necesarias
                required_cols = ['timestamp', 'zone_name', 'temperature']
                if all(col in df_sample.columns for col in required_cols):
                    X_sample = df_sample[required_cols].copy()
                    y_sample = df_sample['consumption_kwh'] if 'consumption_kwh' in df_sample.columns else pd.Series([0] * len(df_sample))
                    
                    # Entrenar el pipeline completo (fit_transform en los transformadores)
                    # Esto entrenará: ProductionDataCleaner -> FeatureEngineer -> ColumnTransformer
                    # El ColumnTransformer aprenderá todas las zonas para OneHotEncoding
                    pipeline[:-1].fit(X_sample, y_sample)  # Todos los pasos excepto el modelo
                    
                    GLOBAL_PIPELINE = pipeline
                    print(f"✅ Pipeline entrenado correctamente")
                    
                    # Verificar que genera las features correctas
                    X_transformed = pipeline[:-1].transform(X_sample.head(1))
                    expected_features = GLOBAL_MODEL.n_features_in_ if hasattr(GLOBAL_MODEL, 'n_features_in_') else 'desconocido'
                    print(f"   Features generadas: {X_transformed.shape[1]} (el modelo espera {expected_features})")
                    
                else:
                    print(f"⚠️ CSV no tiene las columnas necesarias: {required_cols}")
                    print(f"   Columnas disponibles: {list(df_sample.columns)}")
                    return
            else:
                print(f"⚠️ CSV de datos no encontrado en {CSV_DATA_PATH}")
                return
            
        except ImportError as e:
            print(f"❌ ERROR: Fallo al importar las clases del pipeline.")
            print(f"   Verifica que 'src/utils/preprocessing.py' tenga las clases correctas.")
            print(f"   Error: {e}")
        except Exception as e:
            print(f"❌ ERROR al cargar el modelo: {e}")
            import traceback
            traceback.print_exc()

# Asegurar que el modelo se cargue al importar este módulo
load_model()
# --- 2. FUNCIÓN DE PREDICCIÓN PARA LAS VISTAS ---

async def get_prediction(timestamp_str: str, zone_name: str) -> Tuple[Dict, int]:
    """
    Realiza una predicción completa siguiendo el flujo:
    1. Recibe timestamp y zona del usuario
    2. Obtiene temperatura de Open-Meteo o históricos
    3. Transforma los datos con el pipeline
    4. Devuelve la predicción del modelo
    5. Intenta obtener datos reales históricos si existen
    
    Args:
        timestamp_str: Fecha y hora en formato ISO (ej: "2025-12-25T20:00:00")
        zone_name: Nombre de la zona (ej: "ALBAICIN")
    
    Returns:
        Tuple[Dict, int]: (diccionario con resultado, código HTTP)
    """
    if GLOBAL_PIPELINE is None:
        return {
            "error": "El modelo de predicción no está disponible.",
            "details": "El pipeline no se ha cargado correctamente. Verifica que exista el archivo .joblib"
        }, 500
    
    try:
        # 1. Parsear timestamp
        try:
            target_datetime = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
        except ValueError as e:
            return {
                "error": "Formato de fecha inválido",
                "details": f"Use formato ISO: YYYY-MM-DDTHH:MM:SS. Error: {e}"
            }, 400
        
        # 2. Obtener temperatura automáticamente
        temp_info = await get_temperature_for_prediction(target_datetime)
        temperature = temp_info["temperature"]
        temp_source = temp_info["source"]
        
        # 3. Preparar datos para el modelo
        input_data = {
            "timestamp": timestamp_str,
            "zone_name": zone_name,
            "temperature": temperature
        }
        
        # 4. Convertir a DataFrame (requerido por el pipeline)
        input_df = pd.DataFrame([input_data])
        
        # DEBUG: Ver qué datos recibe el modelo
        print(f"🔍 INPUT datos originales: timestamp={timestamp_str[:19]}, zona={zone_name}, temp={temperature:.1f}°C")
        
        # 5. Ejecutar la predicción con el pipeline global ya entrenado
        # El pipeline ejecuta: ProductionDataCleaner -> FeatureEngineer -> ColumnTransformer -> Modelo
        
        # DEBUG: Transformar sin predicción para ver las features
        X_transformed = GLOBAL_PIPELINE[:-1].transform(input_df)
        print(f"🔍 FEATURES generadas: {X_transformed.shape}")
        print(f"   Primeros 5 (numéricas): {X_transformed[0][:5]}")
        print(f"   Últimos 20 (zonas one-hot): {X_transformed[0][-20:]}")
        print(f"   Suma de zonas (debe ser 1): {X_transformed[0][-20:].sum()}")
        
        prediction_result = GLOBAL_PIPELINE.predict(input_df)
        
        print(f"🎯 PREDICCIÓN: {prediction_result[0]:.2f} kWh")
        
        # 6. Formatear la salida
        if hasattr(prediction_result, 'ndim') and prediction_result.ndim > 1:
            prediction_value = prediction_result.tolist()
        else:
            prediction_value = float(prediction_result[0])
        
        # 7. Intentar obtener datos reales históricos
        real_consumption = get_historical_consumption(target_datetime, zone_name)
        
        result = {
            "prediction": prediction_value,
            "timestamp": timestamp_str,
            "zone_name": zone_name,
            "temperature": temperature,
            "temperature_source": temp_source,
            "real_consumption": real_consumption  # Siempre incluir (puede ser None/null)
        }
        
        return result, 200

    except Exception as e:
        print(f"❌ Error durante la predicción: {e}")
        import traceback
        traceback.print_exc()
        return {
            "error": "Fallo en el pipeline de predicción.",
            "details": str(e)
        }, 400


def is_model_loaded() -> bool:
    """
    Verifica si el modelo y pipeline están cargados correctamente.
    Útil para el health check.
    """
    return GLOBAL_PIPELINE is not None

