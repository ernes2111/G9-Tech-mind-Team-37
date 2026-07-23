# ROADMAP — TechMind · Ciencia de Datos

> Prioridades y mejoras identificadas desde el rol de **Analista / Científico de Datos**.
> Las secciones están ordenadas por impacto y urgencia para el proyecto.

---

## Leyenda de prioridades

| Símbolo | Significado |
|---------|-------------|
| 🔴 | Crítico — bloquea calidad o integración |
| 🟠 | Alto — impacto directo en el MVP final |
| 🟡 | Medio — mejora significativa post-demo |
| 🟢 | Bajo — nice-to-have a futuro |

---

## Fase 1 — Pre-demo (urgente)

### 🔴 DS-001 · Ampliación del dataset con datos reales — 🟡 En progreso / Herramienta provista
**Problema actual:** el dataset sintético tiene ~60 filas (~7-8 por categoría). Con tan pocos
datos, el split 75/25 deja 1-2 muestras por categoría en test; las métricas actuales
(accuracy ~0.69) son **estadísticamente no confiables**.

**Acción:**
- Incorporar al menos 30-50 ejemplos **reales** por categoría antes de la presentación final.
- **Herramienta provista:** Se creó `ingest_documents.py` para ingestar dinámicamente PDFs y DOCXs. El equipo de Backend/QA puede alimentar la DB de contenidos directamente colocando archivos en `documentos/` y ejecutando el script.
- Objetivo mínimo: **≥250 registros totales**, con distribución balanceada.

**Impacto esperado:** accuracy estimado ≥ 0.82 con datos representativos.

---

### 🔴 DS-002 · Stopwords incompletas — pérdida de señal y ruido en features
**Problema actual:** la lista manual de stopwords en español tiene ~30 términos. Términos
funcionales muy frecuentes en textos técnicos en español (p. ej. "mediante", "través",
"partir", "tanto", "cada", "dicho") no están filtrados, lo que genera features ruidosas que
reducen la discriminación del modelo.

**Acción:**
- Reemplazar la lista manual por `nltk.corpus.stopwords.words('spanish')` (150+ términos) o
  `spacy` con el modelo `es_core_news_sm`.
- Mantener términos técnicos que colisionan con stopwords genéricas (p. ej. "no" en contexto
  de "NoSQL").

---

### 🟠 DS-003 · Persistencia del dataset y subida a OCI Object Storage — ✅ Completado (local)
**Estado actual:** dataset migrado a PostgreSQL (`migrate_to_postgres.py`). FastAPI persiste
cada predicción en la tabla `predicciones`. Docker Compose levanta todo localmente.

**Pendiente únicamente:**
- Subir `tfidf_vectorizer.joblib` y `modelo_clasificador.joblib` a OCI Object Storage.
- Apuntar `PG_HOST` a OCI Database with PostgreSQL en producción.

---

### 🟠 DS-004 · Cross-validation y métricas robustas
**Problema actual:** la evaluación usa un único split (75/25). Con ~60 filas, la varianza
entre splits es enorme; la métrica reportada puede cambiar ±10pp según la semilla.

**Acción:**
- Implementar **k-fold estratificado** (k=5) con `StratifiedKFold` para reportar
  `mean ± std` de accuracy y F1-macro.
- Esto da métricas más honestas y detecta overfitting sobre el dataset pequeño.

---

## Fase 2 — Post-demo (mejoras de calidad)

### 🟡 DS-005 · Reemplazo o complemento de Regresión Logística
**Problema actual:** la Regresión Logística es un buen baseline, pero tiene limitaciones en
vocabularios técnicos con alta dimensionalidad y categorías similares (p. ej. Backend vs.
DevOps tienen vocabulario solapado).

**Acciones evaluadas:**
1. **LinearSVC** — generalmente supera a LogReg en clasificación de texto con TF-IDF; más rápido.
2. **Naive Bayes Multinomial** — excelente con features dispersas, muy interpretable.
3. **Gradient Boosting (LightGBM / XGBoost)** — útil si se añaden features adicionales
   (longitud, densidad técnica, etc.).
4. **Comparación formal** usando `GridSearchCV` o `Pipeline` de scikit-learn con múltiples
   estimadores.

---

### 🟡 DS-006 · Búsqueda semántica con sentence embeddings
**Problema actual:** TF-IDF no captura similaridad semántica. "Contenedor Docker" y
"imagen de contenedor" pueden tener baja similitud TF-IDF pese a ser equivalentes.

