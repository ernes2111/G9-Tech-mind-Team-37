# Guía de Integración — Microservicio FastAPI (Data Science)

> Este documento está dirigido al equipo o IA responsable de construir/conectar el **microservicio de Machine Learning** que consume el backend Spring Boot de TechMind.

---

## Contexto

El backend Spring Boot actúa como intermediario entre el cliente final y el modelo ML. Cuando recibe una solicitud de clasificación, la reenvía **sincrónicamente** al microservicio FastAPI y aguarda la respuesta antes de contestar al cliente.

```
Cliente → POST /contenido → Spring Boot :8080 → POST /predecir → FastAPI :8000
                                 ↑___________________________________|
                                          respuesta del modelo
```

---

## Contrato de la API que debe implementar FastAPI

### Endpoint requerido

```
POST /predecir
```

Spring Boot construye la URL como:
```
{TECHMIND_DS_API_URL}/predecir
```
Por defecto: `http://localhost:8000/predecir`

---

### Request que enviará Spring Boot

**Headers:**
```
Content-Type: application/json
```

**Body JSON:**
```json
{
  "titulo": "string — título del contenido",
  "texto":  "string — cuerpo completo del contenido"
}
```

**Ejemplo:**
```json
{
  "titulo": "ChatGPT supera los 100 millones de usuarios",
  "texto": "La inteligencia artificial desarrollada por OpenAI continúa batiendo récords..."
}
```

---

### Response que DEBE retornar FastAPI

**HTTP Status:** `200 OK`

**Body JSON:**
```json
{
  "categoria": "string",
  "probabilidad": 0.94,
  "informaciones_adicionales": ["keyword1", "keyword2", "keyword3"]
}
```

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `categoria` | `string` | Categoría del contenido (ej: `"tecnología"`, `"política"`, `"deportes"`) |
| `probabilidad` | `float` | Confianza del modelo entre `0.0` y `1.0` |
| `informaciones_adicionales` | `string[]` | Lista de palabras clave relevantes (puede ser `[]`) |

**Ejemplo:**
```json
{
  "categoria": "tecnología",
  "probabilidad": 0.94,
  "informaciones_adicionales": ["ChatGPT", "OpenAI", "inteligencia artificial", "usuarios"]
}
```

---

## ⚠️ Restricciones Críticas

### Nombres de campos — NO modificar

Spring Boot parsea la respuesta con **expresiones regulares** sobre los nombres literales de los campos. Los nombres deben ser exactamente:

| Nombre esperado | ✅ Correcto | ❌ Incorrecto |
|-----------------|-----------|--------------|
| `categoria` | `"categoria": "tech"` | `"category": "tech"` |
| `probabilidad` | `"probabilidad": 0.9` | `"probability": 0.9` |
| `informaciones_adicionales` | `"informaciones_adicionales": [...]` | `"keywords": [...]` |

### Timeout

Spring Boot espera la respuesta en máximo **10 segundos**. Si FastAPI tarda más, la petición falla con `503 Service Unavailable`. El modelo ML debe responder dentro de ese límite.

### Código HTTP de respuesta

- ✅ `2xx` → Spring Boot procesa la respuesta como exitosa
- ❌ Cualquier otro código → Spring Boot retorna `503` al cliente

---

## Template Mínimo de Implementación (FastAPI)

```python
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI(title="TechMind DS API", version="1.0.0")


class ContenidoRequest(BaseModel):
    titulo: str
    texto: str


class PrediccionResponse(BaseModel):
    categoria: str
    probabilidad: float
    informaciones_adicionales: List[str]


@app.post("/predecir", response_model=PrediccionResponse)
def predecir(request: ContenidoRequest) -> PrediccionResponse:
    """
    Clasifica un contenido textual y retorna la categoría predicha,
    la probabilidad de confianza y palabras clave relevantes.
    """
    # ── Tu lógica de ML aquí ──────────────────────────────
    categoria = modelo.predict(request.titulo, request.texto)
    probabilidad = modelo.predict_proba()
    keywords = modelo.extract_keywords(request.texto)
    # ─────────────────────────────────────────────────────

    return PrediccionResponse(
        categoria=categoria,
        probabilidad=probabilidad,
        informaciones_adicionales=keywords
    )
```

**Para correr FastAPI:**
```bash
pip install fastapi uvicorn
uvicorn main:app --host 0.0.0.0 --port 8000
```

---

## Configuración de Conexión

### URL del servicio FastAPI

Configurada en dos lugares:

**`application.properties`:**
```properties
techmind.ds.api.url=http://localhost:8000
```

**`.env`:**
```
TECHMIND_DS_API_URL=http://localhost:8000
```

Para apuntar a otro host (ej: contenedor Docker, servidor remoto), cambiar `localhost` por la IP o nombre del servicio correspondiente.

### Timeouts configurados en Spring Boot

| Tipo | Valor |
|------|-------|
| Connect timeout | 5 segundos |
| Read timeout | 10 segundos |

---

## Pruebas de Integración

### Verificar FastAPI de forma aislada

```bash
curl -X POST http://localhost:8000/predecir \
  -H "Content-Type: application/json" \
  -d '{
    "titulo": "Messi gana el Balón de Oro",
    "texto": "El astro argentino se consagra nuevamente como el mejor del mundo..."
  }'
```

**Respuesta esperada:**
```json
{
  "categoria": "deportes",
  "probabilidad": 0.97,
  "informaciones_adicionales": ["Messi", "fútbol", "Balón de Oro", "Argentina"]
}
```

### Probar el flujo completo (Spring Boot → FastAPI → PostgreSQL)

```bash
curl -X POST http://localhost:8080/contenido \
  -H "Content-Type: application/json" \
  -d '{
    "titulo": "Messi gana el Balón de Oro",
    "texto": "El astro argentino se consagra nuevamente como el mejor del mundo..."
  }'
```

**Respuesta esperada (HTTP 201):**
```json
{
  "categoria": "deportes",
  "probabilidad": 0.97,
  "informaciones_adicionales": ["Messi", "fútbol", "Balón de Oro", "Argentina"]
}
```

---

## Checklist de Integración

- [ ] FastAPI corre en `http://localhost:8000` (o la URL configurada)
- [ ] El endpoint `POST /predecir` está implementado
- [ ] La respuesta incluye exactamente: `categoria`, `probabilidad`, `informaciones_adicionales`
- [ ] `probabilidad` es un número flotante entre `0.0` y `1.0`
- [ ] `informaciones_adicionales` es un array de strings (puede estar vacío: `[]`)
- [ ] El modelo responde en menos de **10 segundos**
- [ ] FastAPI retorna `200 OK` en clasificaciones exitosas
- [ ] PostgreSQL está corriendo: `docker-compose up -d`
- [ ] Spring Boot levantó correctamente en el puerto `8080`

---

## Variables de Entorno de Referencia

| Variable | Valor por defecto | Descripción |
|----------|-------------------|-------------|
| `PG_HOST` | `localhost` | Host de PostgreSQL |
| `PG_PORT` | `5432` | Puerto de PostgreSQL |
| `PG_DB` | `techmind` | Nombre de la base de datos |
| `PG_USER` | `techmind_user` | Usuario de PostgreSQL |
| `PG_PASSWORD` | `techmind_pass` | Contraseña de PostgreSQL |
| `TECHMIND_DS_API_URL` | `http://localhost:8000` | URL base del microservicio FastAPI |
