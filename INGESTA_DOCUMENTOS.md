# 📄 Ingesta de Documentos — TechMind

> Guía para ampliar el dataset de entrenamiento con archivos PDF o DOCX.
> Cuantos más documentos reales agregues, mejor clasifica el modelo.

---

## ¿Por qué hacer esto?

El modelo actual fue entrenado con **61 registros sintéticos** → accuracy ~0.69.
Con **≥250 registros reales** el accuracy estimado sube a **≥0.82**.

Esta herramienta te permite subir cualquier artículo técnico, guía, documentación oficial
o apunte del equipo en formato PDF o DOCX, y el sistema lo procesa automáticamente.

---

## Setup (solo la primera vez)

```bash
pip install -r requirements.txt
```

---

## Uso — Tres formas de ejecutar

### Forma 1 — Procesar una carpeta completa (recomendado)

```bash
# 1. Colocá tus PDFs y DOCX en la carpeta documentos/
cp mis_guias/*.pdf documentos/
cp apuntes/*.docx documentos/

# 2. Ejecutar
python3 ingest_documents.py
```

El script procesa todos los archivos de la carpeta uno por uno.

---

### Forma 2 — Procesar un archivo específico

```bash
python3 ingest_documents.py --archivo guia_spring_boot.pdf
```

---

### Forma 3 — Archivo con categoría ya definida (sin preguntas)

```bash
python3 ingest_documents.py --archivo docker_intro.pdf --categoria DevOps
```

Útil cuando el tema del documento es obvio y no querés que el script te pregunte.

---

## ¿Qué pasa cuando ejecutás el script?

Para cada archivo, el script:

1. **Extrae el texto** del PDF o DOCX
2. **Limpia** saltos de página, headers/footers, líneas vacías repetidas
3. **Muestra un preview** de ~60 palabras del documento
4. **Pregunta si el documento cubre un solo tema o varios**:
   - Si es un **único tema** → lo inserta como un registro con la categoría que elijas
   - Si **cubre múltiples temas** → divide el documento en secciones y te pide una categoría para cada una
5. **Verifica duplicados**: si el mismo texto ya estaba en la base de datos, lo saltea
6. **Inserta en PostgreSQL** (tabla `contenidos`)

### Ejemplo de sesión interactiva

```
✅ Conectado a PostgreSQL

══════════════════════════════════════════════════════════════
  📂 arquitectura_microservicios.pdf
══════════════════════════════════════════════════════════════
  📄 arquitectura_microservicios.pdf
  Preview: "En este artículo exploramos los patrones de diseño
  para sistemas distribuidos usando microservicios con Spring..."
  📊 1842 palabras totales

  ¿Este documento cubre MÚLTIPLES categorías y querés dividirlo
  en secciones? [s/N]: N

  Categorías disponibles:
     1. Backend
     2. Frontend
     3. Data Science
     4. DevOps
     5. Mobile
     6. Bases de Datos
     7. Seguridad
     8. Cloud

  ¿Categoría? [1-8] (o 's' para saltear): 1

  ✅ Insertado: "Arquitectura Microservicios" → Backend
```

---

## Documentos multi-categoría

Si tenés un PDF que cubre varios temas (ej: "Guía de Spring Boot + Docker + PostgreSQL"),
respondé **s** cuando el script te pregunte si tiene múltiples categorías.

El script detecta las secciones automáticamente y te pide categoría para cada una:

```
  ¿Este documento cubre MÚLTIPLES categorías? [s/N]: s

  📑 Se detectaron 3 secciones:
    1. Spring Boot   — "Introducción a Spring Boot para crear APIs..."
    2. Docker        — "Contenerizar la aplicación con Docker..."
    3. Base de datos — "Conectar con PostgreSQL usando Spring Data..."

  ── Sección 1/3: Spring Boot
  ¿Categoría? [1-8]: 1    → Backend

  ── Sección 2/3: Docker
  ¿Categoría? [1-8]: 4    → DevOps

  ── Sección 3/3: Base de datos
  ¿Categoría? [1-8]: 6    → Bases de Datos
```

---

## Qué tipos de documentos usar

### ✅ Buenos para el modelo

