# 🧪 Guía de QA — TechMind · Equipo 37

> **¿Para quién es este documento?**
> Para el equipo de QA que valida que el sistema clasifica textos correctamente
> y que la integración entre Spring Boot y FastAPI funciona de extremo a extremo.

---

## Arquitectura a testear

```
Postman (QA)
     │  POST /contenido  { titulo, texto }
     ▼
Spring Boot — Puerto 8080        ← punto de entrada QA
     │  llama internamente
     ▼
FastAPI — Puerto 8000            ← microservicio DS
     │  guarda predicción
     ▼
PostgreSQL — Puerto 5432         ← verificación en base de datos
```

**Regla importante:** QA siempre prueba contra **Spring Boot (puerto 8080)**.
FastAPI (puerto 8000) es un servicio interno — solo el equipo de DS lo usa directamente.

---

## Ambiente de pruebas — Setup

### Requisitos previos

| Herramienta | Versión mínima | Para qué |
|-------------|---------------|---------|
| Docker Desktop | cualquiera | correr PostgreSQL |
| Postman | cualquiera | ejecutar los test cases |
| Java / Spring Boot | JDK 17+ | la API que QA prueba |
| Python 3.10+ + Conda | 3.10+ | correr FastAPI (DS lo levanta) |

### Levantar el entorno completo

```bash
# 1. PostgreSQL
docker-compose up -d

# 2. Migrar datos (solo la primera vez)
cp .env.example .env
python3 migrate_to_postgres.py

# 3. FastAPI (lo levanta el equipo de DS)
uvicorn app.main:app --port 8000

# 4. Spring Boot (lo levanta el equipo de Backend)
./mvnw spring-boot:run   # o desde IntelliJ
```

### Verificar que todo está operativo antes de testear

```bash
# PostgreSQL
docker exec techmind-postgres psql -U techmind_user -d techmind \
  -c "SELECT COUNT(*) FROM contenidos;"
# → debe retornar: 61

# FastAPI (interno — QA no prueba esto en prod, pero sí en local)
curl http://localhost:8000/health
# → {"status":"ok","model_loaded":true,"version":"0.4.0"}

# Spring Boot
curl http://localhost:8080/actuator/health
# → {"status":"UP"}
```

---

## Endpoints a testear

### Endpoint principal — `POST /contenido` (Spring Boot)

| Propiedad | Valor |
|-----------|-------|
| Método | `POST` |
| URL | `http://localhost:8080/contenido` |
| Content-Type | `application/json` |
| Autenticación | Ninguna (MVP local) |

**Request body:**
```json
{
  "titulo": "string",
  "texto": "string"
}
```

**Response exitosa (200 OK):**
```json
{
  "categoria": "Backend",
  "probabilidad": 0.2955,
  "informaciones_adicionales": ["boot", "spring boot", "spring", "rest", "java spring"]
}
```

### Endpoints secundarios de FastAPI (para validación interna de DS)

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `http://localhost:8000/health` | GET | Verifica que el modelo está cargado |
| `http://localhost:8000/categorias` | GET | Lista las 8 categorías disponibles |
| `http://localhost:8000/predecir` | POST | Mismo contrato que `/contenido` de Spring Boot |
| `http://localhost:8000/docs` | GET | Documentación Swagger interactiva |

---

## 🟢 Casos de prueba — Happy Path (deben funcionar)

### TC-001 · Clasificación Backend
**Descripción:** texto claramente relacionado con Java y Spring Boot.

**Request:**
```json
{
  "titulo": "Introducción a Spring Boot",
  "texto": "Conceptos básicos para la creación de APIs REST con Java y Spring Boot. Incluye configuración de dependencias, controladores y manejo de excepciones."
}
```

**Respuesta esperada (200 OK):**
```json
{
  "categoria": "Backend",
  "probabilidad": 0.XX,
  "informaciones_adicionales": ["spring boot", "java", "api rest", "spring", "controladores"]
}
```
✅ **Validar:** `categoria == "Backend"` · `probabilidad > 0.0` · `informaciones_adicionales` no vacío

