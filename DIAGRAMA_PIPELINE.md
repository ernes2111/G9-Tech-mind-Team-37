# 📊 TechMind — Diagrama del Pipeline de Ciencia de Datos

> Versión **v0.5** — refleja la arquitectura actual con FastAPI + PostgreSQL + Spring Boot + Ingesta.
> Útil para el equipo de Back-End al integrarse con el componente de DS.

---

## Diagrama visual

![TechMind — Pipeline de Ciencia de Datos v0.4](pipeline_flowchart.png)

---

## Diagrama interactivo (Mermaid)

> Renderizable en GitHub, Notion, GitLab y editores compatibles con Mermaid.

```mermaid
flowchart TD

    subgraph TRAIN ["🎓 SECCIÓN 1 — Entrenamiento (Offline · Notebook)"]
        direction TB
        INGEST["🔧 ingest_documents.py\n(PDF/DOCX a PostgreSQL)"]
        PG_IN[("🗄️ PostgreSQL\ntabla: contenidos\n61+ registros · 8 categorías")]
        EDA["🔍 EDA — Análisis Exploratorio\n─────────────────────────\n• Distribución por categoría\n• Longitud de textos\n• Nulos y duplicados"]
        PREP["🧹 Preprocesamiento\n─────────────────────────\n• titulo + texto concatenados\n• Minúsculas + remoción de puntuación\n• Filtrado de stopwords en español\nfn: limpiar_texto()"]
        TFIDF["🔢 Vectorización TF-IDF\n─────────────────────────\n• TfidfVectorizer\n• max_features=1500 · ngram_range=(1,2)\n• Unigramas y bigramas"]
        MODEL["🤖 Entrenamiento del Modelo\n─────────────────────────\n• Regresión Logística\n• Train/Test split 75/25 estratificado\n• class_weight='balanced'"]
        KW["🔑 Extracción de Keywords\n─────────────────────────\n• Top 5 tokens por peso TF-IDF\n• Por documento individual\nfn: extraer_keywords()"]
        EVAL["📊 Evaluación\n─────────────────────────\n• Accuracy: ~0.69 (actual)\n• Precision / Recall / F1\n• Matriz de confusión"]
        SERIAL["💾 Serialización de Artefactos\n─────────────────────────\n• tfidf_vectorizer.joblib\n• modelo_clasificador.joblib"]

        INGEST -->|"INSERT contenidos"| PG_IN
        PG_IN -->|"pd.read_sql_query()"| EDA
        EDA --> PREP
        PREP -->|"limpiar_texto()"| TFIDF
        TFIDF --> MODEL
        TFIDF --> KW
        MODEL --> EVAL
        KW --> EVAL
        EVAL -->|"joblib.dump()"| SERIAL
    end

    subgraph PROD ["⚡ SECCIÓN 2 — Inferencia en Producción (Online · FastAPI)"]
        direction TB
        FASTAPI["⚡ FastAPI — Puerto 8000\n─────────────────────────\nPOST /predecir · GET /health\nGET /categorias · GET /docs\n─────────────────────────\n• Limpia texto · vectoriza · predice\n• Extrae keywords · guarda en DB"]
        PG_OUT[("🗄️ PostgreSQL\ntabla: predicciones\nid · titulo · categoria\nprobabilidad · keywords · created_at")]
        SPRING["☕ Spring Boot — Puerto 8080\n─────────────────────────\n• Recibe POST /contenido\n• Valida el request\n• Llama a FastAPI internamente\n• Responde al cliente"]
        CLIENT[/"📤 Cliente / Postman\n─────────────────────────\n{ 'categoria': 'Backend',\n  'probabilidad': 0.88,\n  'informaciones_adicionales': [...] }"/]

        FASTAPI -->|"INSERT prediccion"| PG_OUT
        SPRING -->|"HTTP interno POST /predecir"| FASTAPI
        FASTAPI -->|"JSON response"| SPRING
        SPRING -->|"POST /contenido"| CLIENT
        CLIENT -->|"request"| SPRING
    end

    SERIAL -->|"carga al arrancar"| FASTAPI
    INGEST -.->|"re-entrenamiento auto (>=3 docs)"| SERIAL

    style INGEST fill:#f43f5e,color:#fff,stroke:#e11d48
    style PG_IN  fill:#7c3aed,color:#fff,stroke:#5b21b6
    style EDA    fill:#2563eb,color:#fff,stroke:#1d4ed8
    style PREP   fill:#0891b2,color:#fff,stroke:#0e7490
    style TFIDF  fill:#059669,color:#fff,stroke:#047857
    style MODEL  fill:#d97706,color:#fff,stroke:#b45309
    style KW     fill:#ca8a04,color:#fff,stroke:#a16207
    style EVAL   fill:#dc2626,color:#fff,stroke:#b91c1c
    style SERIAL fill:#db2777,color:#fff,stroke:#be185d
    style FASTAPI fill:#4f46e5,color:#fff,stroke:#3730a3
    style PG_OUT  fill:#0f766e,color:#fff,stroke:#0d9488
    style SPRING  fill:#1e40af,color:#fff,stroke:#1e3a8a
    style CLIENT  fill:#f5f0d0,color:#111,stroke:#92400e
```

