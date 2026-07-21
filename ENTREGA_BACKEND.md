# 📦 Entrega al Equipo de Backend — TechMind DS

> **¿Para qué sirve este documento?**
> Lista exacta de lo que el equipo de Ciencia de Datos (Ernesto) le entrega
> al equipo de Backend (Java / Spring Boot) para que puedan arrancar la integración.

---

## ⚠️ Importante antes de empezar

Hay **dos formas de recibir los archivos**:

| Canal | Qué llega por ahí |
|-------|-------------------|
| 📁 **Repositorio GitHub** (clonar) | Todo el código fuente, documentación y scripts |
| 📨 **Compartido manualmente** (Drive / Slack / ZIP) | Los archivos del modelo (`.joblib`) — **NO están en el repo** |

Los modelos `.joblib` están excluidos del repositorio por `.gitignore` porque son artefactos
generados (binarios de ~100KB) que se regeneran corriendo el notebook.
**Sin ellos, FastAPI no puede arrancar.**

---

## Paso 1 — Clonar el repositorio

```bash
git clone https://github.com/ernes2111/G9-Tech-mind-Team-37.git
cd G9-Tech-mind-Team-37
```

El repo es **privado** — pedirle acceso a Ernesto si no pueden clonarlo.

---

## Paso 2 — Archivos que llegan por el repo ✅

Al clonar ya van a tener todo esto:

### Código del servicio FastAPI

| Archivo | Para qué sirve |
|---------|---------------|
| `app/main.py` | El microservicio que Spring Boot llama internamente |
| `app/database.py` | Conexión a PostgreSQL — crea tablas y guarda predicciones |
| `app/.__init__.py` | Módulo Python |

### Setup del entorno

| Archivo | Para qué sirve |
|---------|---------------|
| `docker-compose.yml` | Levanta PostgreSQL con un solo comando |
| `.env.example` | Plantilla de variables de entorno — copiar a `.env` |
| `requirements.txt` | Instalar todas las dependencias Python |
| `migrate_to_postgres.py` | Poblar la base de datos con el dataset de entrenamiento |
| `contenidos_tecnicos.csv` | El dataset de entrenamiento (fuente de datos) |

### Documentación

| Archivo | Contenido |
|---------|-----------|
| `BACKEND_INTEGRATION.md` | **👈 Leer primero** — guía completa de integración con código Java |
| `QA_TESTING.md` | Casos de prueba para el equipo de QA |
| `postman_collection.json` | Colección Postman lista para importar |
| `DIAGRAMA_PIPELINE.md` | Cómo funciona el modelo internamente |

---

## Paso 3 — Archivos que Ernesto comparte manualmente ⚠️

> Estos **NO están en el repositorio** — hay que pedirlos o generarlos.

| Archivo | Tamaño aprox. | Para qué sirve |
|---------|--------------|---------------|
| `tfidf_vectorizer.joblib` | ~44 KB | El vectorizador TF-IDF entrenado — convierte texto en números |
| `modelo_clasificador.joblib` | ~65 KB | El clasificador entrenado — predice la categoría |

**Dónde colocarlos:** en la raíz del repositorio (al mismo nivel que `app/`).

```
TechMind - G9 - LATAM - TEAM 37/
├── app/
├── tfidf_vectorizer.joblib        ← acá
├── modelo_clasificador.joblib     ← acá
├── docker-compose.yml
...
```

> **Alternativa:** si Ernesto no puede compartirlos, pueden generarlos localmente corriendo
> el notebook `TechMind_DataScience.ipynb` (requiere Python + Anaconda/Jupyter instalado).

---

## Paso 4 — Levantar el entorno completo

Una vez que tienen todo, el orden es:

```bash
# 1. Instalar dependencias Python
pip install -r requirements.txt

# 2. Levantar PostgreSQL (necesita Docker)
docker-compose up -d

# 3. Configurar variables de entorno
cp .env.example .env
# El .env ya tiene los valores correctos para desarrollo local

# 4. Poblar la base de datos
python3 migrate_to_postgres.py

# 5. Levantar FastAPI
uvicorn app.main:app --port 8000
```

Si FastAPI arranca bien, van a ver:
```
✅  Modelos cargados correctamente
✅  Tabla 'predicciones' lista en PostgreSQL
INFO:     Uvicorn running on http://0.0.0.0:8000
```

---

## Paso 5 — Verificar que todo funciona

```bash
# Health check — debe responder {"status":"ok","model_loaded":true}
curl http://localhost:8000/health

# Test de predicción
curl -X POST http://localhost:8000/predecir \
  -H "Content-Type: application/json" \
  -d '{"titulo":"Spring Boot REST","texto":"API REST con Java y Spring Boot, controladores y dependencias."}'
```

Respuesta esperada:
```json
{
  "categoria": "Backend",
  "probabilidad": 0.2955,
  "informaciones_adicionales": ["spring boot", "java", "api rest", "spring", "rest"]
}
```

---

## Paso 6 — Lo que implementa Spring Boot

Con FastAPI corriendo en `http://localhost:8000`, Spring Boot necesita:

1. **Llamar a `POST /predecir`** con `{ titulo, texto }` — ver `BACKEND_INTEGRATION.md` para el código Java
2. **Exponer `POST /contenido`** hacia Postman/cliente
3. **Conectarse a PostgreSQL** con los datos del `.env.example`

```properties
# application.properties de Spring Boot
spring.datasource.url=jdbc:postgresql://localhost:5432/techmind
spring.datasource.username=techmind_user
spring.datasource.password=techmind_pass
techmind.ds.api.url=http://localhost:8000
```

---

## Resumen rápido — Checklist ✅

### Ernesto entrega:
- [ ] Acceso al repositorio privado de GitHub
- [ ] `tfidf_vectorizer.joblib` (compartido manualmente)
- [ ] `modelo_clasificador.joblib` (compartido manualmente)
- [ ] Confirmación de que PostgreSQL y FastAPI funcionan localmente

### Backend recibe y hace:
- [ ] `git clone` del repositorio
- [ ] Copiar los `.joblib` a la raíz del repo
- [ ] `docker-compose up -d` → PostgreSQL corriendo
- [ ] `cp .env.example .env`
- [ ] `pip install -r requirements.txt`
- [ ] `python3 migrate_to_postgres.py` → 61 registros cargados
- [ ] `uvicorn app.main:app --port 8000` → FastAPI corriendo
- [ ] `curl http://localhost:8000/health` → `{"status":"ok","model_loaded":true}`
- [ ] Implementar Spring Boot que llame a `POST /predecir`

---

## Contacto

Cualquier problema con la configuración o los archivos → **Ernesto** (Ciencia de Datos).

Documentación completa de integración → [`BACKEND_INTEGRATION.md`](BACKEND_INTEGRATION.md)

---

*TechMind G9 LATAM Team 37 · Documento preparado por el equipo de Ciencia de Datos.*
*Última actualización: 2026-07-21*
