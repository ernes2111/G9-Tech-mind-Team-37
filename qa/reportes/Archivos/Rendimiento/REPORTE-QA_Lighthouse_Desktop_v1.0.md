# Informe de Auditoría Técnica y QA - Google Lighthouse (Escritorio) — Evaluación v1.6.0

**Proyecto / URL:** `http://147.15.127.238:5173/` (Clasificación de contenido técnico)  
**Fecha de Ejecución:** 13 de agosto de 2026, 18:32hs (GMT-3)  
**Versión de la App:** `1.6.0`   
**Entorno de Prueba:** Emulated Desktop | Chrome 151.0.0.0 | Lighthouse 13.4.0  
**Rol:** Tester QA  

---

## 1. Resumen Ejecutivo (Dashboard de Métricas)

Se ha llevado a cabo un análisis exhaustivo del rendimiento, accesibilidad, buenas prácticas y SEO en la versión de escritorio de la aplicación de Clasificación de Contenido Técnico.

El reporte original exportado directamente desde Lighthouse se encuentra disponible para su descarga:  
👉 **[Ver / Descargar PDF de Lighthouse Desktop Original](https://drive.google.com/file/d/1hABBis34oLTwinbT57K0m6-Q1qVM08Z9/view?usp=sharing)**

| Categoría | Puntaje | Estado | Umbral Objetivo |
| :--- | :---: | :---: | :---: |
| **Performance (Rendimiento)** | **51 / 100** | ⚠️ Crítico / Requiere Optimización | ≥ 90 |
| **Accessibility (Accesibilidad)** | **87 / 100** | 🟡 Aceptable / Oportunidades de mejora | ≥ 95 |
| **Best Practices (Buenas Prácticas)** | **74 / 74** | ⚠️ Riesgo de Seguridad / Inseguro | 100 |
| **SEO** | **90 / 100** | 🟢 Bueno / Ajustes Menores | 100 |

---

## 2. Métricas Core Web Vitals y Rendimiento (Performance: 51/100)

El puntaje global de Rendimiento está gravemente penalizado principalmente por el **Cumulative Layout Shift (CLS)** y el tiempo de bloqueo en el hilo principal (*Render-blocking requests*).

### 2.1 Desglose de Métricas Clave

* **First Contentful Paint (FCP):** `2.2 s` (Aceptable, pero con margen de mejora)
* **Largest Contentful Paint (LCP):** `2.3 s` (Aceptable en escritorio, cercano al umbral de 2.5s)
* **Speed Index (SI):** `2.2 s`
* **Total Blocking Time (TBT):** `0 ms` (Excelente respuesta al hilo principal en la carga inicial)
* **Cumulative Layout Shift (CLS):** `1.516` 🚨 **CRÍTICO** (El umbral óptimo es `< 0.1`). La página sufre desplazamientos masivos e inestabilidad visual durante la renderización.

---

### 2.2 Diagnósticos e Insights de Performance

1. **Solicitudes que bloquean la renderización (Render-blocking requests):**
   * **Ahorro estimado:** `1,370 ms`
   * **Hallazgo:** Los scripts y hojas de estilo iniciales detienen el dibujado de la página.
   * **Recursos afectados:**
     * `http://147.15.127.238:5173/app.js?v=1.6.0` (93.2 KiB | 290 ms)
     * `cdn.tailwindcss.com/3.4.17` (127.2 KiB | 230 ms)
     * `cdn.jsdelivr.net/npm/chart.js` (70.5 KiB | 550 ms)
     * Google Fonts CSS (`fonts.googleapis.com`) (2.0 KiB | 340 ms)

2. **Carga y despliegue de tipografías (Font display):**
   * **Ahorro estimado:** `190 ms`
   * **Hallazgo:** Falta configurar `font-display: swap` o `optional` en la carga de fuentes web (`fonts.gstatic.com`), lo que causa texto invisible o cambios bruscos de fuente que alimentan el alto CLS.
   * **Archivos tipográficos pesados:** `...woff2` de Google Fonts alcanzando hasta `1,099.4 KiB` (1.1 MB solo en tipografía).

3. **Inestabilidad Visual (Causantes del CLS = 1.516):**
   * Fuentes cargadas de manera asíncrona sin espacio reservado (`.woff2` aportando 0.783 y 0.713 al score de layout shift).
   * Elementos dinámicos como `main#main-content`, `a#nav-classifier` y elementos con animaciones CSS no compuestas (`animate-pulse`, `shimmer`, `led-pulse`).

4. **Trabajo en Hilo Principal (Main-Thread Work):**
   * **Tiempo total consumido:** `2.5 s`
   * **Evaluación de scripts:** `843 ms`
   * **Estilos y Layout:** `615 ms`
   * **Extensión de navegador detectada con alto consumo:** `contentscript.js` / MetaMask (`nkbihfbeogaeaoehlefnkodbefgpgknn`) consumió más de `424 KiB` en transferencia y `133 ms` en hilo principal.

5. **Tamaño del Payload de Red:**
   * **Peso total transferido:** `1,668 KiB` (~1.67 MB).
   * **Distribución:**
     * Google Fonts CDN: `1,209.9 KiB` (72.5% del total del peso de la página).
     * JavaScript / Assets locales: `258.2 KiB`.
     * Tailwind CDN: `127.2 KiB`.

---

## 3. Accesibilidad (Accessibility: 87/100)

Aunque el puntaje es aceptable, existen fallos que impiden una experiencia adecuada para usuarios que utilizan tecnologías de asistencia (lectores de pantalla / navegación por teclado).

### 3.1 Deficiencias Detectadas

1. **Botones sin Nombre Accesible (Names and Labels):**
   * **Elemento:** `button#btn-status-trigger.sidebar-nav-item...`
   * **Impacto:** Los lectores de pantalla solo anuncian "botón", omitiendo su función o propósito.

2. **Relación de Contraste Insuficiente (Color Contrast):**
   * Múltiples elementos de texto y badges no cumplen con las proporciones mínimas de contraste según WCAG 2.1 AA.
   * **Elementos afectados:**
     * Badges de estado: `span.text-sky-700.dark:text-sky-400...`
     * Tarjetas de historial: `p.history-card-body.text-on-surface-variant...opacity-80`
     * Botones de eliminación: `button.btn-delete-entry.bg-rose-500/15...`

3. **Verificaciones Manuales Pendientes:**
   * Verificar que la secuencia de tabulación (`tabindex`) siga un orden visual lógico.
   * Asegurar que los paneles contextuales (popovers como `#admin-user-popover` o `#status-popover`) atrapen o dirijan el foco del usuario correctamente al abrirse.

---

## 4. Buenas Prácticas (Best Practices: 74/100)

Se identificaron vulnerabilidades críticas de seguridad en la capa de red y en la configuración del servidor web.

### 4.1 Brechas de Seguridad Críticas (Trust & Safety)

1. **Ausencia de HTTPS (6 solicitudes Inseguras):**
   * La aplicación se está sirviendo mediante HTTP no cifrado (`http://147.15.127.238:5173`).
   * No existe redirección de tráfico HTTP a HTTPS.
   * **Riesgo:** Exposición de datos en tránsito, susceptibilidad a ataques Man-in-the-Middle (MitM) y bloqueo de APIs modernas del navegador.

2. **Falta de Cabeceras de Seguridad (Security Headers):**
   * **Content Security Policy (CSP):** No configurado o ausente en modo *enforcement*. Genera alta vulnerabilidad a ataques XSS (Cross-Site Scripting).
   * **HSTS (HTTP Strict Transport Security):** Sin cabecera.
   * **COOP (Cross-Origin-Opener-Policy):** Sin cabecera.
   * **X-Frame-Options / frame-ancestors:** Sin cabecera (vulnerable a Clickjacking).
   * **Trusted Types:** No requeridos.

3. **Errores en Consola y Mapeo de Código:**
   * Error al obtener Source Map: `Failed fetching source map (404)` para `/npm/chart.umd.min.js.map` en JSDelivr CDN.

---

## 5. SEO (Search Engine Optimization: 90/100)

El sitio presenta una base sólida para indexación, pero requiere un ajuste esencial de metadata.

### 5.1 Oportunidad de Mejora
* **Falta de Meta Description:** El documento HTML no posee la etiqueta `<meta name="description" content="...">`.
* **Impacto:** Los motores de búsqueda no pueden mostrar un resumen optimizado en los resultados de búsqueda (SERP).

### 5.2 Auditorías Aprobadas
* Documento posee etiqueta `<title>`.
* Códigos de respuesta HTTP exitosos (200 OK).
* Enlaces rastreables con texto descriptivo.
* Etiqueta `<html>` posee atributo `lang` válido.

---

## 6. Plan de Acción y Recomendaciones QA (Matriz de Priorización)

Para elevar la calificación de Lighthouse por encima de 90 en todas las categorías, se sugiere ejecutar los siguientes tickets de desarrollo:

### 🔴 Prioridad Alta (Bloqueante / Seguridad y Performance)

1. **Corregir Layout Shift (CLS):**
   * Añadir dimensiones explícitas o reservadas (`min-height`, `aspect-ratio`) en el CSS para el contenedor `main#main-content` y la barra lateral (`#sidebar`).
   * Aplicar `font-display: swap;` en las fuentes e incluir un *font fallback* con métricas ajustadas.
2. **Implementar HTTPS y TLS:**
   * Configurar un certificado SSL/TLS (p. ej., Let's Encrypt) en el servidor/reverse proxy y forzar la redirección HTTP -> HTTPS.
3. **Depurar e Incrustar Tipografías:**
   * Evitar descargar paquetes completos de WOFF2 (`>1MB`). Subconjuntar (*subsetting*) las fuentes para incluir únicamente los caracteres requeridos (Latin base) o servir localmente las variantes necesarias.

### 🟡 Prioridad Media (Accesibilidad y Buenas Prácticas)

4. **Configurar Cabeceras de Seguridad:**
   * Agregar cabeceras HTTP en el servidor web (Nginx/Apache/Caddy): `Content-Security-Policy`, `Strict-Transport-Security`, `X-Frame-Options: DENY`, `X-Content-Type-Options: nosniff`.
5. **Optimizar Scripts de Terceros:**
   * Utilizar bundles optimizados localmente en lugar de cargar Tailwind completo vía CDN (`cdn.tailwindcss.com`) en producción. Se recomienda compilar CSS con Tailwind CLI / Vite.
   * Cargar scripts de analítica/gráficos (`chart.js`) con atributos `defer` o `async`.
6. **Añadir Labels y Ajustar Contraste:**
   * Agregar `aria-label="Estado de conexión"` en `button#btn-status-trigger`.
   * Incrementar la opacidad y oscuridad de los textos con clases `text-sky-700`, `text-on-surface-variant` para superar la relación 4.5:1.

### 🟢 Prioridad Baja (SEO y Mantenimiento)

7. **Añadir Meta Description:**
   * Incluir `<meta name="description" content="Plataforma de clasificación y análisis de contenido técnico.">` en el `<head>`.
8. **Corregir Source Maps:**
   * Vincular correctamente los archivos `.map` para librerías CDN o deshabilitar la advertencia en producción.

---
*Informe generado por el equipo de Quality Assurance de TechMind.*
