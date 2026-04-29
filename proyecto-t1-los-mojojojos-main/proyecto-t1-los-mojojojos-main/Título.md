# 📘 Proyecto Máster 1 Trimestre: Sistema de Predicción Energética "Granada Smart City"

## [Enlace GitHub](https://classroom.github.com/a/WYC97Sdf)

## 1. El Desafío de Negocio

El **Ayuntamiento de Granada**, dentro de su estrategia de *Smart City*, se enfrenta a un problema de gestión energética. Actualmente, la ciudad recibe datos de sensores de consumo ubicados en distintos barrios, pero la gestión es reactiva. No saben cuánta energía se necesitará mañana o dentro de unas horas, lo que impide optimizar costes y dimensionar la red adecuadamente.

Vuestro equipo ha sido contratado como **Consultores de Data Science**.
**Vuestra misión:** Transformar datos históricos "sucios" en un sistema inteligente capaz de anticipar la demanda eléctrica horaria de la ciudad.

## 2. Materia Prima: El Dataset

Recibiréis el archivo `consumo_granada.csv`. Contiene registros horarios históricos (2015-2025) de sensores distribuidos por la ciudad.

**Diccionario de Datos:**
* `timestamp`: Fecha y hora exacta de la lectura.
* `zone_id`: Identificador numérico del barrio/zona.
* `zone_name`: Nombre del barrio (texto).
* `temperature`: Temperatura ambiente registrada (°C).
* `consumption_kwh`: Consumo eléctrico real medido (Variable Objetivo).

> **⚠️ Advertencia Crítica:** Estos datos provienen de sensores reales. **No son perfectos.** Contienen errores de transmisión, fallos de sensor e inconsistencias humanas. Parte esencial de vuestro trabajo es auditar y limpiar estos datos antes de que toquen cualquier modelo. Un modelo alimentado con datos erróneos es inútil (*Garbage In, Garbage Out*).

## 3. El Pipeline Técnico (Metodología)

El proyecto debe cubrir el ciclo de vida completo del dato. No se permiten "atajos".

### Fase 1: Ingeniería y Calidad del Dato
Tenéis total libertad y responsabilidad para decidir cómo tratar el dataset. Deberéis detectar:
* ¿Hay valores imposibles?
* ¿Hay información faltante?
* ¿Hay textos inconsistentes?
**Nota:** No recibiréis instrucciones sobre cómo limpiar. Debéis justificar vuestras decisiones en la memoria.

### Fase 2: Feature Engineering (Creatividad)
No utilizaremos modelos complejos de series temporales. Por tanto, vuestro éxito depende de vuestra capacidad para **"explicarle el tiempo"** a los modelos clásicos.
* ¿Cómo le decís a un árbol de decisión que "son las 8 de la tarde"?
* ¿Cómo le indicáis que "hoy es festivo en Granada"?
* ¿Cómo relacionáis la temperatura con el consumo?

### Fase 3: Benchmark de Modelos
Debéis entrenar, optimizar y **comparar rigurosamente** los siguientes algoritmos vistos en el máster:
1.  **Dummy Regressor:** Línea base obligatoria (el peor escenario aceptable).
2.  **K-Nearest Neighbors (KNN).**
3.  **Support Vector Regressor (SVR).**
4.  **Decision Tree Regressor.**
5.  **Random Forest Regressor.**

### Fase 4: Investigación (Gradient Boosting)
Se exige investigar e implementar un modelo de **Gradient Boosting Regressor**.
* **Objetivo:** Entender la diferencia entre *Bagging* (Random Forest) y *Boosting*.
* Este modelo suele ser el estándar de la industria en datos tabulares. Debéis comprobar si supera a los demás.

### Fase 5: Validación Robusta
Para evitar resultados engañosos, **TODOS** los modelos deben ser evaluados obligatoriamente mediante **Validación Cruzada de 5 particiones (5-Fold Cross-Validation)**.

---

## 4. Referencias de Calidad

Para que sepáis si vuestro trabajo va por buen camino, el departamento técnico anterior ha dejado establecidas unas métricas de referencia utilizando 5-Fold CV. Vuestro objetivo es acercaros o mejorar estos números. Si vuestro error es mucho mayor, algo falla en vuestro preprocesado.

| Modelo de Referencia | MAE Promedio (kWh) | RMSE Promedio (kWh) | Interpretación |
| :--- | :--- | :--- | :--- |
| **DummyRegressor (Base)** | ~1114.18 | ~1462.52 | Si no superáis esto, el modelo no sirve. |
| **DecisionTree (Prepoda)** | ~428.98 | ~632.06 | Rendimiento medio aceptable. |
| **GradientBoosting** | **~218.58** | **~342.82** | Rendimiento excelente (Objetivo). |

