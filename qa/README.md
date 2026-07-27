# 🧪 Guía de Ejecución de QA y Testing — TechMind

Este documento describe la estrategia, las herramientas, la configuración del entorno y el procedimiento paso a paso para la ejecución de la suite de pruebas del proyecto **TechMind**.

---

## 🛠️ 1. Requisitos Previos y Herramientas

Para ejecutar la suite completa de pruebas necesitás contar con los siguientes elementos configurados:

* **Postman** (Desktop Client o Web).
* **Servidor de FastAPI** iniciado y escuchando en `http://localhost:8000`.
* **Base de datos PostgreSQL** operativa y conectada al microservicio.
* **Navegador Web** para el acceso a la documentación interactiva Swagger UI (`http://localhost:8000/docs`).

---

## ⚙️ 2. Configuración del Entorno de Pruebas

### Pasos para importar la Colección en Postman:
1. Abrí **Postman**.
2. Hacé clic en **Import** (esquina superior izquierda).
3. Seleccioná y cargá los siguientes archivos ubicados en la carpeta `postman/` de este repositorio:
   * `techmind_collection.json` *(Colección de peticiones y assertions)*.
   * `techmind_environment.json` *(Variables de entorno)*.
4. Seleccioná el entorno **TechMind - Local** en el desplegable superior derecho.
5. Verificá que la variable `base_url` apunte a `http://localhost:8000`.

---

## 📐 3. Cobertura de Pruebas (Matriz CP-01 a CP-20)

La suite cubre 6 dimensiones clave de calidad sobre el microservicio:

1. **Pruebas Funcionales / Flujo Feliz (7 Casos):**
   * Validación de clasificación de texto (`CP-01`), extracción de palabras clave (`CP-02`), cálculo de probabilidad entre 0 y 1 (`CP-03`), contrato JSON (`CP-09`), carga del modelo `.joblib` (`CP-10`), latencia < 2000 ms (`CP-11`),  normalización de mayúsculas/tildes (`CP-20`) y evalúa la latencia y estabilidad ante 100 peticiones concurrentes (`CP-22`).

2. **Casos Borde y Stress Leve (3 Casos):**
   * Evaluación de payloads extensos de +500k caracteres (`CP-12`), sanitización de caracteres especiales/emojis en UTF-8 (`CP-13`) y la evaluación de cómo reacciona la API ante entradas no técnicas o sin sentido (`CP-21`).

3. **Validación de Esquema y Tipos (1 Caso):**
   * Verificación de rechazo con HTTP 422 ante tipos de datos no válidos (`CP-14`), también se valida que la API rechace payloads nulos (`CP-23`) y detecte errores de sintaxis JSON (`CP-24`).

4. **Pruebas de Seguridad y Robustez (2 Casos):**
   * Inmunidad contra Inyección SQL en campos de entrada (`CP-15`) y rechazo de cabeceras no soportadas como XML (`CP-16`).

5. **Endpoints Complementarios (2 Casos):**
   * Diagnóstico de disponibilidad en `GET /health` (`CP-17`) y consulta del catálogo de 8 categorías en `GET /categorias` (`CP-18`).

6. **Integridad de Datos y Validaciones (6 Casos):**
   * Control de errores HTTP 422/405 ante campos vacíos (`CP-04`, `CP-05`, `CP-06`), JSON mal formado (`CP-07`), método HTTP no permitido (`CP-08`) y omisión de claves requeridas (`CP-19`).

---

## 🚀 4. Guía de Ejecución Paso a Paso

### Opción A: Ejecución Manual vía Swagger UI
1. Navegá a `http://localhost:8000/docs`.
2. Ubicá el endpoint `POST /predecir`.
3. Hacé clic en **Try it out**.
4. Ingresá un payload de prueba en el cuerpo de la petición. Por ejemplo:
   ```json
   {
     "titulo": "Introducción a Spring Boot",
     "texto": "En este contenido se presentan los conceptos básicos para la creación de APIs REST utilizando Java y Spring Boot."
   }

### Opción B: Ejecución Automatizada con Postman
1. Navegá a `http://localhost:8000/docs`.
2. Ubicá el endpoint `POST /predecir`.
3. Hacé clic en **Try it out**.
4. Ingresá un payload de prueba en el cuerpo de la petición. Por ejemplo:
   ```json
   {
     "titulo": "Introducción a Spring Boot",
     "texto": "En este contenido se presentan los conceptos básicos para la creación de APIs REST utilizando Java y Spring Boot."
   }

---

## 🔍 5. Assertions Implementadas en Postman (Scripts de Prueba)

Todas las peticiones principales incluyen scripts automáticos de validación escritos en JavaScript dentro de la pestaña Tests:

```
// Validación de código de respuesta HTTP 200
pm.test("Status code es 200 OK", function () {
    pm.response.to.have.status(200);
});

// Validación de tiempo de respuesta (Latencia < 2000 ms)
pm.test("Tiempo de respuesta menor a 2000ms", function () {
    pm.expect(pm.response.responseTime).to.be.below(2000);
});

// Validación de contrato y presencia de propiedades JSON
pm.test("Respuesta contiene el esquema correcto", function () {
    const responseJson = pm.response.json();
    pm.expect(responseJson).to.have.property("categoria");
    pm.expect(responseJson).to.have.property("probabilidad");
    pm.expect(responseJson).to.have.property("informaciones_adicionales");
});

// Validación del rango de probabilidad (0 a 1)
pm.test("La probabilidad es un número válido entre 0 y 1", function () {
    const responseJson = pm.response.json();
    pm.expect(responseJson.probabilidad).to.be.a('number');
    pm.expect(responseJson.probabilidad).to.be.within(0, 1);
});
```
---

## 6. Registro y Reporte de Evidencias

### Cada ejecución de pruebas se documenta siguiendo esta estructura:
- Capturas de pantalla: Guardadas en evidencias/capturas/ asociadas al ID del caso (ej. CP-01_Swagger_POST_predecir_HTTP200.png).
- Respuestas JSON: Almacenadas en evidencias/respuestas-json/.
- Reporte: Documentado en reportes/informes.
- Reporte Ejecutivo: Documentado en reportes/resultados-sprint-1.md.

_QA Testing Guide — TechMind Project v1.0 — Sprint 1_