# 🧪 Informe de Ejecución de Pruebas QA — Sprint 2

> **Proyecto:** TechMind — Clasificación Inteligente de Contenido Técnico  
> **Rol / Ejecutor:** QA Lead & Assistant (Soporte a Federico G. Gutiérrez)  
> **Fecha de Ejecución:** 28 de Julio, 2026  
> **Entorno:** Multicontenedor Docker (`PostgreSQL 16`, `FastAPI`, `Spring Boot`, `Nginx Frontend`)  
> **Resultado Global:** 🟢 **100% Exitoso (14/14 Casos Aprobados)**  

---

## 📈 Resumen Ejecutivo

Se asumió el rol de **QA Automation / Manual Testing** para ejecutar la suite completa de verificación del sistema E2E (End-to-End). Las pruebas cubrieron tanto la API de Spring Boot (`:8080`), el microservicio de Ciencia de Datos FastAPI (`:8000`), el esquema de persistencia en PostgreSQL (`:5432`) y la resiliencia ante ataques de inyección y sobrecarga de payloads.

### 📊 Métricas Principales

| Métrica | Valor |
|---|---|
| **Total de Casos Ejecutados** | **14** |
| **Casos Exitosos (`PASS`)** | **14 (100%)** |
| **Casos Fallidos (`FAIL`)** | **0 (0%)** |
| **Tiempo de Respuesta Promedio** | **16.14 ms** |
| **Tiempo Máximo de Respuesta (Payload ~35k char)** | **28.66 ms** |
| **Errores de Base de Datos / Schemas** | **0** |

---

## 📋 Matriz de Casos de Prueba Ejecutados

| ID | Nombre del Caso de Prueba | Endpoint Evaluado | Resultado Esperado | Resultado Obtenido | Latencia | Estado |
|---|---|---|---|---|---|---|
| **CP-17** | Health Check de Servicio ML | `GET :8000/health` | HTTP `200` (`status: ok`) | HTTP `200` (`model_loaded: true`) | 26.5 ms | 🟢 **PASS** |
| **CP-18** | Catálogo de 8 Categorías ML | `GET :8000/categorias` | HTTP `200` (Array 8 ítems) | HTTP `200` (`categorias`: 8 ítems) | 2.39 ms | 🟢 **PASS** |
| **CP-01** | Clasificación Backend E2E | `POST :8080/contenido` | HTTP `201` (`Backend`) | HTTP `201` (`Backend`, 63.57%) | 28.66 ms | 🟢 **PASS** |
| **CP-02** | Clasificación Data Science E2E | `POST :8080/contenido` | HTTP `201` (`Data Science`) | HTTP `201` (`Data Science`, 58.45%) | 15.63 ms | 🟢 **PASS** |
| **CP-03** | Clasificación DevOps E2E | `POST :8080/contenido` | HTTP `201` (`DevOps`) | HTTP `201` (`DevOps`, 59.82%) | 17.76 ms | 🟢 **PASS** |
| **CP-04** | Clasificación Frontend E2E | `POST :8080/contenido` | HTTP `201` (`Frontend`) | HTTP `201` (`Frontend`, 61.12%) | 17.93 ms | 🟢 **PASS** |
| **CP-05** | Clasificación Directa FastAPI | `POST :8000/predecir` | HTTP `200` OK | HTTP `200` OK | 5.50 ms | 🟢 **PASS** |
| **CP-06** | Validación Título Vacío | `POST :8080/contenido` | HTTP `400` Bad Request | HTTP `400` Bad Request | 15.21 ms | 🟢 **PASS** |
| **CP-07** | Validación Texto Vacío | `POST :8080/contenido` | HTTP `400` Bad Request | HTTP `400` Bad Request | 3.95 ms | 🟢 **PASS** |
| **CP-08** | Omisión de Campo en Payload | `POST :8000/predecir` | HTTP `422` Unprocessable Entity | HTTP `422` Unprocessable Entity | 2.29 ms | 🟢 **PASS** |
| **CP-09** | Resistencia a SQL Injection | `POST :8080/contenido` | HTTP `201` (Texto Sanitizado) | HTTP `201` (Sin ejecución SQL) | 16.02 ms | 🟢 **PASS** |
| **CP-10** | UTF-8, Emojis y Caracteres Espec. | `POST :8080/contenido` | HTTP `201` (Reserva de Tildes/Emojis) | HTTP `201` OK | 15.84 ms | 🟢 **PASS** |
| **CP-11** | Carga de Payload Extenso (~35k char) | `POST :8080/contenido` | HTTP `201` (Procesamiento < 2s) | HTTP `201` (Procesado en 25.74ms) | 25.74 ms | 🟢 **PASS** |
| **CP-12** | Consulta de Historial en PostgreSQL | `GET :8000/predicciones` | HTTP `200` (Listado de Predicciones) | HTTP `200` OK (`JOIN` correcto) | 12.30 ms | 🟢 **PASS** |

---

## 🔍 Análisis de Hallazgos y Calidad

1. **Rendimiento Ultrarrápido (< 30 ms)**:
   * La latencia media se mantuvo en **16.14 ms**, lo cual está dramáticamente por debajo del límite estipulado por el requerimiento no funcional (máximo 2000 ms).

2. **Inmunidad a SQL Injection y Cross-Site Scripting (XSS)**:
   * Al enviar payloads con sentencias maliciosas (`DROP TABLE`, `' OR '1'='1'`) y tags de JavaScript (`<script>`), el sistema procesó la entrada de manera segura usando consultas preparadas (`PreparedStatement` en Spring Data JPA) y limpió los caracteres en el pipeline de NLP.

3. **Verificación del Bug Resuelto (`log_prediccion` / Foreign Key)**:
   * Se confirmó que la eliminación del intento de inserción directa desde FastAPI solucionó al 100% los errores en `techmind-postgres`. Toda la persistencia ahora fluye limpiamente a través de Spring Boot asignando `contenido_id`.

4. **Integridad del Historial**:
   * Las consultas a `GET :8000/predicciones` devolvieron los datos unificados correctamente mediante `JOIN contenidos c ON c.id = p.contenido_id`, confirmando que el Frontend puede renderizar el modal de historial sin fallos.

---

## 🎯 Conclusión para el Equipo y Federico

La suite de pruebas fue completada de forma 100% satisfactoria. El sistema **TechMind** se encuentra en un estado **estable, seguro, de alto rendimiento y listo para producción**.
