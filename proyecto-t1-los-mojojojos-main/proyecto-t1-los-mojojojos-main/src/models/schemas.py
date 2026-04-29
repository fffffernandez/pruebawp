"""
Modelos Pydantic para validación de datos (schemas).
Define la estructura de los JSON que recibe y devuelve la API.
VERSIÓN SIMPLIFICADA: Solo predicción sin base de datos.
"""
from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional


# ============================================
# SCHEMAS PARA PREDICCIÓN
# ============================================

class PredictionInput(BaseModel):
    """
    Datos de entrada para hacer una predicción.
    El usuario solo proporciona fecha/hora y zona.
    La API obtiene la temperatura automáticamente.
    
    Ejemplo JSON:
    {
        "timestamp": "2025-12-25T20:00:00",
        "zone_name": "ALBAICIN"
    }
    """
    timestamp: str = Field(..., description="Fecha y hora en formato ISO (YYYY-MM-DDTHH:MM:SS)")
    zone_name: str = Field(..., description="Nombre del barrio/zona")
    
    @field_validator('zone_name')
    @classmethod
    def validate_zone_name(cls, v: str) -> str:
        """Normaliza el nombre de la zona a mayúsculas y sin espacios extra"""
        return v.strip().upper()
    
    @field_validator('timestamp')
    @classmethod
    def validate_timestamp(cls, v: str) -> str:
        """Valida que el timestamp sea un formato válido"""
        try:
            datetime.fromisoformat(v.replace('Z', '+00:00'))
            return v
        except ValueError:
            raise ValueError('Formato de fecha inválido. Use: YYYY-MM-DDTHH:MM:SS')
    
    class Config:
        json_schema_extra = {
            "example": {
                "timestamp": "2025-12-25T20:00:00",
                "zone_name": "ALBAICIN"
            }
        }


class PredictionOutput(BaseModel):
    """
    Respuesta de la API con la predicción.
    Incluye información sobre la fuente de la temperatura y consumo real si está disponible.
    """
    prediction: float = Field(..., description="Consumo predicho en kWh")
    timestamp: str = Field(..., description="Timestamp de la predicción")
    zone_name: str = Field(..., description="Zona consultada")
    temperature: float = Field(..., description="Temperatura utilizada")
    temperature_source: str = Field(..., description="Fuente de temperatura: open-meteo, historical_average, o default_average")
    real_consumption: Optional[float] = Field(None, description="Consumo real histórico si está disponible")
    
    class Config:
        json_schema_extra = {
            "example": {
                "prediction": 1234.56,
                "timestamp": "2025-12-25T20:00:00",
                "zone_name": "ALBAICIN",
                "temperature": 4.5,
                "temperature_source": "open-meteo",
                "real_consumption": 1150.30
            }
        }


# ============================================
# SCHEMAS PARA INFORMACIÓN DE ZONAS
# ============================================

class ZonesResponse(BaseModel):
    """
    Lista de zonas disponibles.
    """
    zones: list[str]
    count: int


# ============================================
# SCHEMAS GENÉRICOS
# ============================================

class HealthCheck(BaseModel):
    """
    Respuesta del health check.
    """
    status: str
    message: str
    model_loaded: bool
    csv_available: bool


class ErrorResponse(BaseModel):
    """
    Respuesta de error estándar.
    """
    error: str
    details: Optional[str] = None
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())