---

## 5. El Producto: Plataforma Web de Gestión Energética

El entregable final no es un Notebook aislado; es una solución de software operativa. Debéis desarrollar una aplicación web funcional que sirva como interfaz de toma de decisiones para el Ayuntamiento.

**Arquitectura Técnica Obligatoria:**
* **Backend/API:** Se recomienda encarecidamente el uso de **FastAPI** para servir el modelo y gestionar la lógica.
* **Base de Datos:** La aplicación **debe conectarse en tiempo real a vuestra base de datos MySQL**. Los datos históricos no pueden estar en un CSV estático dentro de la app; deben ser consultados mediante *queries* SQL desde la aplicación.
* **Frontend:** Libertad de elección (HTML/JS básico, Templates Jinja2, Dash, etc.), siempre que sea usable por un usuario no técnico.

La aplicación debe constar de **3 módulos o pestañas obligatorias**:

### 5.1. Cuadro de Mando Estratégico (Lectura de SQL)
Este módulo debe visualizar el estado histórico de la red eléctrica consultando directamente la base de datos MySQL. Debe responder a la pregunta: *"¿Qué ha pasado en la ciudad hasta hoy?"*.

* **KPIs Globales (Tarjetas numéricas):**
    * Consumo Total Histórico (kWh).
    * Consumo Promedio por hora.
    * Pico Máximo de demanda registrado (con fecha y zona).
* **Visualizaciones Dinámicas:**
    * **Ranking de Zonas:** Gráfico de barras mostrando el consumo promedio por Barrio (agrupado por SQL).
    * **Correlación Climática:** Gráfico de dispersión (*scatter plot*) que cruce `Temperatura` vs `Consumo` para visualizar la forma de "U" o tendencias lineales.

### 5.2. Simulador de Demanda "What-If" (Inferencia del Modelo)
Una interfaz tipo "calculadora" que permita al técnico simular escenarios futuros. Aquí entra en juego vuestro **Mejor Modelo (serializado/guardado)**.

* **Interfaz de Entrada (Inputs):** Formulario donde el usuario introduce:
    * Fecha y Hora objetivo (ej: *25 de Diciembre de 2025 a las 20:00*).
    * Zona/Barrio a consultar.
    * Temperatura prevista para esa hora (ej: *4ºC*).
* **Lógica de Backend:**
    1.  La App recibe los datos.
    2.  **Transformación:** El backend debe generar "al vuelo" las variables que el modelo necesita (ej: calcular si esa fecha es festivo, si es fin de semana, extraer el mes, etc.).
    3.  **Predicción:** Pasa los datos procesados al modelo cargado.
* **Salida (Output):** Muestra en pantalla el consumo estimado en kWh.

### 5.3. Auditoría del Modelo: Realidad vs. Predicción
Esta es la prueba de fuego visual para convencer al cliente de que el modelo funciona.

* **Selector de Periodo:** El usuario selecciona un rango de fechas del pasado (ej: *Primera semana de Febrero 2024*).
* **Proceso Híbrido:**
    1.  **Línea Real (SQL):** La App hace una query a MySQL para traer el consumo real (`consumption_kwh`) de ese periodo.
    2.  **Línea Predicha (Modelo):** La App usa las fechas y temperaturas de ese mismo periodo para generar las predicciones con vuestro modelo.
* **Gráfico Comparativo:** Superponer ambas líneas en un gráfico temporal.
    * *Objetivo:* Demostrar visualmente si vuestro modelo es capaz de "calcar" los picos de consumo, los valles nocturnos y el comportamiento en festivos.

---

## 6. Dinámica de Trabajo y Evaluación

### Organización (Equipos de 4)
* **Roles:** Organizad el trabajo (Limpieza, EDA, Modelado, App Web), pero recordad la regla de la defensa.

### ☠️ La Defensa: "Ruleta Rusa" con Temporizador
Dispondréis de **30 minutos** para presentar vuestro trabajo ante el tribunal.
* **Regla de Oro:** Habrá un **temporizador**. Cada 5 minutos sonará una alarma. En ese momento, el profesor señalará **al azar** a cualquier miembro del grupo para que continúe la exposición exactamente donde se quedó el anterior.
* **Implicación:** Todos debéis saberlo todo. Si al especialista en "Diseño Web" le toca explicar por qué el *Random Forest* tiene *overfitting* y no sabe responder, penalizará a todo el grupo. No compartimentéis el conocimiento, compartidlo.