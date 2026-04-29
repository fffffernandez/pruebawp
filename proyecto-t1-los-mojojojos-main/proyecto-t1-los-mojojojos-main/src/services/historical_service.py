"""
Servicio para obtener temperatura histórica desde el CSV limpio.
Calcula la temperatura media de los últimos 5 años para una fecha/hora específica.
También consulta consumo real desde PostgreSQL.
"""
import pandas as pd
from datetime import datetime
from pathlib import Path
from typing import Optional
import sys
import os

# Importar database para consultas PostgreSQL
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from database import execute_query

# Ruta al CSV limpio
CSV_PATH = Path(__file__).resolve().parent.parent.parent / "data" / "processed" / "consumo_granada_cleaned.csv"


def get_historical_temperature(target_datetime: datetime, zone_name: Optional[str] = None) -> Optional[float]:
    """
    Obtiene la temperatura media histórica de los últimos 5 años
    para una fecha/hora y zona específicas.
    
    Args:
        target_datetime: Fecha y hora objetivo
        zone_name: Nombre de la zona (opcional). Si no se proporciona, calcula media de todas las zonas.
    
    Returns:
        Temperatura media en °C o None si no hay datos
    
    Ejemplo:
        Si pides 25 de diciembre a las 20:00, busca todos los 25 de diciembre a las 20:00
        de los últimos 5 años y devuelve la media.
    """
    try:
        # Verificar que el CSV existe
        if not CSV_PATH.exists():
            print(f"⚠️ CSV no encontrado en: {CSV_PATH}")
            return None
        
        # Leer CSV
        df = pd.read_csv(CSV_PATH)
        
        # Asegurar que timestamp es datetime
        if 'timestamp' not in df.columns:
            print("❌ CSV no tiene columna 'timestamp'")
            return None
        
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Extraer mes, día y hora del target
        target_month = target_datetime.month
        target_day = target_datetime.day
        target_hour = target_datetime.hour
        
        # Filtrar por mes, día y hora
        mask = (
            (df['timestamp'].dt.month == target_month) &
            (df['timestamp'].dt.day == target_day) &
            (df['timestamp'].dt.hour == target_hour)
        )
        
        # Filtrar por zona si se proporciona
        if zone_name:
            if 'zone_name' in df.columns:
                # Normalizar nombre de zona
                zone_name_upper = zone_name.strip().upper()
                mask = mask & (df['zone_name'].str.upper() == zone_name_upper)
        
        filtered_df = df[mask]
        
        if filtered_df.empty or 'temperature' not in filtered_df.columns:
            print(f"⚠️ No hay datos históricos para {target_datetime.strftime('%d/%m a las %H:00')}")
            return None
        
        # Calcular media de temperatura
        mean_temp = filtered_df['temperature'].mean()
        
        if pd.isna(mean_temp):
            return None
        
        print(f"✅ Temperatura histórica (media 5 años): {mean_temp:.2f}°C para {target_datetime.strftime('%d/%m/%Y %H:00')}")
        print(f"   Basado en {len(filtered_df)} registros históricos")
        
        return float(mean_temp)
        
    except FileNotFoundError:
        print(f"❌ Archivo CSV no encontrado: {CSV_PATH}")
        return None
    except Exception as e:
        print(f"❌ Error leyendo datos históricos: {e}")
        return None


def get_available_zones() -> list:
    """
    Obtiene la lista de zonas disponibles en el CSV.
    Útil para el frontend (dropdown de zonas).
    
    Returns:
        Lista de nombres de zonas
    """
    try:
        if not CSV_PATH.exists():
            return []
        
        df = pd.read_csv(CSV_PATH)
        
        if 'zone_name' not in df.columns:
            return []
        
        zones = df['zone_name'].unique().tolist()
        return sorted(zones)
        
    except Exception as e:
        print(f"❌ Error obteniendo zonas: {e}")
        return []


def get_historical_consumption(target_datetime: datetime, zone_name: str) -> Optional[float]:
    """
    Obtiene el consumo real histórico desde PostgreSQL para una fecha/hora y zona específicas.
    Usa el MISMO formato de zona que el dashboard (zona_albaicin_alto, zona_pts_tecnologico, etc.)
    
    Args:
        target_datetime: Fecha y hora exacta
        zone_name: Nombre de la zona del frontend (ej: "ALBAICIN" o "Albaicin_Alto")
    
    Returns:
        Consumo en kWh o None si no hay datos
    """
    try:
        # Mapeo de zonas: del frontend → columna PostgreSQL
        # El frontend envía nombres como "ALBAICIN", "CENTRO_CATEDRAL", "PTS_TECNOLOGICO"
        # PostgreSQL tiene columnas como "zona_albaicin_alto", "zona_centro_catedral", "zona_pts_tecnologico"
        
        # Normalizar: minúsculas, reemplazar espacios por guiones bajos
        zone_normalized = zone_name.strip().lower().replace(' ', '_')
        
        # Construir nombre de columna: zona_ + nombre normalizado
        zona_column = f"zona_{zone_normalized}"
        
        # Extraer componentes de fecha para la consulta
        year = target_datetime.year
        month = target_datetime.month
        day = target_datetime.day
        hour = target_datetime.hour
        
        # Consulta a PostgreSQL (EXACTAMENTE igual que el dashboard)
        query = f"""
            SELECT consumption_kwh
            FROM consumo_granada
            WHERE {zona_column} = 1
              AND year = %s
              AND month = %s
              AND day_of_month = %s
              AND hour = %s
            LIMIT 1;
        """
        
        params = (year, month, day, hour)
        
        print(f"🔍 Buscando consumo real: {zona_column} | {year}/{month}/{day} {hour}:00")
        
        result = execute_query(query, params, fetch_one=True)
        
        if result and 'consumption_kwh' in result:
            consumption = float(result['consumption_kwh'])
            print(f"✅ Consumo real encontrado en BD: {consumption:.2f} kWh")
            return consumption
        else:
            print(f"⚠️ No hay datos reales para {zona_column} en {year}/{month:02d}/{day:02d} {hour:02d}:00")
            return None
        
    except Exception as e:
        print(f"❌ Error consultando BD: {e}")
        import traceback
        traceback.print_exc()
        return None


def get_temperature_statistics() -> dict:
    """
    Obtiene estadísticas generales de temperatura del CSV.
    Útil para validación y debugging.
    
    Returns:
        Dict con estadísticas (min, max, mean, std)
    """
    try:
        if not CSV_PATH.exists():
            return {}
        
        df = pd.read_csv(CSV_PATH)
        
        if 'temperature' not in df.columns:
            return {}
        
        return {
            "min": float(df['temperature'].min()),
            "max": float(df['temperature'].max()),
            "mean": float(df['temperature'].mean()),
            "std": float(df['temperature'].std()),
            "count": int(df['temperature'].count())
        }
        
    except Exception as e:
        print(f"❌ Error obteniendo estadísticas: {e}")
        return {}
