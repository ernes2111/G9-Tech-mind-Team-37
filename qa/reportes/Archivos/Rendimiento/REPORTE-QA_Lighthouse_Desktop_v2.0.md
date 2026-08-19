# Informe de Auditoría Técnica y QA - Google Lighthouse (Escritorio) — Re-evaluación v2.4.0

**Proyecto / URL:** `http://147.15.127.238:5173/` (TechMind - Clasificación de contenido técnico)  
**Fecha de Ejecución:** 14 de agosto de 2026, 20:22hs (GMT-3)  
**Versión de la App:** `2.4.0`   
**Entorno de Prueba:** Emulated Desktop | Chrome 151.0.0.0 | Lighthouse 13.4.0  
**Rol:** Tester QA   
**Documento Adjunto:** [Descargar Nuevo Reporte Completo de Lighthouse Escritorio (PDF)](https://drive.google.com/file/d/1JG5DfL7kTJzXwJiAg1gE8kbzWes1Hktg/view?usp=sharing)  

---

## 1. Resumen Ejecutivo (Dashboard de Métricas & Comparativa)

Se ha realizado una nueva re-evaluación del entorno de escritorio tras la aplicación de las correcciones del **Sprint 5**. Se observa una **mejora sustancial** en el rendimiento global y la accesibilidad.

### 📊 Cuadro Comparativo (Evaluación Anterior vs. Re-evaluación v2.4.0)

| Categoría | Score Anterior (v1.6.0) | Nuevo Score (v2.4.0) | Delta / Evolución | Estado |
| :--- | :---: | :---: | :---: | :---: |
| **Performance (Rendimiento)** | 51 / 100 | **70 / 100** | 🟢 **+19 pts** | 🟡 Aceptable / En camino a la excelencia |
| **Accessibility (Accesibilidad)** | 87 / 100 | **95 / 100** | 🟢 **+8 pts** | 🟢 **Excelente** (Objetivo alcanzado) |
| **Best Practices (Buenas Prácticas)** | 74 / 100 | **74 / 100** | ➖ **0 pts** | ⚠️ Requiere TLS / HTTPS |
| **SEO** | 90 / 100 | **91 / 100** | 🟢 **+1 pt** | 🟢 **Excelente** |

---

## 2. Métricas Core Web Vitals y Rendimiento (Performance: 70/100)

El puntaje de rendimiento se incrementó de **51 a 70 puntos**, reduciendo drásticamente la latencia de carga inicial (FCP/LCP recortados a la mitad).

### 2.1 Desglose de Métricas Clave

* **First Contentful Paint (FCP):** `1.1 s` (Antes: `2.2 s` | Reducción del 50%) 🟢 **EXCELENTE**.
* **Largest Contentful Paint (LCP):** `1.1 s` (Antes: `2.3 s` | Reducción del 52.1%) 🟢 **EXCELENTE**.
* **Speed Index (SI):** `1.5 s` (Antes: `2.2 s` | Mejora del 31.8%) 🟢 **EXCELENTE**.
* **Total Blocking Time (TBT):** `20 ms` (Totalmente insignificante, casi cero bloqueo del hilo principal) 🟢 **EXCELENTE**.
* **Cumulative Layout Shift (CLS):** `1.144` (Antes: `1.516` | Se redujo un ~24.5%, pero sigue estando por encima del umbral óptimo de `0.1`) 🚨 **AÚN CRÍTICO**.

---

### 2.2 Diagnósticos e Insights de las Mejoras y Pendientes

1. **Optimizaciones Exitosas Aplicadas:**
   * **Reducción de Peticiones Bloqueantes (Render-blocking):** El ahorro estimado se redujo de `1,370 ms` a solo `450 ms`.
   * **Carga Diferida de Scripts (Defer):** `chart.js` fue movido al final del `<body>` con el atributo `defer` (`chart.umd.min.js`), eliminando la latencia de carga inicial.
   * **Optimización de Payload de Fuentes:** Se agregó el parámetro `subset=latin` en la llamada a Google Fonts, reduciendo la transferencia de tipografías de **1,210 KiB a 415 KiB** (Ahorro masivo del ~65% en peso de red).
   * **Inclusión de Fallbacks CSS:** Se implementaron reglas `@font-face` con `size-adjust`, `ascent-override` y `descent-override` para suavizar el FOUT.

2. **Causa Raíz del CLS Pendiente (`1.144`):**
   * El desplazamiento visual persistente proviene principalmente del renderizado asíncrono de las fuentes web externas (`.woff2` de Google Fonts aporta `0.978` al score de CLS).
   * **Solución Técnica Definitiva:** Alojar localmente las fuentes `Inter`, `Outfit` y `JetBrains Mono` en el servidor web (*self-hosting*) en lugar de consumirlas mediante CDN externa (`fonts.gstatic.com`).

3. **Consumo de Payload Global:**
   * **Peso total transferido:** Se redujo drásticamente de `1,668 KiB` (~1.67 MB) a **`819 KiB`** (~0.8 MB), cortando a la mitad el tráfico total del sitio.

---

## 3. Accesibilidad (Accessibility: 95/100)

Se ha alcanzado un nivel sobresaliente en accesibilidad, superando el umbral meta del proyecto (≥95).

### 3.1 Correcciones Verificadas

1. **Resolución de Nombres Accesibles en Botones:**
   * **Fix Confirmado:** Se agregó exitosamente el atributo `aria-label="Estado de servicios"` en `button#btn-status-trigger`, permitiendo que los lectores de pantalla reconozcan correctamente la función del control.
2. **Cumplimiento de Auditorías PASSED (16 comprobaciones aprobadas):**
   * Atributos ARIA válidos y coincidentes con sus roles.
   * [user-scalable="no"] no utilizado, garantizando zoom accesible en móviles.
   * Navegación por teclado e íconos interactivos optimizados.

3. **Detalles Menores Pendientes (Contraste):**
   * Persisten algunos pequeños textos/badges con contraste marginal en temas específicos (p. ej., `span.text-pink-700` y `button.btn-delete-entry`).

---

## 4. Buenas Prácticas (Best Practices: 74/100)

Se mantiene constante el puntaje debido a aspectos de infraestructura de servidor que no han sido modificados.

### 4.1 Brechas de Seguridad (Inalteradas)

1. **Ausencia de HTTPS:**
   * Se continúan sirviendo 6 solicitudes sobre HTTP inseguro (`http://147.15.127.238:5173`).
2. **Falta de Cabeceras de Seguridad HTTP:**
   * Ausencia de `Content-Security-Policy` (CSP en enforcement mode), `HSTS`, `COOP` y `X-Frame-Options`.

---

## 5. SEO (SEO: 91/100)

Subió a **91 / 100** tras la corrección de metadatos.

### 5.1 Corrección Verificada
* **Meta Description Añadida:** Se incorporó correctamente la etiqueta `<meta name="description" content="TechMind — Plataforma inteligente de clasificación y organización de contenido técnico...">` en la línea 9 del HTML.

### 5.2 Advertencia Detectada en `robots.txt`
* **Observación QA:** La auditoría marcó un fallo en la validación de `robots.txt` indicando *"robots.txt is not valid — 1,195 errors found"*. Esto ocurre porque el servidor está respondiendo el archivo `index.html` completo cuando el rastreador intenta consultar `/robots.txt` (comportamiento típico de una SPA sin fallback de archivo estático en el servidor web).

---

## 6. Plan de Acción y Siguientes Pasos (Roadmap a 100 pts)

1. **🔴 Prioridad Alta — Eliminar el CLS por Completo (Performance -> 95+):**
   * Descargar las fuentes tipográficas (`Inter`, `Outfit`, `JetBrains Mono`) e incluirlas localmente en la carpeta `/assets/fonts/`.
2. **🔴 Prioridad Alta — Configurar SSL/TLS (Best Practices -> 100):**
   * Habilitar HTTPS en el servidor web/proxy para cifrar el tráfico y aplicar cabeceras HSTS/CSP.
3. **🟡 Prioridad Media — Servir archivo `robots.txt` estático:**
   * Configurar el servidor para entregar un archivo `robots.txt` plano de texto en lugar del `index.html`.

---
*Informe generado por el equipo de Quality Assurance de TechMind.*
