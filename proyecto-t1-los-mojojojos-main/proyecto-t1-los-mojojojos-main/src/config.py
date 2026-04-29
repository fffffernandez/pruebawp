"""
Configuración centralizada de la aplicación.
Lee las variables de entorno desde el archivo .env
Sin base de datos.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Obtener la ruta base del proyecto (directorio raíz)
BASE_DIR = Path(__file__).resolve().parent.parent

# Cargar variables de entorno desde .env
load_dotenv(BASE_DIR / ".env")

# ============================================
# CONFIGURACIÓN DE LA APLICACIÓN
# ============================================
APP_HOST = os.getenv("APP_HOST", "127.0.0.1")
APP_PORT = int(os.getenv("APP_PORT", "8000"))
DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "yes")

# ============================================
# CONFIGURACIÓN DEL MODELO ML
# ============================================
MODEL_PATH = BASE_DIR / os.getenv("MODEL_PATH", "data/models/random_forest_model_1.joblib")

# ============================================
# RUTAS DE ARCHIVOS
# ============================================
STATIC_DIR = BASE_DIR / "src" / "static"
TEMPLATES_DIR = BASE_DIR / "src" / "templates"
CSV_DATA_PATH = BASE_DIR / "data" / "processed" / "consumo_granada_cleaned.csv"

# ============================================
# COORDENADAS DE GRANADA (para Open-Meteo API)
# ============================================
GRANADA_LATITUDE = 37.1773
GRANADA_LONGITUDE = -3.5986

print(f"✅ Configuración cargada:")
print(f"   - Servidor: {APP_HOST}:{APP_PORT}")
print(f"   - Modo Debug: {DEBUG}")
print(f"   - Ruta del modelo: {MODEL_PATH}")
print(f"   - CSV de datos: {CSV_DATA_PATH}")
print(f"   - Coordenadas Granada: ({GRANADA_LATITUDE}, {GRANADA_LONGITUDE})")

