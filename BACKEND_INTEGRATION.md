# 🔌 Guía de Integración — Backend (Java / Spring Boot)

> **¿Para quién es este documento?**
> Para el equipo de Backend que implementa la API REST en Java/Spring Boot.
> Explica cómo conectarse al microservicio Python (FastAPI) y a la base de datos PostgreSQL.

---

## Arquitectura del sistema (visión general)

```
  Postman / Cliente
       │
       │  POST /contenido  { "titulo": "...", "texto": "..." }
       ▼
┌──────────────────────────────────────────┐
│         Spring Boot — Puerto 8080        │  ← VOS implementás esto
│                                          │
│  1. Validar el request                   │
│  2. Llamar a FastAPI (HTTP interno)      │
│  3. Guardar el resultado en PostgreSQL   │
│  4. Devolver el JSON al cliente          │
└────────────────┬─────────────────────────┘
                 │  POST http://localhost:8000/predecir
                 │  (llamada interna, no expuesta al cliente)
                 ▼
┌──────────────────────────────────────────┐
│         FastAPI (Python) — Puerto 8000   │  ← implementado por DS (Ernesto)
│                                          │
│  • Carga los modelos .joblib al arrancar │
│  • Clasifica el texto                    │
│  • Devuelve categoria + probabilidad     │
│    + palabras clave                      │
└────────────────┬─────────────────────────┘
                 │
                 ▼
┌──────────────────────────────────────────┐
│         PostgreSQL — Puerto 5432         │
│         Base de datos: techmind          │
│                                          │
│  • contenidos   — dataset de entreno     │
│  • predicciones — log de inferencias     │
└──────────────────────────────────────────┘
```

**Regla clave:** Postman habla SOLO con Spring Boot.
FastAPI es un servicio interno — el cliente nunca lo llama directamente.

---

## Paso 1 — Levantar PostgreSQL (Docker)

Necesitás Docker instalado. Luego, desde la raíz del repositorio:

```bash
docker-compose up -d
```

Eso levanta PostgreSQL en `localhost:5432` con:

| Parámetro | Valor |
|-----------|-------|
| Host | `localhost` |
| Puerto | `5432` |
| Base de datos | `techmind` |
| Usuario | `techmind_user` |
| Contraseña | `techmind_pass` |

Verificar que PostgreSQL está corriendo:
```bash
docker ps
# Deberías ver: techmind-postgres   Up X seconds
```

---

## Paso 2 — Configurar variables de entorno (Python)

```bash
cp .env.example .env
# El .env ya tiene los valores correctos para desarrollo local — no hace falta editarlo
```

---

## Paso 3 — Migrar el dataset a PostgreSQL

```bash
pip install -r requirements.txt
python3 migrate_to_postgres.py
```

Salida esperada:
```
✅  Esquema creado/verificado en PostgreSQL
📂  Leyendo dataset desde CSV: contenidos_tecnicos.csv
    61 registros leídos
✅  61 registros insertados en PostgreSQL

📊  Distribución por categoría:
    Backend              12 registros
    Data Science         10 registros
    ...
```

---

## Paso 4 — Levantar FastAPI

Primero asegurate de que los modelos `.joblib` están generados
(Ernesto los genera corriendo el notebook).

```bash
uvicorn app.main:app --reload --port 8000
```

Salida esperada al arrancar:
```
✅  Modelos cargados correctamente
✅  Tabla 'predicciones' lista en PostgreSQL
INFO:     Uvicorn running on http://0.0.0.0:8000
```

Documentación automática disponible en: **http://localhost:8000/docs**

---

## Paso 5 — Verificar que FastAPI está operativa

```bash
curl http://localhost:8000/health
```

Respuesta esperada:
```json
{
  "status": "ok",
  "model_loaded": true,
  "version": "0.4.0"
}
```

---

## Contrato del endpoint interno `/predecir`

### `POST http://localhost:8000/predecir`

Este es el único endpoint que Spring Boot necesita llamar.

#### Request body (JSON)

```json
{
  "titulo": "Introducción a Spring Boot",
  "texto": "Conceptos básicos para la creación de APIs REST con Java y Spring Boot."
}
```

