# Guía de Instalación y Configuración

## Requisitos Previos

| Herramienta | Versión mínima | Descripción |
|-------------|---------------|-------------|
| Java JDK | 17+ | Runtime de Spring Boot |
| Maven | 3.8+ (o usar `./mvnw`) | Build tool (incluido en el repo) |
| Docker | Cualquier versión reciente | Para levantar PostgreSQL |
| Docker Compose | v2+ | Orquestación de contenedores |

> El microservicio FastAPI (Data Science) es externo a este repositorio. Consultar [INTEGRACION_FASTAPI.md](INTEGRACION_FASTAPI.md) para su configuración.

---

## 1. Clonar el Repositorio

```bash
git clone <url-del-repositorio>
cd g9-techmind-team37
```

---

## 2. Configurar Variables de Entorno

El archivo `.env` en la raíz del proyecto ya contiene los valores por defecto para desarrollo local:

```env
PG_HOST=localhost
PG_PORT=5432
PG_DB=techmind
PG_USER=techmind_user
PG_PASSWORD=techmind_pass
TECHMIND_DS_API_URL=http://localhost:8000
```

> Para producción o entornos distintos, modificar estos valores según corresponda.

---

## 3. Levantar la Base de Datos

```bash
# Desde la raíz del proyecto
docker-compose up -d
```

Esto levanta un contenedor **PostgreSQL 16** con:
- Base de datos: `techmind`
- Usuario: `techmind_user` / Contraseña: `techmind_pass`
- Puerto: `5432`
- Volumen persistente: `techmind_postgres_data`

### Verificar que PostgreSQL está listo

```bash
docker-compose ps
# El estado debe ser "healthy"
```

### Detener la base de datos

```bash
docker-compose down
```

### Eliminar los datos persistidos (reset completo)

```bash
docker-compose down -v
```

---

## 4. Levantar la API Spring Boot

```bash
cd api/api

# Con Maven Wrapper (recomendado, no requiere Maven instalado)
./mvnw spring-boot:run

# Con Maven instalado globalmente
mvn spring-boot:run
```

> En Windows usar `mvnw.cmd` en lugar de `./mvnw`:
> ```cmd
> mvnw.cmd spring-boot:run
> ```

La aplicación inicia en **`http://localhost:8080`**.

Al arrancar, **Flyway ejecuta automáticamente** las migraciones SQL pendientes (crea las tablas `contenidos` y `predicciones` si no existen).

---

## 5. Verificar que Todo Funciona

### Health check básico

```bash
# Debe retornar HTTP 405 (Method Not Allowed) — el endpoint solo acepta POST
curl -i http://localhost:8080/contenido
```

### Prueba con el microservicio FastAPI levantado

```bash
curl -X POST http://localhost:8080/contenido \
  -H "Content-Type: application/json" \
  -d '{
    "titulo": "Test de integración",
    "texto": "Este es un texto de prueba para verificar que el sistema funciona correctamente."
  }'
```

**Respuesta esperada (HTTP 201):**
```json
{
  "categoria": "...",
  "probabilidad": 0.XX,
  "informaciones_adicionales": ["...", "..."]
}
```

---

## 6. Ejecutar los Tests

```bash
cd api/api

# Ejecutar todos los tests
./mvnw test

# En Windows
mvnw.cmd test
```

---

## Configuración Avanzada

### Cambiar el puerto de la API

Agregar en `application.properties`:
```properties
server.port=9090
```

### Cambiar la URL del microservicio FastAPI

En `application.properties`:
```properties
techmind.ds.api.url=http://mi-servidor-fastapi:8000
```

### Logs de SQL

Por defecto el SQL está activado en modo desarrollo. Para desactivarlo:
```properties
spring.jpa.show-sql=false
```

---

## Estructura de Puertos por Defecto

| Servicio | Puerto |
|----------|--------|
| Spring Boot API | `8080` |
| PostgreSQL | `5432` |
| FastAPI (DS) — externo | `8000` |

---

## Troubleshooting

### Error: `Connection refused` al iniciar Spring Boot

**Causa:** PostgreSQL no está corriendo.  
**Solución:** `docker-compose up -d` y esperar que el health check sea `healthy`.

### Error: `503 Service Unavailable` al llamar `/contenido`

**Causa:** El microservicio FastAPI no está corriendo o no es accesible en `http://localhost:8000`.  
**Solución:** Levantar el microservicio FastAPI. Ver [INTEGRACION_FASTAPI.md](INTEGRACION_FASTAPI.md).

### Error de Flyway al arrancar: `Schema-version mismatch`

**Causa:** La base de datos tiene un estado inconsistente con las migraciones.  
**Solución:** `docker-compose down -v && docker-compose up -d` para resetear completamente la base de datos.

### Puerto `8080` ya en uso

**Causa:** Otro proceso usa el puerto.  
**Solución:** Cambiar el puerto en `application.properties` o matar el proceso con `netstat -ano | findstr :8080` (Windows) / `lsof -i :8080` (Linux/Mac).