| Tipo de documento | Categoría sugerida |
|-------------------|--------------------|
| Documentación oficial de Spring Boot | Backend |
| Tutoriales de React / Vue / Angular | Frontend |
| Artículos de Scikit-Learn / Pandas / PyTorch | Data Science |
| Guías de Docker, Kubernetes, CI/CD | DevOps |
| Documentación de Android / iOS / React Native | Mobile |
| Tutoriales de PostgreSQL, MongoDB, Redis | Bases de Datos |
| Guías de JWT, OAuth2, OWASP | Seguridad |
| Documentación de AWS, GCP, OCI, Azure | Cloud |

### ⚠️ Evitar

- PDFs escaneados (imágenes — el texto no se puede extraer)
- Documentos muy cortos (< 50 palabras) — poca información para el modelo
- PDFs protegidos con contraseña
- Documentos en idiomas distintos al español (el modelo fue entrenado en español)

---

## Después de ingestar — Re-entrenamiento automático

**Regla configurada:** el script te ofrece re-entrenar automáticamente cada vez que ingestás **3 o más documentos** en una sola sesión.

Cuando terminan de procesarse los archivos, si se insertó el umbral mínimo, el script pregunta:

```
  🔁 Se alcanzó el umbral de 3 documento(s) nuevo(s).
  ¿Re-entrenar el modelo ahora? [s/N]: s

  ⏳ Re-entrenando el modelo (esto puede tardar 1-2 minutos)...
  ✅ Modelo re-entrenado correctamente.
  💾 Nuevos .joblib generados: tfidf_vectorizer.joblib · modelo_clasificador.joblib
  ⚠️  Reiniciá FastAPI para que cargue los nuevos modelos:
        uvicorn app.main:app --port 8000
```

Si respondés **N**, podés re-entrenar más adelante manualmente:

### Re-entrenamiento manual

```bash
# Opción 1 — Automático (re-corre el notebook completo)
jupyter nbconvert --to notebook --execute TechMind_DataScience.ipynb
# Los nuevos .joblib se generan solos

# Opción 2 — Manual (abrí el notebook y ejecutá todas las celdas)
jupyter notebook TechMind_DataScience.ipynb
```

Después de re-entrenar, reiniciá FastAPI:

```bash
# Ctrl+C para detener FastAPI, luego:
uvicorn app.main:app --port 8000
```

---

## Verificar que los documentos se cargaron

```bash
# Total de registros
docker exec techmind-postgres psql -U techmind_user -d techmind \
  -c "SELECT COUNT(*) FROM contenidos;"

# Distribución por categoría
docker exec techmind-postgres psql -U techmind_user -d techmind \
  -c "SELECT categoria, COUNT(*) FROM contenidos GROUP BY categoria ORDER BY COUNT(*) DESC;"

# Últimos 5 documentos insertados
docker exec techmind-postgres psql -U techmind_user -d techmind \
  -c "SELECT titulo, categoria, created_at FROM contenidos ORDER BY created_at DESC LIMIT 5;"
```

---

## Solución de problemas

| Problema | Causa probable | Solución |
|----------|---------------|---------|
| `No se pudo extraer texto` | PDF escaneado (imagen) | Usar un PDF con texto seleccionable |
| `Documento ya existe` | Ya fue insertado antes | Normal — el script evita duplicados |
| `No se pudo conectar a PostgreSQL` | Docker no está corriendo | `docker-compose up -d` |
| `pdfplumber no instalado` | Falta dependencia | `pip install pdfplumber` |
| El texto extraído tiene caracteres raros | Encoding del PDF | Probar con otro PDF o convertirlo primero |
| Sección detectada con muy poco texto | El split automático no siempre es perfecto | Ignorar esa sección o editarla manualmente |

---

## Estructura de la carpeta `documentos/`

```
documentos/
├── .gitkeep                    # Mantiene la carpeta en el repo (no versionar los PDFs)
├── guia_spring_boot.pdf        ← tus archivos acá
├── tutorial_react.docx
├── intro_docker.pdf
└── ...
```

> **Nota:** Los archivos PDF/DOCX no se suben al repositorio (están en `.gitignore`).
> Son archivos locales de cada miembro del equipo.

---

*TechMind G9 LATAM Team 37 · Documentación de Ciencia de Datos.*
*Última actualización: 2026-07-21*