| Campo | Tipo | Requerido | Descripción |
|-------|------|-----------|-------------|
| `titulo` | `string` | ✅ Sí | Título del contenido técnico |
| `texto` | `string` | ✅ Sí | Descripción o cuerpo del contenido |

#### Response (200 OK)

```json
{
  "categoria": "Backend",
  "probabilidad": 0.8879,
  "informaciones_adicionales": ["spring boot", "java", "api rest", "creación apis", "spring"]
}
```

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `categoria` | `string` | Una de las 8 categorías (ver abajo) |
| `probabilidad` | `float` (0–1) | Confianza del modelo en esa categoría |
| `informaciones_adicionales` | `string[]` | Top 5 palabras clave del texto |

#### Categorías disponibles

`Backend` · `Frontend` · `Data Science` · `DevOps` · `Mobile` · `Bases de Datos` · `Seguridad` · `Cloud`

Consultable en tiempo real:
```bash
curl http://localhost:8000/categorias
```

#### Códigos de error

| Código | Cuándo ocurre | Qué hacer |
|--------|--------------|-----------|
| `422` | `titulo` o `texto` vacíos | Validar en Spring Boot antes de llamar |
| `503` | FastAPI arrancó pero los `.joblib` no se cargaron | Verificar que los archivos existen |
| `500` | Error interno inesperado | Revisar logs de FastAPI |

---

## Cómo llamar a FastAPI desde Spring Boot

### Opción A — `RestTemplate` (más simple)

```java
// Configuración del bean (una sola vez)
@Bean
public RestTemplate restTemplate() {
    return new RestTemplate();
}

// En el servicio o controlador
@Autowired
private RestTemplate restTemplate;

public PrediccionDTO clasificar(String titulo, String texto) {
    String url = "http://localhost:8000/predecir";

    Map<String, String> request = Map.of(
        "titulo", titulo,
        "texto",  texto
    );

    ResponseEntity<PrediccionDTO> response = restTemplate.postForEntity(
        url,
        request,
        PrediccionDTO.class
    );

    return response.getBody();
}
```

### Opción B — `WebClient` (reactivo, recomendado para proyectos nuevos)

```java
// Configuración del bean
@Bean
public WebClient webClient() {
    return WebClient.builder()
        .baseUrl("http://localhost:8000")
        .build();
}

// En el servicio
@Autowired
private WebClient webClient;

public PrediccionDTO clasificar(String titulo, String texto) {
    return webClient.post()
        .uri("/predecir")
        .contentType(MediaType.APPLICATION_JSON)
        .bodyValue(Map.of("titulo", titulo, "texto", texto))
        .retrieve()
        .bodyToMono(PrediccionDTO.class)
        .block();
}
```

### DTO que Spring Boot necesita

```java
// PrediccionDTO.java
public class PrediccionDTO {
    private String categoria;
    private double probabilidad;
    private List<String> informacionesAdicionales;

    // getters y setters...
}
```

> **Nota sobre el campo `informaciones_adicionales`:**
> En JSON viene con guión bajo (`informaciones_adicionales`).
> En Java usá `@JsonProperty("informaciones_adicionales")` si el nombre del atributo difiere:

```java
@JsonProperty("informaciones_adicionales")
private List<String> informacionesAdicionales;
```

---

## Configuración de Spring Boot (`application.properties`)

```properties
# PostgreSQL
spring.datasource.url=jdbc:postgresql://localhost:5432/techmind
spring.datasource.username=techmind_user
spring.datasource.password=techmind_pass
spring.datasource.driver-class-name=org.postgresql.Driver

# JPA / Hibernate
spring.jpa.hibernate.ddl-auto=update
spring.jpa.show-sql=false
spring.jpa.properties.hibernate.dialect=org.hibernate.dialect.PostgreSQLDialect

# URL interna de FastAPI (configurable por entorno)
techmind.ds.api.url=http://localhost:8000
```

Dependencia de PostgreSQL para `pom.xml`:
```xml
<dependency>
    <groupId>org.postgresql</groupId>
    <artifactId>postgresql</artifactId>
    <scope>runtime</scope>
</dependency>
```

---

## Schema de la base de datos (referencia para JPA)

### Tabla `contenidos` — el dataset de entrenamiento