**Acción:**
- Integrar `sentence-transformers` con el modelo `paraphrase-multilingual-MiniLM-L12-v2`
  (soporte nativo en español, ~120 MB).
- Calcular embeddings de cada documento al indexar y almacenarlos.
- Exponer un endpoint `POST /buscar` que reciba una consulta en lenguaje natural y devuelva
  los N contenidos más similares (cosine similarity).
- Alternativa ligera: usar la **matriz TF-IDF existente** + `cosine_similarity` de scikit-learn
  para un sistema de recomendación sin modelos adicionales (costo cero).

---

### 🟡 DS-007 · Sistema de recomendación de contenidos relacionados
**Objetivo:** dado un contenido ingresado, sugerir los K más similares del repositorio.

**Implementación sugerida (MVP rápido):**
```python
from sklearn.metrics.pairwise import cosine_similarity

def recomendar(texto_consulta: str, top_k: int = 3):
    vector_consulta = tfidf_vectorizer.transform([limpiar_texto(texto_consulta)])
    similitudes = cosine_similarity(vector_consulta, X_matrix).flatten()
    top_indices = similitudes.argsort()[::-1][:top_k]
    return df.iloc[top_indices][["titulo", "categoria"]].to_dict(orient="records")
```
- Requiere mantener `X_matrix` (la matriz TF-IDF del corpus completo) persistida junto con
  los `.joblib`.
- Endpoint sugerido: `POST /recomendar` → devuelve lista de `{titulo, categoria, similitud}`.

---

### 🟡 DS-008 · Explicabilidad del modelo (XAI)
**Objetivo:** que el usuario entienda **por qué** el modelo asignó una categoría.

**Acciones:**
- Implementar `eli5` o `LIME` para mostrar los tokens que más influyeron en la predicción.
- Añadir campo opcional `explicacion` en la respuesta JSON:
  ```json
  {
    "categoria": "DevOps",
    "probabilidad": 0.74,
    "informaciones_adicionales": ["kubernetes", "docker", "pods"],
    "explicacion": ["kubernetes (+0.42)", "despliegue (+0.31)", "contenedor (+0.27)"]
  }
  ```
- Alternativa sin dependencias extra: usar los coeficientes de la Regresión Logística
  (`modelo.coef_`) para extraer los top tokens por clase.

---

### 🟡 DS-009 · Procesamiento en lote (CSV / JSON array)
**Objetivo:** permitir clasificar múltiples contenidos en una sola llamada.

**Acción:**
- Agregar endpoint `POST /contenido/batch` que reciba un array JSON o archivo CSV y devuelva
  un array de resultados.
- Implementar `procesar_batch(filas: list[dict]) -> list[dict]` usando `vectorizer.transform`
  sobre el batch completo (más eficiente que llamar `procesar_contenido` N veces).

---

## Fase 3 — Escala y producción (futuro)

### 🟢 DS-010 · Migración a embeddings densos con fine-tuning
**Objetivo:** superar las limitaciones de TF-IDF para textos técnicos en español.

**Acciones:**
- Fine-tune de `bert-base-multilingual-cased` o `dccuchile/bert-base-spanish-wwm-cased`
  (BETO) sobre el dataset ampliado.
- Usar Hugging Face `Trainer` API con el dataset propio.
- Evaluar mejora en F1-macro frente al pipeline TF-IDF + LogReg.
- Requisito: dataset de al menos 500 ejemplos por categoría para fine-tuning efectivo.

---

### 🟢 DS-011 · Reentrenamiento automatizado (MLOps básico) — 🟡 Parcialmente completado (Local)
**Objetivo:** que el modelo se actualice cuando se incorporen nuevos contenidos.

**Acciones:**
- **Localmente implementado:** El script `ingest_documents.py` detecta si se insertaron ≥ 3 documentos en una sesión y permite re-entrenar el modelo localmente de forma automática invocando a Jupyter en segundo plano.
- **Pendiente:** Integrar orquestación con GitHub Actions (trigger semanal o por commit) y subir automáticamente los nuevos `.joblib` a OCI Object Storage.
- Registro de experimentos con MLflow o un log simple en OCI Object Storage.

---

### 🟢 DS-012 · Detección de categorías nuevas (zero-shot / few-shot)
**Objetivo:** que el sistema clasifique contenidos en categorías que no existen en el
dataset de entrenamiento, sin necesidad de reentrenar.

