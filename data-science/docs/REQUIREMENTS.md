# REQUIREMENTS — TechMind · Ciencia de Datos

> Dependencias, versiones y pasos de instalación del componente de Ciencia de Datos.
> Última actualización: 2026-07-17.

---

## Requisito previo — Python

| Componente | Versión utilizada | Mínimo requerido |
|------------|-------------------|------------------|
| **Python** | 3.12.3 | ≥ 3.10 |

Verificá tu versión con:
```bash
python3 --version
```

---

## Instalación rápida

```bash
# 1. (Opcional pero recomendado) Crear un entorno virtual
python3 -m venv venv
source venv/bin/activate        # macOS / Linux
# venv\Scripts\activate         # Windows

# 2. Instalar todas las dependencias
pip install -r requirements.txt

# 3. Verificar
python3 -c "import pandas, sklearn, matplotlib, seaborn, joblib; print('OK')"
```

---

## Dependencias del proyecto

### 📦 Paquetes externos (requieren instalación)

| Paquete | Versión mínima | ¿Para qué se usa? |
|---------|---------------|-------------------|
| **pandas** | ≥ 2.2.0 | Carga del dataset desde PostgreSQL (`read_sql_query`), manipulación de DataFrames |
| **numpy** | ≥ 1.26.0 | Operaciones sobre matrices TF-IDF, cálculo de probabilidades |
| **scikit-learn** | ≥ 1.4.0 | `TfidfVectorizer`, `LogisticRegression`, métricas de evaluación, `train_test_split` |
| **joblib** | ≥ 1.3.0 | Serialización y carga de los artefactos (`tfidf_vectorizer.joblib`, `modelo_clasificador.joblib`) |
| **matplotlib** | ≥ 3.8.0 | Visualizaciones del EDA (histograma de longitudes, matriz de confusión) |
| **seaborn** | ≥ 0.13.0 | Gráficos estadísticos (`countplot`, `heatmap`) sobre las visualizaciones de matplotlib |
| **notebook** | ≥ 7.0.0 | Entorno Jupyter para ejecutar `TechMind_DataScience.ipynb` |
| **ipykernel** | ≥ 6.29.0 | Kernel Python dentro de Jupyter |

### 🐍 Módulos de la stdlib (incluidos en Python, sin instalar)

| Módulo | ¿Para qué se usa? |
|--------|-------------------|
| `re` | Limpieza de texto: remoción de puntuación y caracteres especiales |
| `json` | Serialización de la salida de inferencia al formato JSON del contrato REST |
| `csv` | Lectura del CSV original en el script `migrate_to_postgres.py` |
| `pathlib` | Manejo de rutas de archivo en `migrate_to_postgres.py` |
| `datetime` | Generación del timestamp `created_at` al insertar registros en PostgreSQL |

---

## Artefactos generados al ejecutar el notebook

Estos archivos **no se instalan** — se generan localmente al correr el notebook de punta a punta:

| Archivo | ¿Qué es? | ¿Dónde se usa? |
|---------|----------|----------------|
| `tfidf_vectorizer.joblib` | Vectorizador TF-IDF entrenado | FastAPI al recibir un texto nuevo |
| `modelo_clasificador.joblib` | Clasificador de Regresión Logística entrenado | FastAPI para predecir categoría |

> ⚠️ **Importante:** `tfidf_vectorizer.joblib` y `modelo_clasificador.joblib` deben subirse a
> OCI Object Storage para que el Back-End (Java / Spring Boot) pueda acceder a ellos.
> Ver el ROADMAP (ítem DS-003b) para los pasos de subida.

---

## Dependencias opcionales (no instaladas aún)

Estas dependencias corresponden a funcionalidades del ROADMAP que aún no están implementadas:

| Paquete | Versión sugerida | Para qué se necesitaría |
|---------|-----------------|-------------------------|
| `nltk` | ≥ 3.8 | Stopwords en español más completas (DS-002 del ROADMAP) |
| `spacy` + `es_core_news_sm` | ≥ 3.7 | Alternativa avanzada para preprocesamiento (DS-002) |
| `sentence-transformers` | ≥ 2.7 | Búsqueda semántica con embeddings (DS-006) |
| `eli5` o `lime` | ≥ 0.13 / ≥ 0.11 | Explicabilidad del modelo (DS-008) |
| `oci` | ≥ 2.120 | SDK oficial de Oracle Cloud para subir artefactos a OCI Object Storage (DS-003b) |
| `fastapi` + `uvicorn` | ≥ 0.111 / ≥ 0.29 | Microservicio Python de inferencia (opción arquitectónica alternativa al Java) |

---

## Compatibilidad de entornos

| Entorno | Compatible | Notas |
|---------|------------|-------|
| **Jupyter Notebook** (local) | ✅ | Recomendado para desarrollo y demostración |
| **Google Colab** | ✅ | Subir el notebook; configurar las variables de entorno apuntando a una PostgreSQL accesible |
| **VS Code + extensión Jupyter** | ✅ | Seleccionar el intérprete del virtualenv |
| **pip + venv** | ✅ | Flujo estándar descrito arriba |
| **conda** | ✅ | `conda install pandas scikit-learn matplotlib seaborn joblib notebook` |
| **Python < 3.10** | ❌ | No garantizado; se usan type hints modernos |
| **Python 2.x** | ❌ | No compatible |

---

## Verificación rápida del entorno

Ejecutá esta celda al inicio del notebook (o en la terminal) para validar que todo está disponible:

```python
import sys, importlib

requeridos = {
    "pandas":      "2.2.0",
    "numpy":       "1.26.0",
    "sklearn":     "1.4.0",   # importado como sklearn, instalado como scikit-learn
    "joblib":      "1.3.0",
    "matplotlib":  "3.8.0",
    "seaborn":     "0.13.0",
}

print(f"Python {sys.version}\n")
for mod, minver in requeridos.items():
    try:
        m = importlib.import_module(mod)
        ver = getattr(m, "__version__", "?")
        status = "✅" if ver >= minver else "⚠️ actualizar"
        print(f"  {status}  {mod:15} {ver}")
    except ImportError:
        print(f"  ❌  {mod:15} NO INSTALADO — pip install {mod}")
```

---

*Mantenido por el equipo de Ciencia de Datos — TechMind G9 LATAM Team 37.*
