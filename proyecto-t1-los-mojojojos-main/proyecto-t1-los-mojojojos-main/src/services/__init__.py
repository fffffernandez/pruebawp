# Servicios externos
from .weather_service import get_temperature_for_prediction
from .historical_service import get_historical_temperature

__all__ = ["get_temperature_for_prediction", "get_historical_temperature"]