**Acciones:**
- Integrar un modelo de clasificación zero-shot (p. ej. `facebook/bart-large-mnli` vía
  Hugging Face Inference API) como fallback cuando la probabilidad del clasificador local
  es baja (< umbral configurable, sugerido 0.40).
- Esto cubre casos como una nueva categoría "IA / LLMs" que no estaba en el dataset original.

---

### 🟢 DS-013 · Dashboard de monitoreo del modelo
**Objetivo:** visibilidad operativa sobre las predicciones en producción.

**Acciones:**
- Loguear cada predicción (timestamp, categoria, probabilidad, longitud del texto).
- Dashboard simple con Streamlit o Metabase mostrando: distribución de categorías predichas,
- Dashboard simple con Streamlit o Metabase mostrando: distribución de categorías predichas,
  distribución de probabilidades (alertar si muchas predicciones caen bajo 0.50), drift de
  vocabulario (términos nuevos no vistos en entrenamiento).

---

## Fixes conocidos (bugs / deuda técnica)

| ID | Severidad | Descripción |
|----|-----------|-------------|
| FIX-001 | 🔴 Alta | `min_df=1` en el vectorizador hace que cada término aparezca como feature aunque solo esté en un documento — aumenta dimensionalidad sin aportar generalización. Cambiar a `min_df=2` cuando el dataset supere los 100 registros. |
| FIX-002 | 🟠 Media | La lista `STOPWORDS_ES` incluye frases completas ("se explica", "se presenta") que `TfidfVectorizer` trata como tokens individuales y **nunca coincidirán** con unigramas del vocabulario — son dead code. Eliminar o implementar filtrado post-tokenización. |
| FIX-003 | 🟠 Media | `ngram_range=(1,2)` con `max_features=1500` y solo ~60 documentos genera un vocabulario pequeño donde muchos bigramas son idiosincráticos del texto de entrenamiento — riesgo de sobreajuste. Evaluar reducir a `(1,1)` o aumentar `max_features` junto con el dataset. |
| FIX-004 | 🟡 Baja | No existe validación del campo `probabilidad` cuando ningún token del input está en el vocabulario del vectorizador (texto vacío o en otro idioma) — `predict_proba` devuelve distribución uniforme y la probabilidad reportada es ~0.125 (1/8 categorías), lo cual es engañoso. Añadir un umbral mínimo y un campo `confianza: "baja"` en la respuesta. |
| FIX-005 | ✅ Resuelto | ~~El notebook no incluye requirements.txt ni environment.yml — el equipo de Back-End no puede reproducir el entorno sin inspeccionar el código. Generar con pip freeze o conda env export.~~ Resuelto: Se creó `requirements.txt` que contiene todas las dependencias y se mantiene actualizado con cada nueva funcionalidad. |
| FIX-006 | 🟢 Muy baja | Las fechas en los `print` de ejemplos no están estandarizadas (algunas celdas usan `json.dumps` y otras `print` directo) — normalizar la salida para que sea 100% JSON válido en todas las celdas de demostración. |
| FIX-007 | ✅ Resuelto | ~~CSV como fuente de verdad obsoleta.~~ Resuelto: PostgreSQL es ahora la única fuente de verdad. El CSV queda como referencia histórica y fallback del script de migración. |
| FIX-008 | ✅ Resuelto | ~~Bug crítico en `app/main.py`: la variable `probabilidad` se usaba en `log_prediccion()` sin haber sido calculada, causando `NameError` en cada predicción.~~ Resuelto en v0.6.0: se agrega `proba_arr = modelo.predict_proba(vector)[0]` y `probabilidad = float(proba_arr.max())` antes de la llamada. |
| FIX-009 | ✅ Resuelto | ~~Las celdas de serialización del notebook guardaban los `.joblib` en `data-science/notebooks/` en lugar de `data-science/models/` (rutas relativas sin prefijo de directorio).~~ Resuelto en v0.6.0: rutas corregidas a `"../models/tfidf_vectorizer.joblib"` y `"../models/modelo_clasificador.joblib"`. |
| FIX-010 | ✅ Resuelto | ~~La columna en la tabla `predicciones` fue creada como `keywords` por el script de migración, mientras que `database.py` la referencia como `informaciones_adicionales`, causando error silencioso en el INSERT.~~ Resuelto en v0.6.0: columna renombrada vía `ALTER TABLE`. |

---

*Documento generado el 2026-07-15 — Última actualización: 2026-07-22 — TechMind G9 LATAM Team 37 · Rol: Ciencia de Datos.*
