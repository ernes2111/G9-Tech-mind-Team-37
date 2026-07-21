# CHANGELOG — TechMind · Ciencia de Datos

> Todas las versiones están ordenadas de la más reciente a la más antigua.
> Se sigue el formato [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/).

---

## [0.5.0] — 2026-07-21 · Ingesta de Documentos + Re-entrenamiento Automático (actual)

### Añadido
- **Script de ingesta interactiva** (`ingest_documents.py`) que permite importar archivos PDF (`pdfplumber`) y DOCX (`python-docx`) a PostgreSQL.
  - Soporta la extracción y limpieza automatizada de texto.
  - Permite etiquetar manualmente la categoría (Opción A) en una interfaz CLI interactiva con preview de texto.
  - Detección de secciones para documentos multi-categoría, permitiendo split y etiquetado independiente por sección.
  - Control de duplicados mediante verificación del hash MD5 del contenido en la base de datos.
- **Re-entrenamiento automático local**: el script de ingesta cuenta con un trigger automático que detecta si se han importado 3 o más documentos en una sola sesión y ofrece ejecutar el notebook mediante Jupyter (`jupyter nbconvert --execute`) en segundo plano para regenerar los modelos `.joblib`.
- **Nueva guía de ingesta** (`INGESTA_DOCUMENTOS.md`) detallando la preparación de documentos, flujo de ejecución, Edge Cases y solución de problemas.
- **Guía de entrega de Backend** (`ENTREGA_BACKEND.md`) para facilitar al equipo Java qué archivos deben clonarse (código, docker, docs) y cuáles compartirse manualmente (modelos `.joblib` en `.gitignore`).
- **Plan y suite de pruebas para QA** (`QA_TESTING.md` y `postman_collection.json`) con 23 casos de prueba para validar Happy Paths, Edge Cases, Error Handling y performance contra el endpoint local.

### Cambiado
- **`requirements.txt`** — agregadas dependencias para procesamiento de documentos: `pdfplumber>=0.11.0` y `python-docx>=1.1.0`.
- **`.gitignore`** — modificado para excluir archivos locales PDF y DOCX en la carpeta `documentos/` (`documentos/*.pdf` y `documentos/*.docx`) y mantener solo la carpeta usando `.gitkeep`.
- **`README.md`** — tabla de documentación actualizada con los nuevos entregables (`ENTREGA_BACKEND.md`, `QA_TESTING.md`, `INGESTA_DOCUMENTOS.md` y `postman_collection.json`).

---

## [0.4.0] — 2026-07-21 · FastAPI + PostgreSQL

### Añadido
- **Microservicio FastAPI** (`app/main.py`) con tres endpoints:
  - `POST /predecir` — inferencia interna consumida por Spring Boot. Carga los `.joblib` al arrancar, clasifica el texto y persiste la predicción en PostgreSQL.
  - `GET /health` — health check para que Spring Boot verifique disponibilidad antes de llamar.
  - `GET /categorias` — devuelve la lista de las 8 categorías del modelo.
  - `GET /docs` — documentación Swagger automática generada por FastAPI.
- **Módulo de base de datos** (`app/database.py`) con `get_connection()`, `init_db()` y `log_prediccion()` para PostgreSQL.
- **Script de migración a PostgreSQL** (`migrate_to_postgres.py`) — crea las tablas `contenidos` y `predicciones`, lee desde SQLite o CSV, e incluye confirmación interactiva para evitar reemplazos accidentales.
- **Tabla `predicciones`** en PostgreSQL — log automático de cada inferencia con `titulo`, `texto`, `categoria`, `probabilidad`, `keywords` y `created_at`.
- **`docker-compose.yml`** — levanta PostgreSQL 16 localmente con un solo comando (`docker-compose up -d`). Incluye health check y volumen persistente.
- **`.env.example`** — plantilla de variables de entorno para Python (FastAPI) y referencia para Spring Boot.
- **`.gitignore`** — excluye `.env`, `*.joblib`, `techmind.db` y archivos de Python/Jupyter del repositorio.
- **`BACKEND_INTEGRATION.md`** — guía completa para el equipo de Java/Spring Boot: setup, contrato del endpoint `/predecir`, ejemplos de código Java (`RestTemplate` y `WebClient`), configuración de `application.properties`, schema SQL y checklist de verificación.

### Cambiado
- **`requirements.txt`** — agregados `fastapi>=0.111.0`, `uvicorn[standard]>=0.29.0`, `psycopg2-binary>=2.9.9`, `python-dotenv>=1.0.0`.
- **`TechMind_DataScience.ipynb` — Celda 3** — modo dual: si `PG_HOST` está configurado carga desde PostgreSQL; si no, hace fallback a SQLite local (retrocompatible).

### Arquitectura
```
Postman → Spring Boot (8080) → FastAPI (8000) → PostgreSQL (5432)
                     └─────────────────────────────────────────────┘
```

---

## [0.3.0] — 2026-07-17 · Migración de base de datos a SQLite

### Añadido
- **Base de datos SQLite** `techmind.db` — migración del dataset original `contenidos_tecnicos.csv` a una base de datos relacional embebida. La tabla `contenidos` incorpora dos campos nuevos respecto al CSV:
  - `id` — clave primaria autoincremental, necesaria para que el Back-End pueda referenciar registros individuales.
  - `created_at` — timestamp UTC de inserción, útil para auditoría y reentrenamiento incremental.
