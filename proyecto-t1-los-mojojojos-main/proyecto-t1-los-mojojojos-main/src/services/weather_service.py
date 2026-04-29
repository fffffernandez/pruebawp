"""
Servicio para obtener temperatura desde Open-Meteo API.
API gratuita, sin necesidad de token.
Documentación: https://open-meteo.com/en/docs
"""
import httpx
from datetime import datetime, timedelta
from typing import Optional, Dict

# Coordenadas de Granada, España
GRANADA_LATITUDE = 37.1773
GRANADA_LONGITUDE = -3.5986


async def get_temperature_from_open_meteo(
    target_datetime: datetime,
    latitude: float = GRANADA_LATITUDE,
    longitude: float = GRANADA_LONGITUDE
) -> Optional[float]:
    """
    Obtiene la temperatura para una fecha/hora específica desde Open-Meteo.
    
    Open-Meteo proporciona:
    - Forecast: Hasta 16 días en el futuro
    - Historical: Hasta 5 días en el pasado (past_days=5)
    
    Args:
        target_datetime: Fecha y hora objetivo
        latitude: Latitud (default: Granada)
        longitude: Longitud (default: Granada)
    
    Returns:
        Temperatura en °C o None si no está disponible
    """
    try:
        now = datetime.now()
        days_difference = (target_datetime.date() - now.date()).days
        
        # Construir URL según si es pasado o futuro
        if days_difference < 0:
            # Fecha en el pasado (últimos 5 días disponibles)
            past_days = abs(days_difference)
            if past_days > 5:
                # Open-Meteo solo tiene últimos 5 días gratis
                return None
            
            url = (
                f"https://api.open-meteo.com/v1/forecast?"
                f"latitude={latitude}&longitude={longitude}"
                f"&past_days={past_days}"
                f"&hourly=temperature_2m"
                f"&timezone=auto"
            )
        else:
            # Fecha en el futuro (próximos 16 días disponibles)
            if days_difference > 16:
                # Open-Meteo solo tiene 16 días de forecast gratis
                return None
            
            url = (
                f"https://api.open-meteo.com/v1/forecast?"
                f"latitude={latitude}&longitude={longitude}"
                f"&hourly=temperature_2m"
                f"&timezone=auto"
            )
        
        # Hacer petición a la API
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=10.0)
            response.raise_for_status()
            data = response.json()
        
        # Extraer temperatura para la hora específica
        if "hourly" not in data or "time" not in data["hourly"]:
            return None
        
        times = data["hourly"]["time"]
        temperatures = data["hourly"]["temperature_2m"]
        
        # Buscar la hora exacta
        target_str = target_datetime.strftime("%Y-%m-%dT%H:00")
        
        if target_str in times:
            index = times.index(target_str)
            temp = temperatures[index]
            print(f"✅ Temperatura obtenida de Open-Meteo: {temp}°C para {target_str}")
            return float(temp)
        
        # Si no encuentra la hora exacta, buscar la más cercana
        # (por si hay diferencia de minutos)
        target_hour = target_datetime.strftime("%Y-%m-%dT%H")
        for i, time_str in enumerate(times):
            if time_str.startswith(target_hour):
                temp = temperatures[i]
                print(f"✅ Temperatura obtenida (hora cercana): {temp}°C para {time_str}")
                return float(temp)
        
        return None
        
    except httpx.HTTPError as e:
        print(f"❌ Error HTTP al consultar Open-Meteo: {e}")
        return None
    except Exception as e:
        print(f"❌ Error obteniendo temperatura de Open-Meteo: {e}")
        return None


async def get_temperature_for_prediction(target_datetime: datetime) -> Dict:
    """
    Función asíncrona para obtener temperatura.
    Determina si usar Open-Meteo o datos históricos.
    
    Args:
        target_datetime: Fecha y hora objetivo
    
    Returns:
        Dict con: {"temperature": float, "source": str}
    """
    # Intentar obtener de Open-Meteo
    temp = await get_temperature_from_open_meteo(target_datetime)
    
    if temp is not None:
        return {
            "temperature": temp,
            "source": "open-meteo"
        }
    
    # Si no está disponible en Open-Meteo, usar históricos
    from .historical_service import get_historical_temperature
    
    historical_temp = get_historical_temperature(target_datetime)
    
    if historical_temp is not None:
        return {
            "temperature": historical_temp,
            "source": "historical_average"
        }
    
    # Si tampoco hay históricos, usar temperatura promedio de Granada
    print("⚠️ No se pudo obtener temperatura, usando promedio de Granada")
    return {
        "temperature": 15.5,  # Temperatura promedio anual de Granada
        "source": "default_average"
    }