---

### TC-002 · Clasificación Data Science
**Request:**
```json
{
  "titulo": "Machine Learning con Scikit-Learn",
  "texto": "Pipeline de clasificación usando TF-IDF y regresión logística para análisis de textos en español. Incluye vectorización, entrenamiento y evaluación del modelo."
}
```
✅ **Validar:** `categoria == "Data Science"`

---

### TC-003 · Clasificación Frontend
**Request:**
```json
{
  "titulo": "Componentes en React",
  "texto": "Uso de hooks como useState y useEffect para manejar el estado en aplicaciones React. Incluye ejemplos de componentes funcionales y ciclo de vida."
}
```
✅ **Validar:** `categoria == "Frontend"`

---

### TC-004 · Clasificación DevOps
**Request:**
```json
{
  "titulo": "Despliegue con Docker y Kubernetes",
  "texto": "Creación de imágenes Docker, configuración de contenedores y orquestación con Kubernetes. Pipelines de CI/CD con GitHub Actions."
}
```
✅ **Validar:** `categoria == "DevOps"`

---

### TC-005 · Clasificación Cloud
**Request:**
```json
{
  "titulo": "Servicios en Oracle Cloud OCI",
  "texto": "Uso de OCI Object Storage, Compute instances y redes virtuales para desplegar aplicaciones escalables en la nube de Oracle."
}
```
✅ **Validar:** `categoria == "Cloud"`

---

### TC-006 · Clasificación Mobile
**Request:**
```json
{
  "titulo": "Desarrollo de apps con React Native",
  "texto": "Creación de aplicaciones móviles multiplataforma para Android e iOS usando React Native, navegación con React Navigation y consumo de APIs REST."
}
```
✅ **Validar:** `categoria == "Mobile"`

---

### TC-007 · Clasificación Bases de Datos
**Request:**
```json
{
  "titulo": "Consultas avanzadas en PostgreSQL",
  "texto": "Uso de JOINs, índices, transacciones ACID y procedimientos almacenados en PostgreSQL. Optimización de queries y análisis de planes de ejecución."
}
```
✅ **Validar:** `categoria == "Bases de Datos"`

---

### TC-008 · Clasificación Seguridad
**Request:**
```json
{
  "titulo": "Autenticación con JWT y OAuth2",
  "texto": "Implementación de autenticación stateless con JSON Web Tokens. Flujos de autorización OAuth2, manejo de refresh tokens y buenas prácticas de seguridad."
}
```
✅ **Validar:** `categoria == "Seguridad"`

---

### TC-009 · Verificar que la predicción se guardó en PostgreSQL
Luego de cualquier TC-001 al TC-008, ejecutar:
```bash
docker exec techmind-postgres psql -U techmind_user -d techmind \
  -c "SELECT titulo, categoria, ROUND(probabilidad::numeric, 4), created_at FROM predicciones ORDER BY created_at DESC LIMIT 1;"
```
✅ **Validar:** el registro más reciente coincide con el último request enviado.

---

## 🟡 Casos de prueba — Edge Cases (comportamiento esperado definido)

### TC-010 · Texto muy corto (1 palabra)
**Request:**
```json
{
  "titulo": "Java",
  "texto": "Java"
}
```
✅ **Validar:** devuelve `200 OK` con alguna categoría · `probabilidad` puede ser baja (~0.12) · `informaciones_adicionales` puede ser vacío `[]`

---

### TC-011 · Texto en inglés
**Request:**
```json
{
  "titulo": "Introduction to React Hooks",
  "texto": "React hooks allow functional components to use state and side effects. useState, useEffect, and custom hooks."
}
```
✅ **Validar:** devuelve `200 OK` · el modelo intenta clasificar (puede equivocarse, es esperado con texto en inglés)

---

