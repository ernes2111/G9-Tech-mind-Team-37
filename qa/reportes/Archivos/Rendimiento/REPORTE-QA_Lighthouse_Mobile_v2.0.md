# Informe de Auditoría Técnica y QA - Google Lighthouse (Mobile) — Re-evaluación v2.4.0

**Proyecto / URL:** `http://147.15.127.238:5173/` (TechMind - Clasificación de contenido técnico)  
**Fecha de Ejecución:** 14 de agosto de 2026, 20:24hs (GMT-3)  
**Versión de la App:** `2.4.0`  
**Entorno de Prueba:** Emulated Moto G Power | Slow 4G Throttling | Chrome 151.0.0.0 | Lighthouse 13.4.0  
**Rol:** Tester QA   
**Documento Adjunto:** [Descargar Nuevo Reporte Completo de Lighthouse Mobile (PDF)](https://drive.google.com/file/d/1ONBKcit5ZvSoSF2PND6vIHDWaDPEZWwy/view?usp=sharing)  

---

## 1. Resumen Ejecutivo (Dashboard de Métricas & Comparativa Mobile)

Se ha realizado una nueva re-evaluación en el entorno **Mobile (Moto G Power / Red Slow 4G)** tras la implementación de las optimizaciones del **Sprint 5**. Se registra un **progreso significativo en el rendimiento**, acelerando la carga inicial casi al doble, y logrando una calificación excelente en accesibilidad y SEO.

### 📊 Cuadro Comparativo (Evaluación Mobile Anterior vs. Re-evaluación v2.4.0)

| Categoría | Score Anterior (v1.6.0) | Nuevo Score (v2.4.0) | Delta / Evolución | Estado |
| :--- | :---: | :---: | :---: | :---: |
| **Performance (Rendimiento)** | 56 / 100 | **66 / 100** | 🟢 **+10 pts** | 🟡 Avance notable en redes 4G |
| **Accessibility (Accesibilidad)** | 87 / 100 | **95 / 100** | 🟢 **+8 pts** | 🟢 **Excelente** (Objetivo alcanzado) |
| **Best Practices (Buenas Prácticas)** | 74 / 100 | **74 / 100** | ➖ **0 pts** | ⚠️ Requiere TLS / HTTPS |
| **SEO** | 90 / 100 | **91 / 100** | 🟢 **+1 pt** | 🟢 **Excelente** |

---

## 2. Métricas Core Web Vitals y Rendimiento Mobile (Performance: 66/100)

El puntaje de rendimiento en dispositivos móviles saltó de **56 a 66 puntos**, reduciendo drásticamente la espera del usuario en conexiones móviles 4G.

### 2.1 Desglose de Métricas Clave

* **First Contentful Paint (FCP):** `5.5 s` (Antes: `9.9 s` | Reducción del **44.4%** en tiempo de render) 🟢 **GRAN MEJORA**.
* **Largest Contentful Paint (LCP):** `5.5 s` (Antes: `10.9 s` | Reducción del **49.5%** en despliegue visual) 🟢 **GRAN MEJORA**.
* **Speed Index (SI):** `5.5 s` (Antes: `9.9 s` | Mejora del **44.4%**) 🟢 **MEJORA SIGNIFICATIVA**.
* **Total Blocking Time (TBT):** `0 ms` (Cero congelamiento del hilo principal en el procesador móvil) 🟢 **IMPECABLE**.
* **Cumulative Layout Shift (CLS):** `0` (Mantiene cero inestabilidad visual en mobile) 🟢 **PERFECTO**.

---

### 2.2 Diagnósticos e Insights de las Mejoras y Pendientes

1. **Optimizaciones Exitosas Aplicadas:**
   * **Optimización de Solicitudes Bloqueantes (Render-blocking):** El tiempo desperdiciado en peticiones iniciales se redujo de `7,540 ms` a **`3,200 ms`** (Ahorro de más de 4.3 segundos en 4G).
   * **Carga Asíncrona / Defer:** `chart.js` diferido al pie del documento redujo el tiempo de procesamiento en el hilo principal móvil de **10.5 s a 9.2 s**.
   * **Optimización del Payload de Fuentes:** Reducción de la descarga de Google Fonts a **414 KiB** (ahorrando ~800 KB de transferencia móvil).

2. **Oportunidad de Mejora Pendiente en Móviles:**
   * **Carga de Tailwind vía CDN:** `cdn.tailwindcss.com` aún genera una demora de ~780ms en redes móviles.
   * **Recomendación QA:** Compilar las clases CSS usadas mediante Tailwind CLI local/Vite para entregarlas como un único archivo estático minificado (`< 20 KB`).

---

## 3. Accesibilidad Mobile (Accessibility: 95/100)

Excelente puntuación adaptada para dispositivos con tecnología de asistencia y pantallas táctiles.

### 3.1 Correcciones Verificadas
* **Atributo ARIA en Botón de Estado:** El añadido de `aria-label="Estado de servicios"` en `button#btn-status-trigger` corrigió la advertencia de botones sin nombre accesible.
* **Touch Targets Aprobados:** Se confirmó que todos los botones e íconos interactivos cumplen con las dimensiones mínimas para interacción táctil en pantallas de móviles.

---

## 4. Buenas Prácticas y Seguridad (Best Practices: 74/100)

* **Riesgo Inseguro Persistente:** Servido sin cifrado SSL/TLS (`http://147.15.127.238:5173`) y sin cabeceras `Content-Security-Policy` (CSP) o `HSTS`.

---

## 5. SEO Mobile (SEO: 91/100)

* **Meta Description Agregada:** Tag `<meta name="description">` correctamente insertado para motores de búsqueda.
* **Observación de Servidor:** Se detectó la respuesta de `index.html` al consultar `/robots.txt`, lo cual debe ajustarse sirviendo un archivo de texto plano.

---

## 6. Comparativa QA: v1.6.0 vs v2.4.0 (Entorno Mobile 4G)

| Métrica | Version Anterior (v1.6.0) | Nueva Versión (v2.4.0) | Impacto Real en Usuario Móvil |
| :--- | :---: | :---: | :--- |
| **Score Performance** | 56 / 100 | **66 / 100** | 🚀 +10 puntos de rendimiento. |
| **FCP (Primer Pintado)** | 9.9 s | **5.5 s** | ⏱️ **4.4 segundos más rápido** para ver contenido. |
| **LCP (Carga Principal)** | 10.9 s | **5.5 s** | ⏱️ **5.4 segundos más rápido** para interactuar. |
| **CLS (Saltos de Pantalla)** | 0 | **0** | 🟢 Cero desplazamientos molestos. |
| **Peso Total Cargado** | 1,669 KiB | **817 KiB** | 📉 **Ahorro del 51% de datos móviles**. |

---
*Informe generado por el equipo de Quality Assurance de TechMind.*
