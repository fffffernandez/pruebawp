# 📘 Sistema de Predicción Energética "Granada Smart City"

## 🎯 Descripción del Proyecto

Proyecto de Data Science para el **Ayuntamiento de Granada** que transforma datos históricos de consumo energético en un sistema inteligente capaz de anticipar la demanda eléctrica horaria de la ciudad.

Este proyecto forma parte de la estrategia *Smart City* de Granada y abarca el ciclo de vida completo del dato: desde la limpieza de datos sucios hasta el despliegue de una aplicación web funcional con modelos de Machine Learning.

## 🎯 Objetivos

1. **Limpiar y auditar** datos históricos de sensores de consumo eléctrico (2015-2025)
2. **Desarrollar modelos predictivos** para anticipar la demanda energética horaria
3. **Crear una aplicación web** que permita al Ayuntamiento consultar KPIs y simular escenarios futuros
4. **Optimizar la gestión energética** de la ciudad mediante análisis de datos

## 📊 Dataset

El proyecto trabaja con `consumo_granada.csv`, que contiene registros horarios de sensores distribuidos por diferentes barrios de Granada.

**Variables:**
- `timestamp`: Fecha y hora de la lectura
- `zone_id`: Identificador numérico del barrio
- `zone_name`: Nombre del barrio
- `temperature`: Temperatura ambiente (°C)
- `consumption_kwh`: Consumo eléctrico real (Variable Objetivo)

⚠️ **Nota**: Los datos contienen errores reales de sensores que deben ser detectados y tratados.

## 🔬 Metodología

### Fase 1: Ingeniería y Calidad del Dato
- Detección de valores imposibles y faltantes
- Tratamiento de inconsistencias
- Documentación de decisiones de limpieza

### Fase 2: Feature Engineering
- Extracción de características temporales (hora, día, mes, festivos)
- Ingeniería de variables climáticas
- Codificación de variables categóricas

### Fase 3: Benchmark de Modelos
Comparación rigurosa de algoritmos:
1. Dummy Regressor (baseline)
2. K-Nearest Neighbors (KNN)
3. Support Vector Regressor (SVR)
4. Decision Tree Regressor
5. Random Forest Regressor
6. **Gradient Boosting Regressor** (investigación)

### Fase 4: Validación Robusta
- Validación Cruzada de 5 particiones (5-Fold CV)
- Métricas: MAE, RMSE, R²

## 📈 Métricas de Referencia (5-Fold CV)

| Modelo | MAE (kWh) | RMSE (kWh) | Interpretación |
|--------|-----------|------------|----------------|
| DummyRegressor | ~1114.18 | ~1462.52 | Línea base |
| DecisionTree | ~428.98 | ~632.06 | Aceptable |
| **GradientBoosting** | **~218.58** | **~342.82** | Objetivo |

## 🚀 Aplicación Web

Plataforma web con 3 módulos principales:

### 1. Cuadro de Mando Estratégico
- KPIs globales (consumo total, promedio, picos)
- Ranking de zonas por consumo
- Correlación temperatura vs consumo

### 2. Simulador de Demanda "What-If"
- Interfaz para simular escenarios futuros
- Predicción en tiempo real basada en:
  - Fecha y hora objetivo
  - Zona/Barrio
  - Temperatura prevista

### 3. Auditoría del Modelo
- Comparación visual: Consumo Real vs Predicción
- Selector de periodo histórico
- Validación gráfica del rendimiento

## 🛠️ Tecnologías

- **Backend**: FastAPI, uvicorn
- **Base de Datos**: PostgreSQL (psycopg2-binary, SQLAlchemy)
- **ML/Data Science**: scikit-learn, pandas, numpy
- **Visualización**: matplotlib, seaborn, plotly
- **Frontend**: Bootstrap 5, Jinja2 Templates

## 📁 Estructura del Proyecto