```sql
CREATE TABLE contenidos (
    id          SERIAL PRIMARY KEY,
    titulo      TEXT        NOT NULL,
    texto       TEXT        NOT NULL,
    categoria   TEXT        NOT NULL,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

> Spring Boot puede leer esta tabla para mostrar el catálogo de contenidos disponibles.

### Tabla `predicciones` — log de inferencias

```sql
CREATE TABLE predicciones (
    id              SERIAL PRIMARY KEY,
    titulo          TEXT        NOT NULL,
    texto           TEXT        NOT NULL,
    categoria       TEXT        NOT NULL,
    probabilidad    FLOAT       NOT NULL,
    keywords        TEXT[]      NOT NULL,  -- array de strings en PostgreSQL
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

> FastAPI escribe en esta tabla automáticamente con cada predicción.
> Spring Boot puede leerla para mostrar historial, estadísticas, etc.

---

## Checklist de verificación completa

Antes de la demo, verificar que todo el stack local funciona:

```bash
# 1. PostgreSQL corriendo
docker ps | grep techmind-postgres

# 2. Dataset migrado
docker exec techmind-postgres psql -U techmind_user -d techmind \
  -c "SELECT COUNT(*) FROM contenidos;"
# → Debe mostrar: 61

# 3. FastAPI operativa
curl http://localhost:8000/health
# → {"status":"ok","model_loaded":true,"version":"0.4.0"}

# 4. Predicción funciona
curl -X POST http://localhost:8000/predecir \
  -H "Content-Type: application/json" \
  -d '{"titulo":"Spring Boot REST","texto":"API REST con Java y Spring Boot."}'
# → {"categoria":"Backend","probabilidad":0.88,"informaciones_adicionales":[...]}

# 5. La predicción se guardó en PostgreSQL
docker exec techmind-postgres psql -U techmind_user -d techmind \
  -c "SELECT titulo, categoria, probabilidad FROM predicciones LIMIT 5;"

# 6. Spring Boot puede conectarse a PostgreSQL
# → Verificar en los logs de Spring que no hay errores de conexión
```

---

## Testear el endpoint de Spring Boot con Postman

Una vez que Spring Boot expone `POST /contenido`:

**Configuración en Postman:**
- Método: `POST`
- URL: `http://localhost:8080/contenido`
- Headers: `Content-Type: application/json`
- Body (raw JSON):
```json
{
  "titulo": "Introducción a Spring Boot",
  "texto": "Conceptos básicos para la creación de APIs REST con Java y Spring Boot."
}
```

**Respuesta esperada (200 OK):**
```json
{
  "categoria": "Backend",
  "probabilidad": 0.8879,
  "informaciones_adicionales": ["spring boot", "java", "api rest", "creación apis", "spring"]
}
```

---

## Errores frecuentes y soluciones

| Error | Causa | Solución |
|-------|-------|---------|
| `Connection refused` en puerto 8000 | FastAPI no está corriendo | `uvicorn app.main:app --port 8000` |
| `Connection refused` en puerto 5432 | PostgreSQL no está corriendo | `docker-compose up -d` |
| `FileNotFoundError: tfidf_vectorizer.joblib` | Los modelos no están generados | Pedirle a Ernesto los `.joblib` o correr el notebook |
| `422 Unprocessable Entity` desde FastAPI | `titulo` o `texto` vacíos en el JSON | Validar en Spring Boot antes de llamar |
| `Cannot deserialize informaciones_adicionales` | Falta `@JsonProperty` en el DTO | Agregar `@JsonProperty("informaciones_adicionales")` |
| `FATAL: password authentication failed` | Credenciales incorrectas | Verificar `application.properties` con los valores del `.env.example` |

---

## Contacto

Cualquier duda sobre la parte de Ciencia de Datos o la API de FastAPI → **Ernesto** (rol DS).

Documentación adicional del componente de DS:
- [`README.md`](README.md) — visión general del proyecto
- [`DIAGRAMA_PIPELINE.md`](DIAGRAMA_PIPELINE.md) — cómo funciona el modelo internamente
- [`ROADMAP.md`](ROADMAP.md) — mejoras planificadas

---

*Documento preparado por el equipo de Ciencia de Datos — TechMind G9 LATAM Team 37.*
*Última actualización: 2026-07-21*