- **Script de migración** `migrate_to_sqlite.py` — script Python reutilizable (sin dependencias externas, solo stdlib) que: lee el CSV → crea el esquema → importa los 61 registros → verifica la distribución por categoría → imprime ejemplos de carga. Puede volver a ejecutarse en cualquier momento para regenerar la DB desde cero.
- **Índice sobre `categoria`** (`idx_categoria`) — mejora el rendimiento de consultas por categoría, especialmente relevante cuando el dataset crezca.

### Cambiado
- **Notebook `TechMind_DataScience.ipynb` — Celda 3**: la carga del dataset se migró de `pd.read_csv("contenidos_tecnicos.csv")` a `pd.read_sql_query(...)` sobre `techmind.db`. El resto del pipeline (preprocesamiento, vectorización, modelo, serialización) no requirió cambios.

### Por qué SQLite
- Permite al Back-End consultar, insertar y filtrar contenidos sin parsear un CSV manualmente.
- Soporta queries SQL estándar (`SELECT`, `INSERT`, `WHERE categoria = ?`) directamente desde Java (JDBC) o Python.
- Es un archivo único (`techmind.db`) — no requiere servidor, fácil de subir a OCI Object Storage.
- La tabla queda preparada para recibir nuevos registros vía `POST /contenido` sin necesidad de reescribir el archivo CSV.

---

## [0.2.0] — 2026-07-15 · MVP del Hackathon

### Añadido
- **Pipeline de inferencia end-to-end** — función `procesar_contenido(titulo, texto)` que encadena limpieza → vectorización → clasificación → extracción de keywords y devuelve un dict JSON-serializable listo para el contrato REST.
- **Extracción de palabras clave** (campo `informaciones_adicionales`) mediante los términos con mayor peso TF-IDF dentro del documento individual, desacoplada de la predicción de categoría.
- **Tres ejemplos de uso documentados** en el notebook (Backend / Data Science / DevOps) como requisito obligatorio del MVP.
- **Serialización de artefactos** — `tfidf_vectorizer.joblib` y `modelo_clasificador.joblib` guardados con `joblib`, más celda de validación de carga que simula el arranque de la API.
- **Notas de integración** en la última sección del notebook (Celda 28): pasos para subir a OCI Object Storage y opciones de arquitectura (microservicio Python vs. exportación al formato Java).
- **Contrato de respuesta acordado** — campo renombrado a `informaciones_adicionales` (plural) para alinear con el equipo de Back-End:
  ```json
  {
    "categoria": "Backend",
    "probabilidad": 0.2779,
    "informaciones_adicionales": ["boot", "spring boot", "spring", "creación apis", "java spring"]
  }
  ```

### Cambiado
- El campo de salida originalmente denominado `informacion_adicional` (singular, según el PDF de la consigna) fue renombrado a `informaciones_adicionales` (plural) para coincidir con el contrato que usa el equipo de Back-End.

---

## [0.1.0] — 2026-07-14 · Construcción del pipeline base

### Añadido
- **Dataset sintético** `contenidos_tecnicos.csv` — ~60 registros en español, con campos `titulo`, `texto` y `categoria`, repartidos en 8 categorías: Backend, Frontend, Data Science, DevOps, Mobile, Bases de Datos, Seguridad y Cloud.
- **EDA inicial** — gráfico de distribución de categorías (countplot), histograma de longitud de textos (en palabras), chequeo de nulos y filas duplicadas.
- **Preprocesamiento de texto** — función `limpiar_texto(texto)`: minúsculas → remoción de puntuación (regex) → filtrado de stopwords en español (lista propia de ~30 términos, incluidos frases funcionales como "se explica", "se presenta").
- **Vectorización TF-IDF** — `TfidfVectorizer` con `max_features=1500`, `ngram_range=(1, 2)` y `min_df=1` para capturar unigramas y bigramas (p. ej. "api rest", "machine learning").
- **Modelo de clasificación** — Regresión Logística con `class_weight="balanced"` y `max_iter=1000`, entrenada sobre split train/test estratificado (75/25, `random_state=42`).
- **Evaluación del modelo** — accuracy, `classification_report` por categoría (precision / recall / F1) y matriz de confusión (heatmap con Seaborn).
  - Accuracy reportado sobre el test set actual: **~0.69** (orientativo; refleja las limitaciones del dataset pequeño).
  - Categorías con peor generalización: **DevOps** y **Seguridad** (menos ejemplos de entrenamiento).

---

## [0.0.1] — 2026-07-13 · Scaffolding inicial

### Añadido
- Estructura base del notebook `TechMind_DataScience.ipynb` con secciones enumeradas (EDA → Preprocesamiento → Vectorización → Modelo → Evaluación → Keywords → Inferencia → Serialización).
- Definición del alcance y rol del componente de Ciencia de Datos dentro del equipo (ver `detalle_trabajo.md`).
- Primeras dependencias identificadas: `pandas`, `scikit-learn`, `matplotlib`, `seaborn`, `joblib`, `re`, `json`, `numpy`.

---

*Mantenido por el equipo de Ciencia de Datos — TechMind G9 LATAM Team 37. Última actualización: 2026-07-21.*