---

## Descripción de cada paso

### Sección 1 — Entrenamiento (corre en el notebook)

| Paso | Nombre | Entrada | Salida | Herramienta |
|------|--------|---------|--------|-------------|
| 0 | **Ingesta de datos (opcional)** | Carpeta `documentos/` (PDF/DOCX) | PostgreSQL (`contenidos`) | `ingest_documents.py` |
| 1 | **Fuente de datos** | `techmind` (PostgreSQL) | `DataFrame` pandas | `pd.read_sql_query()` |
| 2 | **EDA** | `DataFrame` | Gráficos + estadísticas | `matplotlib` / `seaborn` |
| 3 | **Preprocesamiento** | `titulo` + `texto` | `texto_limpio` | `limpiar_texto()` |
| 4 | **Vectorización TF-IDF** | `texto_limpio` | Matriz numérica dispersa | `TfidfVectorizer` |
| 5a | **Entrenamiento** | Matriz (train) | Modelo entrenado | `LogisticRegression` |
| 5b | **Keywords** | Matriz (doc individual) | Lista de términos | `extraer_keywords()` |
| 6 | **Evaluación** | Modelo + test set | Métricas | `classification_report` |
| 7 | **Serialización** | Modelo + vectorizador | `.joblib` en disco | `joblib.dump()` |

### Sección 2 — Inferencia en Producción

| Paso | Nombre | Entrada | Salida | Servicio |
|------|--------|---------|--------|---------|
| 8 | **FastAPI arranca** | `.joblib` desde disco | Modelo en memoria | `uvicorn app.main:app` |
| 9 | **Spring Boot llama** | `{ titulo, texto }` | `{ categoria, probabilidad, keywords }` | `POST /predecir` |
| 10 | **Log en PostgreSQL** | Predicción | Registro en `predicciones` | `app/database.py` |
| 11 | **Respuesta al cliente** | JSON de FastAPI | JSON al cliente/Postman | Spring Boot `POST /contenido` |

---

## Contrato de la API interna (FastAPI → Spring Boot)

### `POST http://localhost:8000/predecir`

**Request:**
```json
{
  "titulo": "Introducción a Spring Boot",
  "texto": "Conceptos básicos para la creación de APIs REST con Java y Spring Boot."
}
```

**Response (200 OK):**
```json
{
  "categoria": "Backend",
  "probabilidad": 0.8879,
  "informaciones_adicionales": ["spring boot", "java", "api rest", "creación apis", "spring"]
}
```

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `categoria` | `string` | Una de las 8 categorías del modelo |
| `probabilidad` | `float` (0–1) | Confianza del modelo (softmax de LogReg) |
| `informaciones_adicionales` | `string[]` | Top 5 keywords por peso TF-IDF del documento |

---

## Tablas PostgreSQL involucradas

```sql
-- Datos de entrenamiento (lectura por el notebook)
contenidos (id, titulo, texto, categoria, created_at)

-- Log de inferencias (escritura por FastAPI en cada predicción)
predicciones (id, titulo, texto, categoria, probabilidad, keywords[], created_at)
```

---

*Diagrama actualizado el 2026-07-21 — v0.5 · TechMind G9 LATAM Team 37 · Rol: Ciencia de Datos.*