### TC-012 · Texto mezclado (español + inglés)
**Request:**
```json
{
  "titulo": "Tutorial de Docker containers",
  "texto": "Aprenderemos a crear Docker images y deployar containers en producción usando Kubernetes."
}
```
✅ **Validar:** devuelve `200 OK` · probablemente clasifica como `DevOps` o `Cloud`

---

### TC-013 · Texto muy largo (>500 palabras)
**Request:** enviar un texto con varios párrafos de documentación técnica.
✅ **Validar:** devuelve `200 OK` en menos de 2 segundos · la respuesta tiene el mismo formato JSON

---

### TC-014 · Caracteres especiales en el texto
**Request:**
```json
{
  "titulo": "API REST con Spring Boot & JWT 🚀",
  "texto": "Configuración de seguridad: autenticación JWT + OAuth2 (Bearer tokens). URL: /api/v1/auth/login?redirect=true"
}
```
✅ **Validar:** devuelve `200 OK` · los caracteres especiales no rompen la respuesta

---

### TC-015 · Título muy largo, texto vacío (solo espacios)
**Request:**
```json
{
  "titulo": "Este es un título extremadamente largo que tiene muchas palabras y sigue y sigue sin decir nada técnico en particular",
  "texto": "   "
}
```
⚠️ **Comportamiento esperado:** `422 Unprocessable Entity` — texto vacío no es válido.

---

## 🔴 Casos de prueba — Error Handling (deben devolver error)

### TC-016 · Campo `titulo` faltante
**Request:**
```json
{
  "texto": "Texto sin titulo"
}
```
❌ **Esperado:** `422 Unprocessable Entity`
```json
{
  "detail": [{ "msg": "Field required", "loc": ["body", "titulo"] }]
}
```

---

### TC-017 · Campo `texto` faltante
**Request:**
```json
{
  "titulo": "Titulo sin texto"
}
```
❌ **Esperado:** `422 Unprocessable Entity`

---

### TC-018 · Ambos campos vacíos
**Request:**
```json
{
  "titulo": "",
  "texto": ""
}
```
❌ **Esperado:** `422 Unprocessable Entity`

---

### TC-019 · Body completamente vacío
**Request:** `POST /contenido` sin body.
❌ **Esperado:** `422 Unprocessable Entity`

---

### TC-020 · Content-Type incorrecto
**Request:** `POST /contenido` con `Content-Type: text/plain` y body `"hola"`.
❌ **Esperado:** `415 Unsupported Media Type` o `422 Unprocessable Entity`

---

### TC-021 · Método HTTP incorrecto
**Request:** `GET /contenido`
❌ **Esperado:** `405 Method Not Allowed`

---

## 📊 Validaciones de formato de respuesta

Para **toda respuesta exitosa (200 OK)**, validar:

| Campo | Tipo | Restricción |
|-------|------|-------------|
| `categoria` | `string` | Debe ser exactamente uno de: `"Backend"`, `"Bases de Datos"`, `"Cloud"`, `"Data Science"`, `"DevOps"`, `"Frontend"`, `"Mobile"`, `"Seguridad"` |
| `probabilidad` | `number` | `0.0 < probabilidad ≤ 1.0` |
| `informaciones_adicionales` | `array` de `string` | Entre 0 y 5 elementos · cada elemento es una cadena no vacía |

---

## ⚡ Prueba de rendimiento básica

### TC-022 · Tiempo de respuesta
Enviar 10 requests consecutivos al endpoint `/contenido` y medir el tiempo de cada uno.

✅ **Esperado:**
- Cada request: **< 500ms**
- Promedio: **< 200ms**
- Ninguno supera **1000ms**

### TC-023 · Requests simultáneos
Enviar 5 requests al mismo tiempo (usar Postman Runner o Newman).
✅ **Esperado:** todos responden correctamente, sin errores `503` ni timeouts.

---

## 🔍 Verificación de integridad en PostgreSQL