```
proyecto-granada-smart-city/
│
├── data/                               # NO subir a GitHub (poner en .gitignore)
│   ├── raw/                            # El "consumo_granada.csv" original (sucio)
│   └── processed/                      # CSV limpio tras la Fase 1 (para entrenar modelos)
│
├── database/                           # Scripts para montar la BBDD PostgreSQL
│   ├── init_db.sql                     # Script para crear tablas e insertar datos limpios
│   └── queries.sql                     # Queries útiles (KPIs, medias) para probar antes de ir a código
│
├── models/                             # Almacén de modelos serializados (pickle/joblib)
│   ├── decision_tree.ipynb             # Notebook de Decision Tree Regressor
│   ├── doomy.ipynb                     # Notebook de Dummy Regressor (baseline)
│   ├── K_Nearest_Neighbors.ipynb       # Notebook de K-Nearest Neighbors
│   ├── random_forest.ipynb             # Notebook de Random Forest Regressor
│   ├── support-Vector-Machines.ipynb   # Notebook de Support Vector Regressor
│   └── scaler.pkl                      # Si usáis escaladores, guardadlos también aquí
│
├── notebooks/                          # Zona de Experimentación (Data Science)
│   ├── 01_data_cleaning.ipynb          # Fase 1: Limpieza y Calidad
│   ├── 02_data_visualization.ipynb     # Fase 2: Análisis y Feature Engineering
│   ├── 03_eda_features.ipynb           # Fase 2: Análisis y Feature Engineering
│   ├── 04_modeling_bench.ipynb         # Fase 3 y 4: Comparativa de modelos
│   └── sandbox/                        # Carpetas personales para pruebas
│
├── src/                                # Código Fuente de la Aplicación Web (FastAPI)
│   ├── main.dj                         # Punto de entrada de la App (FastAPI)
│   ├── config.dj                       # Variables de entorno (user/pass de PostgreSQL)
│   ├── database.dj                     # Conexión a PostgreSQL (SQLAlchemy o psycopg2)
|   |
|   ├── model/                          # Estructura a medio hacer de Django (Hay que reestructurar y ajustar todo bien)
│   │   ├── loader.py                   # Contiene la función get_prediction() que toma el diccionario de datos, lo convierte en un DataFrame,  
│   │   │                                  lo pasa al pipeline (FeatureEngineer -> StandardScaler -> Modelo) y devuelve el resultado numérico.
│   │   └── views.py                    # Parte funcionamiento API
│   │
│   ├── routes/                         # Endpoints de la API
│   │   ├── dashboard.dj                # Lógica pestaña 1: KPIs y Gráficos SQL
│   │   ├── prediction.dj               # Lógica pestaña 2: Simulador (Carga modelo)
│   │   └── audit.dj                    # Lógica pestaña 3: Comparativa Real vs Pred
│   │
│   ├── utils/                          # Funciones compartidas (IMPORTANTE)
│   │   └── preprocessing.dj            # La MISMA función de limpieza usada en notebooks y app (modificada por Pablo, contiene limpieza y pipeline encapsulada)
│   │
│   ├── static/                         # CSS, Imágenes, logos del ayuntamiento
│   │   └── style.css
│   └── templates/                      # HTMLs (Jinja2) para las vistas web
│       ├── base.html                   # Plantilla base con Bootstrap
│       ├── dashboard.html              # Pestaña 1: Cuadro de Mando
│       └── prediction.html             # Pestaña 2: Simulador What-If
│
├── .gitignore                          # Ignorar: data/, .env, __pycache__, .DS_Store
├── requirements.txt                    # Librerías: pandas, scikit-learn, fastapi, uvicorn, psycopg2-binary, sqlalchemy
└── README.md                           # Documentación para la defensa
```

## 📝 Notebooks de Desarrollo

1. **01_data_cleaning.ipynb**: Limpieza y auditoría de datos
2. **02_eda_features.ipynb**: Análisis exploratorio y creación de features
3. **03_modeling_bench.ipynb**: Entrenamiento y comparación de modelos

## 👥 Equipo

- **Miembro 1**: [Luis] - Desarrollador.
- **Miembro 2**: [Pablo] - Desarrollador.
- **Miembro 3**: [Pascual] - Desarrollador.
- **Miembro 4**: [Ruben] - Desarrollador.

## 📄 Licencia

Este proyecto es parte del Máster en Big Data y Data Science de STEMgranada - CEIABD 2024-2025.

---

**Desarrollado para**: Ayuntamiento de Granada - Iniciativa Smart City  
**Curso**: Máster en Big Data y Data Science 2024-2025  
**Equipo**: Los Mojojojos.


# Para mergear la rama 
**git merge origin/develop**

---

# Instalar venv
**python -m venv venv**

# Activar entorno
**source venv/Scripts/activate**

# Instalar Requirements
**pip install -r requirements.txt**