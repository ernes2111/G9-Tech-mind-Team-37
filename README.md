<div align="center">

# 🧠 TechMind
### Organización Inteligente del Conocimiento Técnico

[![Python](https://img.shields.io/badge/Python-3.12.3-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.4+-F7931E?style=flat&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![SQLite](https://img.shields.io/badge/SQLite-3-003B57?style=flat&logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-F37626?style=flat&logo=jupyter&logoColor=white)](https://jupyter.org/)
[![OCI](https://img.shields.io/badge/Oracle-OCI-F80000?style=flat&logo=oracle&logoColor=white)](https://www.oracle.com/cloud/)
[![Hackathon](https://img.shields.io/badge/G9_LATAM-Team_37-blueviolet?style=flat)](https://github.com/ernes2111/G9-Tech-mind-Team-37)
[![Repo](https://img.shields.io/badge/Repositorio-Privado-red?style=flat&logo=github&logoColor=white)](https://github.com/ernes2111/G9-Tech-mind-Team-37)

**Hackathon TechMind · G9 LATAM · Equipo 37**

</div>

---

## 📌 ¿Qué es TechMind?

TechMind es un sistema de **organización inteligente de contenido técnico**. Dado el título y texto de un artículo, documentación o apunte técnico, el sistema responde automáticamente con:

- 📂 La **categoría temática** del contenido (Backend, Data Science, DevOps, etc.)
- 📊 La **probabilidad** de esa clasificación
- 🔑 Las **palabras clave** más relevantes del texto

Todo en formato JSON, listo para ser consumido por la API REST del equipo.

```json
{
  "categoria": "Backend",
  "probabilidad": 0.8879,
  "informaciones_adicionales": ["spring boot", "java", "api rest", "creación apis", "spring"]
}
```

---

## 🏗️ Arquitectura del Proyecto

```
                    ┌──────────────────────────────────┐
                    │   Usuario / Aplicación cliente   │
                    └───────────────┬──────────────────┘
                                    │ POST /contenido
                    ┌───────────────▼──────────────────┐
                    │    API REST — Java / Spring Boot  │
                    └───────────────┬──────────────────┘
                                    │ consume modelo
                    ┌───────────────▼──────────────────┐
                    │  Ciencia de Datos — Python        │
                    │  TF-IDF + Regresión Logística     │
                    └───────────────┬──────────────────┘
                                    │ artefactos + datos
                    ┌───────────────▼──────────────────┐
                    │  OCI Object Storage               │
                    │  techmind.db · *.joblib           │
                    └──────────────────────────────────┘
```

| Componente | Tecnología | Responsable |
|-----------|-----------|-------------|
| **Ciencia de Datos** | Python · Scikit-Learn · SQLite | Ernesto |
| **Back-End** | Java · Spring Boot | Equipo Backend |
| **Nube** | Oracle Cloud Infrastructure (OCI) | Todo el equipo |

---

## 📁 Estructura del Repositorio

```
TechMind - G9 - LATAM - TEAM 37/
│
├── 📓 TechMind_DataScience.ipynb   # Notebook principal — pipeline completo
├── 🗄️  techmind.db                 # Base de datos SQLite (dataset de entrenamiento)
├── 📋 contenidos_tecnicos.csv      # Fuente original del dataset (referencia)
├── 🔧 migrate_to_sqlite.py         # Script de migración CSV → SQLite
│
├── 📊 pipeline_flowchart.png       # Diagrama visual del pipeline
│
├── 📄 README.md                    # Este archivo
├── 📄 REQUIREMENTS.md              # Dependencias detalladas con descripción
├── 📄 CHANGELOG.md                 # Historial de versiones
├── 📄 ROADMAP.md                   # Mejoras planificadas y bugs conocidos
├── 📄 DIAGRAMA_PIPELINE.md         # Diagrama interactivo (Mermaid) + tabla de pasos
├── 📄 EXPLICACION_PROYECTO.md      # Explicación no técnica para presentaciones
├── 📄 detalle_trabajo.md           # Resumen técnico del trabajo de DS
├── 📄 consigna.md                  # Enunciado original del hackathon
│
└── 📦 requirements.txt             # Dependencias pip
```

> **Nota:** `tfidf_vectorizer.joblib` y `modelo_clasificador.joblib` se generan localmente al
> ejecutar el notebook. No están versionados en el repositorio — deben subirse a OCI Object Storage.

---

## 🚀 Cómo ejecutar el proyecto

### 1. Clonar el repositorio

```bash
git clone https://github.com/ernes2111/G9-Tech-mind-Team-37.git
cd G9-Tech-mind-Team-37
```

### 2. Crear entorno virtual e instalar dependencias

```bash
python3 -m venv venv
source venv/bin/activate          # macOS / Linux
# venv\Scripts\activate           # Windows

pip install -r requirements.txt
```

### 3. (Opcional) Regenerar la base de datos SQLite

Si `techmind.db` no está presente o querés reiniciarla desde el CSV original:

```bash
python3 migrate_to_sqlite.py
```

### 4. Ejecutar el notebook

```bash
jupyter notebook TechMind_DataScience.ipynb
```

Ejecutar todas las celdas de arriba hacia abajo. Al finalizar se generarán:
- `tfidf_vectorizer.joblib`
- `modelo_clasificador.joblib`

### 5. Verificar el entorno

```python
import sys, importlib

requeridos = {"pandas": "2.2.0", "numpy": "1.26.0", "sklearn": "1.4.0",
              "joblib": "1.3.0", "matplotlib": "3.8.0", "seaborn": "0.13.0"}

for mod, minver in requeridos.items():
    m = importlib.import_module(mod)
    ver = getattr(m, "__version__", "?")
    print(f"{'✅' if ver >= minver else '⚠️'} {mod:15} {ver}")
```

---

## 🧪 Pipeline de Ciencia de Datos

![Diagrama del Pipeline](pipeline_flowchart.png)

| Paso | Descripción | Función / Herramienta |
|------|-------------|----------------------|
| 1 | **Carga de datos** desde `techmind.db` | `pd.read_sql_query()` |
| 2 | **EDA** — distribución de categorías, longitud de textos, nulos | `matplotlib` / `seaborn` |
| 3 | **Preprocesamiento** — concatenar título+texto, minúsculas, remover puntuación, stopwords | `limpiar_texto()` |
| 4 | **Vectorización TF-IDF** — unigramas y bigramas, max 1500 features | `TfidfVectorizer` |
| 5a | **Entrenamiento** — split 75/25 estratificado, Regresión Logística balanceada | `LogisticRegression` |
| 5b | **Extracción de keywords** — top 5 tokens por peso TF-IDF del documento | `extraer_keywords()` |
| 6 | **Evaluación** — accuracy ~0.69, precision/recall/F1, matriz de confusión | `classification_report` |
| 7 | **Serialización** de vectorizador y modelo | `joblib.dump()` |
| 8 | **Función de inferencia** end-to-end lista para el Back-End | `procesar_contenido()` |

> Ver [`DIAGRAMA_PIPELINE.md`](DIAGRAMA_PIPELINE.md) para el diagrama interactivo Mermaid con descripción detallada de cada paso.

---

## 📬 Contrato de la API

### Endpoint esperado: `POST /contenido`

**Request:**
```json
{
  "titulo": "Introducción a Spring Boot",
  "texto": "Conceptos básicos para la creación de APIs REST con Java y Spring Boot."
}
```

**Response:**
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

### Las 8 categorías disponibles

| Categoría | Ejemplos de contenido |
|-----------|-----------------------|
| **Backend** | Spring Boot, Node.js, APIs REST, JWT, microservicios |
| **Frontend** | React, Vue.js, Angular, TypeScript, CSS Grid |
| **Data Science** | Pandas, Scikit-Learn, TF-IDF, clustering, series temporales |
| **DevOps** | Docker, Kubernetes, GitHub Actions, Terraform, CI/CD |
| **Mobile** | React Native, Flutter, Swift, Kotlin, Android |
| **Bases de Datos** | SQL, MongoDB, Redis, JPA, transacciones ACID |
| **Seguridad** | OWASP, JWT, criptografía, autenticación 2FA |
| **Cloud** | OCI, serverless, escalabilidad, redes virtuales |

---

## 🗄️ Base de Datos

El dataset de entrenamiento está almacenado en **SQLite** (`techmind.db`).

```sql
CREATE TABLE contenidos (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo      TEXT    NOT NULL,
    texto       TEXT    NOT NULL,
    categoria   TEXT    NOT NULL,
    created_at  TEXT    NOT NULL DEFAULT (datetime('now'))
);
```

**Estado actual:** 61 registros sintéticos en español, distribuidos en 8 categorías.
Se recomienda ampliar con contenidos reales antes de la demo final (ver [ROADMAP](ROADMAP.md)).

Para consultas directas:
```bash
sqlite3 techmind.db "SELECT categoria, COUNT(*) FROM contenidos GROUP BY categoria;"
```

---

## 📦 Dependencias

| Paquete | Versión mínima | Uso |
|---------|---------------|-----|
| `pandas` | ≥ 2.2.0 | Carga desde SQLite, manipulación de datos |
| `numpy` | ≥ 1.26.0 | Operaciones sobre matrices TF-IDF |
| `scikit-learn` | ≥ 1.4.0 | Vectorizador, modelo, métricas |
| `joblib` | ≥ 1.3.0 | Serialización de artefactos |
| `matplotlib` | ≥ 3.8.0 | Visualizaciones EDA |
| `seaborn` | ≥ 0.13.0 | Gráficos estadísticos |
| `notebook` | ≥ 7.0.0 | Entorno Jupyter |

> Ver [`REQUIREMENTS.md`](REQUIREMENTS.md) para la descripción completa, módulos stdlib y dependencias opcionales del ROADMAP.

---

## 📚 Documentación

| Archivo | Descripción |
|---------|-------------|
| [`DIAGRAMA_PIPELINE.md`](DIAGRAMA_PIPELINE.md) | Diagrama visual + Mermaid interactivo del pipeline completo |
| [`EXPLICACION_PROYECTO.md`](EXPLICACION_PROYECTO.md) | Explicación no técnica para presentaciones y demos |
| [`REQUIREMENTS.md`](REQUIREMENTS.md) | Dependencias detalladas, instalación, compatibilidad |
| [`CHANGELOG.md`](CHANGELOG.md) | Historial de versiones del componente de DS |
| [`ROADMAP.md`](ROADMAP.md) | Mejoras planificadas, fixes conocidos y prioridades |
| [`detalle_trabajo.md`](detalle_trabajo.md) | Resumen técnico del trabajo entregado |
| [`consigna.md`](consigna.md) | Enunciado original del hackathon |

---

## 🔮 Próximos pasos

Los ítems prioritarios antes de la demo final:

- [ ] **Ampliar el dataset** con contenidos reales (≥250 registros) — mejora esperada del accuracy a ≥0.82
- [ ] **Subir artefactos a OCI** — `techmind.db`, `tfidf_vectorizer.joblib`, `modelo_clasificador.joblib`
- [ ] **Integración con Back-End** — definir si el modelo corre en microservicio FastAPI o se exporta para Java
- [ ] **Cross-validation k-fold** — métricas más robustas para el dataset pequeño

> Ver [`ROADMAP.md`](ROADMAP.md) para el listado completo con prioridades y descripción técnica.

---

## 👥 Equipo

| Rol | Tecnología | Integrante |
|-----|-----------|-----------|
| **Ciencia de Datos** | Python · Scikit-Learn · SQLite · Jupyter | Ernesto |
| **Back-End** | Java · Spring Boot | Equipo Backend |
| **Cloud** | Oracle Cloud Infrastructure | Todo el equipo |

---

<div align="center">

**TechMind · Hackathon G9 LATAM · Equipo 37**

*"Organización inteligente del conocimiento técnico"*

</div>
