"""
Aplicación principal FastAPI - Granada Smart City
Sistema de Predicción Energética
Sin base de datos, con temperatura automática.
"""
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path

# Importar configuración
from src.config import STATIC_DIR, TEMPLATES_DIR

# Importar routers
from src.routes import prediction_router
from src.routes.dashboard import router as dashboard_router

# Importar funciones de verificación
from src.loader import is_model_loaded
from src.services.historical_service import get_temperature_statistics

# ============================================
# CREAR LA APLICACIÓN FASTAPI
# ============================================

app = FastAPI(
    title="Granada Smart City - Predicción Energética",
    description="API REST para predicción de consumo energético en Granada con temperatura automática",
    version="2.0.0",
    docs_url="/docs",  # Swagger UI en /docs
    redoc_url="/redoc"  # ReDoc en /redoc
)

# ============================================
# CONFIGURAR CORS (para permitir peticiones desde JavaScript)
# ============================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especifica dominios concretos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================
# MONTAR ARCHIVOS ESTÁTICOS Y TEMPLATES
# ============================================

app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

# ============================================
# INCLUIR ROUTERS (MÓDULOS DE LA API)
# ============================================

# Dashboard - Ruta base: /
app.include_router(
    dashboard_router,
    tags=["Dashboard"]
)

# Predicción (sistema principal) - Ruta base: /prediction
app.include_router(
    prediction_router,
    prefix="/prediction",
    tags=["Predicción"]
)

# ============================================
# RUTAS PRINCIPALES
# ============================================

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """
    Ruta raíz: redirige al dashboard.
    """
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/dashboard")


@app.get("/health")
async def health_check():
    """
    Health check general de la aplicación.
    Verifica estado del modelo y disponibilidad de datos históricos.
    """
    model_loaded = is_model_loaded()
    
    # Verificar si el CSV está disponible
    csv_path = Path(__file__).resolve().parent.parent / "data" / "processed" / "consumo_granada_cleaned.csv"
    csv_available = csv_path.exists()
    
    status = "healthy" if (model_loaded and csv_available) else "degraded"
    
    response = {
        "status": status,
        "model": "loaded" if model_loaded else "not_loaded",
        "csv_data": "available" if csv_available else "missing",
        "message": "API operativa" if status == "healthy" else "Algunos servicios no disponibles"
    }
    
    # Añadir estadísticas de temperatura si el CSV está disponible
    if csv_available:
        stats = get_temperature_statistics()
        if stats:
            response["temperature_stats"] = stats
    
    return response


@app.get("/api/info")
async def api_info():
    """
    Información general de la API.
    """
    return {
        "name": "Granada Smart City API",
        "version": "2.0.0",
        "description": "Sistema de Predicción Energética con temperatura automática",
        "features": [
            "Predicción de consumo eléctrico",
            "Obtención automática de temperatura (Open-Meteo API)",
            "Fallback a datos históricos (últimos 5 años)",
            "Sin necesidad de base de datos"
        ],
        "endpoints": {
            "prediction": "/prediction",
            "zones": "/prediction/api/zones",
            "predict": "/prediction/api/predict",
            "docs": "/docs",
            "health": "/health"
        },
        "temperature_sources": {
            "primary": "Open-Meteo API (próximos 16 días + últimos 5 días)",
            "fallback": "Media histórica de últimos 5 años",
            "default": "Temperatura promedio de Granada (15.5°C)"
        }
    }


# ============================================
# MANEJADOR DE ERRORES
# ============================================

@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    """
    Manejador personalizado para errores 404.
    """
    return JSONResponse(
        status_code=404,
        content={
            "error": "Endpoint no encontrado",
            "path": str(request.url),
            "message": "Verifica la documentación en /docs"
        }
    )


@app.exception_handler(500)
async def internal_error_handler(request: Request, exc):
    """
    Manejador personalizado para errores 500.
    """
    return JSONResponse(
        status_code=500,
        content={
            "error": "Error interno del servidor",
            "message": "Contacta con el administrador del sistema"
        }
    )


# ============================================
# EVENTOS DE INICIO/APAGADO
# ============================================

@app.on_event("startup")
async def startup_event():
    """
    Se ejecuta al iniciar la aplicación.
    """
    print("\n" + "="*60)
    print("🚀 Granada Smart City API v2.0 - Iniciando...")
    print("="*60)
    
    # Verificar modelo
    model_status = "✅" if is_model_loaded() else "❌"
    print(f"{model_status} Modelo de Machine Learning")
    if not is_model_loaded():
        print("   ⚠️ Modelo no encontrado. Colócalo en: data/models/random_forest_model_1.joblib")
    
    # Verificar CSV
    csv_path = Path(__file__).resolve().parent.parent / "data" / "processed" / "consumo_granada_cleaned.csv"
    csv_status = "✅" if csv_path.exists() else "❌"
    print(f"{csv_status} Datos históricos CSV")
    if not csv_path.exists():
        print(f"   ⚠️ CSV no encontrado en: {csv_path}")
    
    print("="*60)
    print("📡 Servidor disponible en: http://127.0.0.1:8000")
    print("📚 Documentación Swagger: http://127.0.0.1:8000/docs")
    print("🌡️ Temperatura automática: Open-Meteo + Históricos")
    print("="*60 + "\n")


@app.on_event("shutdown")
async def shutdown_event():
    """
    Se ejecuta al apagar la aplicación.
    """
    print("\n🛑 Granada Smart City API - Apagando...")


