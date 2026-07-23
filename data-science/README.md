# 🧠 TechMind — Módulo de Ciencia de Datos y FastAPI

Este directorio contiene todo el componente de **Ciencia de Datos, Machine Learning y API REST en FastAPI** del proyecto **TechMind** para el equipo **G9 LATAM - Team 37**.

---

## 📌 Repositorio del Proyecto
```bash
git clone https://github.com/No-Country-simulation/g9-latam-techmind-team37.git
cd g9-latam-techmind-team37/data-science
```

---

## 📁 Estructura del Módulo `data-science/`

```
data-science/
│
├── data/
│   ├── raw/
│   │   └── contenidos_tecnicos.csv    # Dataset inicial de entrenamiento (~61 registros)
│   └── processed/                  # Datos procesados / intermedios
│
├── notebooks/
│   └── TechMind_DataScience.ipynb  # Notebook Jupyter con el pipeline de ML completo
│
├── src/
│   ├── migrate_to_postgres.py     # Script de migración CSV -> PostgreSQL
│   └── ingest_documents.py        # Ingesta masiva de PDFs/DOCXs a PostgreSQL
│
├── models/
│   ├── modelo_clasificador.joblib # Modelo de Regresión Logística entrenado
│   └── tfidf_vectorizer.joblib    # Vectorizador TF-IDF ajustado
│
├── docs/
│   ├── BACKEND_INTEGRATION.md     # Guía de integración Java / Spring Boot <-> FastAPI
│   ├── ENTRENAMIENTO_Y_EJECUCION.md # Guía paso a paso para entrenar y ejecutar modelos
│   ├── DIAGRAMA_PIPELINE.md       # Diagrama Mermaid interactivo del pipeline
│   ├── INGESTA_DOCUMENTOS.md      # Guía de ingesta de documentos PDF/DOCX
│   ├── EXPLICACION_PROYECTO.md    # Resumen conceptual del proyecto
│   ├── REQUIREMENTS.md            # Requerimientos detallados
│   ├── ROADMAP.md                 # Próximos pasos
│   └── CHANGELOG.md               # Historial de cambios
│
├── assets/
│   └── pipeline_flowchart.png     # Diagrama visual del flujo de datos
│
├── requirements.txt               # Dependencias de Python
└── README.md                       # Este archivo
```

> ⚠️ **Nota:** el microservicio FastAPI (`app/`) se encuentra en la **raíz del repositorio**, no dentro de `data-science/`.

---

## 🚀 Guía de Inicio Rápido

### 1. Clonar el repositorio del grupo
```bash
git clone https://github.com/No-Country-simulation/g9-latam-techmind-team37.git
cd g9-latam-techmind-team37/data-science
```

### 2. Crear entorno virtual e instalar dependencias
```bash
python3 -m venv venv
source venv/bin/activate        # Linux / macOS
# venv\Scripts\activate         # Windows

pip install -r requirements.txt
```

### 3. Configurar `.env` y levantar PostgreSQL con Docker
```bash
cp .env.example .env
docker-compose up -d
```

### 4. Migrar el dataset semilla a PostgreSQL
```bash
python src/migrate_to_postgres.py
```

### 5. Iniciar la API FastAPI (Microservicio)
```bash
uvicorn app.main:app --reload --port 8000
```
La documentación Swagger estará disponible en: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 📚 Documentación Técnica Detallada

- **Para el Equipo de Backend (Java / Spring Boot):** [`docs/BACKEND_INTEGRATION.md`](docs/BACKEND_INTEGRATION.md)
- **Guía de Entrenamiento y Re-entrenamiento:** [`docs/ENTRENAMIENTO_Y_EJECUCION.md`](docs/ENTRENAMIENTO_Y_EJECUCION.md)
- **Ingesta de Documentos (PDF/DOCX):** [`docs/INGESTA_DOCUMENTOS.md`](docs/INGESTA_DOCUMENTOS.md)
- **Diagrama del Pipeline:** [`docs/DIAGRAMA_PIPELINE.md`](docs/DIAGRAMA_PIPELINE.md)
- **Explicación del Proyecto:** [`docs/EXPLICACION_PROYECTO.md`](docs/EXPLICACION_PROYECTO.md)
