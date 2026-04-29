"""
DOCUMENTACIÓN DE LA API - Granada Smart City
=============================================

## 📁 ESTRUCTURA COMPLETA

src/
├── main.py              ✅ Aplicación principal FastAPI
├── config.py            ✅ Configuración (lee .env)
├── database.py          ✅ Conexión PostgreSQL + queries útiles
├── loader.py            ✅ Carga del modelo ML
├── run.py               ✅ Script para iniciar servidor
│
├── models/
│   ├── __init__.py      ✅ Inicializador
│   └── schemas.py       ✅ Validación de datos (Pydantic)
│
├── routes/
│   ├── __init__.py      ✅ Exporta todos los routers
│   ├── dashboard.py     ✅ KPIs y gráficos
│   ├── prediction.py    ✅ Simulador de predicción
│   └── audit.py         ✅ Auditoría Real vs Predicción
│
├── utils/
│   └── preprocessing.py ✅ Pipeline de transformación
│
├── static/
│   └── style.css        ⚠️ Vacío (pendiente CSS)
│
└── templates/
    ├── base.html        ✅ Base con Bootstrap
    ├── dashboard.html   ⚠️ Básico (necesita JavaScript)
    └── prediction.html  ⚠️ Vacío (pendiente)

## 🚀 CÓMO USAR LA API

### 1. CONFIGURAR BASE DE DATOS

Edita el archivo `.env` con las credenciales que te den tus compañeros:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=granada_smart_city
DB_USER=postgres
DB_PASSWORD=tu_contraseña_real
```

### 2. INSTALAR DEPENDENCIAS

```bash
pip install -r requirements.txt
```

Nuevas dependencias añadidas:
- python-dotenv: Para leer el archivo .env
- sqlalchemy: Para conectar con PostgreSQL

### 3. INICIAR EL SERVIDOR

```bash
# Opción 1: Usar run.py
python src/run.py

# Opción 2: Usar uvicorn directamente
uvicorn src.main:app --reload --host 127.0.0.1 --port 8000
```

### 4. ACCEDER A LA API

- **Dashboard**: http://127.0.0.1:8000/
- **Documentación Swagger**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc
- **Health Check**: http://127.0.0.1:8000/health

## 📡 ENDPOINTS DISPONIBLES

### DASHBOARD (`/dashboard`)

```
GET  /dashboard/              → Vista HTML del dashboard
GET  /dashboard/api/kpis      → KPIs (consumo total, promedio, pico, temp)
GET  /dashboard/api/consumption-by-zone  → Consumo por zona
GET  /dashboard/api/temperature-vs-consumption  → Datos correlación
GET  /dashboard/api/hourly-consumption?hours=24  → Consumo últimas N horas
GET  /dashboard/api/health    → Health check del dashboard
```

### PREDICCIÓN (`/prediction`)

```
GET  /prediction/                → Vista HTML del simulador
POST /prediction/api/predict     → Hacer UNA predicción
POST /prediction/api/predict-batch  → Hacer MÚLTIPLES predicciones
GET  /prediction/api/model-status   → Estado del modelo
```

Ejemplo POST a `/prediction/api/predict`:
```json
{
  "timestamp": "2025-12-25T20:00:00",
  "zone_name": "ALBAICIN",
  "temperature": 4.5
}
```

Respuesta:
```json
{
  "prediction": 1234.56,
  "timestamp": "2025-12-25T20:00:00",
  "zone_name": "ALBAICIN",
  "temperature": 4.5
}
```

### AUDITORÍA (`/audit`)

```
GET  /audit/                → Vista HTML de auditoría
POST /audit/api/audit       → Comparar Real vs Predicción
GET  /audit/api/audit/summary?start_date=2024-02-01&end_date=2024-02-07  → Solo métricas
```

Ejemplo POST a `/audit/api/audit`:
```json
{
  "start_date": "2024-02-01",
  "end_date": "2024-02-07",
  "zone_name": "CENTRO"
}
```

Respuesta:
```json
{
  "start_date": "2024-02-01",
  "end_date": "2024-02-07",
  "zone_name": "CENTRO",
  "data": [
    {
      "timestamp": "2024-02-01T00:00:00",
      "real": 1200.5,
      "predicted": 1185.3
    },
    ...
  ],
  "mae": 218.58,
  "rmse": 342.82
}
```

## 🗄️ FUNCIONES DE BASE DE DATOS

El archivo `database.py` tiene queries listas para usar:

```python
from src.database import (
    get_kpis,                    # KPIs principales
    get_consumption_by_zone,     # Consumo por zona
    get_temperature_vs_consumption,  # Correlación temp-consumo
    get_hourly_consumption,      # Últimas N horas
    get_historical_data,         # Datos históricos para auditoría
    execute_query,               # Ejecutar query custom
    test_connection              # Probar conexión
)
```

## 🤖 MODELO DE MACHINE LEARNING

El archivo `loader.py` maneja el modelo:

```python
from src.loader import get_prediction, is_model_loaded

# Verificar si el modelo está cargado
if is_model_loaded():
    # Hacer predicción
    result, status = get_prediction({
        "timestamp": "2025-12-25T20:00:00",
        "zone_name": "CENTRO",
        "temperature": 10.5
    })
```

**IMPORTANTE**: El modelo debe estar guardado en:
```
database/models/final_prediction_pipeline.joblib
```

Si no existe, la API funcionará pero las predicciones no estarán disponibles.

## ⚠️ LO QUE FALTA POR HACER

### 1. Base de Datos
- [ ] Crear la base de datos PostgreSQL
- [ ] Crear la tabla `consumo_granada` con el esquema correcto
- [ ] Cargar los datos limpios desde `data/processed/`

### 2. Modelo ML
- [ ] Entrenar el mejor modelo en los notebooks
- [ ] Guardar el pipeline completo como `.joblib`
- [ ] Colocar en `database/models/final_prediction_pipeline.joblib`

### 3. Frontend
- [ ] Completar `prediction.html`
- [ ] Añadir JavaScript para hacer peticiones a la API
- [ ] Crear gráficos con Chart.js o Plotly
- [ ] Mejorar `style.css`

### 4. Testing
- [ ] Probar todos los endpoints
- [ ] Verificar que las queries SQL funcionen
- [ ] Testear predicciones con datos reales

## 🔧 COMANDOS ÚTILES

```bash
# Ver logs del servidor
python src/run.py

# Probar endpoint con curl
curl http://127.0.0.1:8000/health

# Probar predicción con curl
curl -X POST http://127.0.0.1:8000/prediction/api/predict \
  -H "Content-Type: application/json" \
  -d '{"timestamp":"2025-12-25T20:00:00","zone_name":"CENTRO","temperature":10.5}'

# Ver documentación interactiva
# Navega a: http://127.0.0.1:8000/docs
```

## 📞 COORDINACIÓN CON EL EQUIPO

**Para el compañero de Base de Datos:**
- Necesitas crear la tabla con estas columnas:
  - `timestamp` (TIMESTAMP)
  - `zone_id` (INTEGER)
  - `zone_name` (VARCHAR)
  - `temperature` (FLOAT)
  - `consumption_kwh` (FLOAT)

**Para el compañero de Modelos:**
- Guardar el pipeline completo (no solo el modelo)
- Usar `joblib.dump(pipeline, 'ruta/al/archivo.joblib')`
- El pipeline debe incluir: DataCleaner → FeatureEngineer → ColumnTransformer → Modelo

**Para el compañero de Frontend:**
- Los endpoints están listos
- Usa fetch() o axios para hacer peticiones
- Todos los endpoints devuelven JSON

## 🎉 RESUMEN

✅ **API completamente lista**
✅ **Estructura correcta FastAPI**
✅ **PostgreSQL configurado**
✅ **Modelos Pydantic para validación**
✅ **Routers organizados**
✅ **Documentación Swagger automática**

🔌 **Solo falta conectar:**
1. La base de datos (tus compañeros)
2. El modelo entrenado (guardar el .joblib)
3. El frontend (JavaScript + HTML)