Luego de correr toda la suite de tests, verificar el estado de la base de datos:

```bash
# Total de predicciones registradas
docker exec techmind-postgres psql -U techmind_user -d techmind \
  -c "SELECT COUNT(*) FROM predicciones;"

# Distribución de predicciones por categoría
docker exec techmind-postgres psql -U techmind_user -d techmind \
  -c "SELECT categoria, COUNT(*) FROM predicciones GROUP BY categoria ORDER BY COUNT(*) DESC;"

# Verificar que probabilidad siempre está entre 0 y 1
docker exec techmind-postgres psql -U techmind_user -d techmind \
  -c "SELECT COUNT(*) FROM predicciones WHERE probabilidad < 0 OR probabilidad > 1;"
# → debe retornar: 0

# Verificar que keywords nunca es NULL
docker exec techmind-postgres psql -U techmind_user -d techmind \
  -c "SELECT COUNT(*) FROM predicciones WHERE keywords IS NULL;"
# → debe retornar: 0
```

---

## 📋 Colección Postman — Importación rápida

Importar el archivo `postman_collection.json` que está en la raíz del repositorio.

O crear manualmente en Postman las siguientes variables de entorno:

| Variable | Valor local |
|----------|-------------|
| `BASE_URL` | `http://localhost:8080` |
| `DS_URL` | `http://localhost:8000` |

---

## ✅ Checklist de regresión pre-demo

Antes de la presentación final, correr este checklist completo:

- [ ] `GET /health` → `{"status":"ok","model_loaded":true}`
- [ ] `GET /categorias` → lista con exactamente 8 categorías
- [ ] TC-001 a TC-008 → cada uno clasifica en la categoría correcta
- [ ] TC-009 → predicciones guardadas en PostgreSQL
- [ ] TC-016 a TC-019 → errores retornan `422`
- [ ] TC-022 → tiempo de respuesta < 500ms
- [ ] PostgreSQL: `SELECT COUNT(*) FROM predicciones` > 0
- [ ] PostgreSQL: ninguna `probabilidad` fuera de rango 0–1
- [ ] Swagger UI accesible en `http://localhost:8000/docs`

---

## ❓ Preguntas frecuentes de QA

**¿A qué URL envío los tests?**
→ Siempre a `http://localhost:8080/contenido` (Spring Boot). Nunca directamente al puerto 8000.

**¿Cómo sé si FastAPI está caída?**
→ Spring Boot debería retornar `503 Service Unavailable`. Si retorna `500`, verificar los logs de FastAPI.

**El modelo clasificó mal un texto, ¿es un bug?**
→ No necesariamente. El modelo tiene un accuracy del ~69% con el dataset actual. Si la clasificación es razonable (ej: clasifica "Docker" como "Cloud" en lugar de "DevOps"), no es un bug sino una limitación del dataset pequeño.

**¿Qué hago si PostgreSQL no levanta?**
→ `docker-compose down -v && docker-compose up -d` y re-ejecutar `python3 migrate_to_postgres.py`.

**¿Puedo probar directamente FastAPI en `/predecir`?**
→ Sí, en entorno local para debugging. En producción FastAPI no estará expuesto públicamente.

---

## Contacto

Dudas sobre el comportamiento esperado del modelo o la API de DS → **Ernesto** (Ciencia de Datos).
Dudas sobre los endpoints de Spring Boot → **Equipo Backend**.

Documentación adicional:
- [`BACKEND_INTEGRATION.md`](BACKEND_INTEGRATION.md) — detalles de integración Spring Boot ↔ FastAPI
- [`DIAGRAMA_PIPELINE.md`](DIAGRAMA_PIPELINE.md) — cómo funciona el modelo internamente
- `http://localhost:8000/docs` — Swagger UI con todos los endpoints de FastAPI

---

*Documento preparado por el equipo de Ciencia de Datos — TechMind G9 LATAM Team 37.*
*Última actualización: 2026-07-21*
