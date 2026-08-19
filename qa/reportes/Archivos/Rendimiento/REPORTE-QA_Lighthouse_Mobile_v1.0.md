# Informe de Auditoría Técnica y QA - Google Lighthouse (Mobile) — Evaluación v1.6.0

**Proyecto / URL:** `http://147.15.127.238:5173/` (Clasificación de contenido técnico)  
**Fecha de Ejecución:** 13 de agosto de 2026, 18:47hs (GMT-3)  
**Versión de la App:** `1.6.0`   
**Entorno de Prueba:** Emulated Moto G Power | Slow 4G Throttling | Chrome 151.0.0.0 | Lighthouse 13.4.0  
**Rol:** Tester QA  

---

## 1. Resumen Ejecutivo (Dashboard de Métricas Mobile)

Se ha llevado a cabo un análisis detallado del rendimiento, accesibilidad, buenas prácticas y SEO en la versión **Mobile (Dispositivos Móviles)** simulando una red **Slow 4G** y una CPU gama media/baja (*Moto G Power*).

El reporte original exportado directamente desde Lighthouse se encuentra disponible para su descarga:  
👉 **[Ver / Descargar PDF de Lighthouse Mobile Original](https://drive.google.com/file/d/1e_xcBMoTtd0rkCGdtV3kbzkdpGTfC-0z/view?usp=sharing)**

| Categoría | Puntaje Mobile | Puntaje Desktop (Ref.) | Estado | Umbral Objetivo |
| :--- | :---: | :---: | :---: | :---: |
| **Performance (Rendimiento)** | **56 / 100** | 51 / 100 | ⚠️ Crítico (Tiempos de carga altos) | ≥ 90 |
| **Accessibility (Accesibilidad)** | **87 / 100** | 87 / 100 | 🟡 Aceptable / Ajustes de Contraste | ≥ 95 |
| **Best Practices (Buenas Prácticas)** | **74 / 100** | 74 / 100 | ⚠️ Riesgo de Seguridad / Sin HTTPS | 100 |
| **SEO** | **90 / 100** | 90 / 100 | 🟢 Bueno / Falta Meta Description | 100 |

---

## 2. Métricas Core Web Vitals y Rendimiento Mobile (Performance: 56/100)

Aunque el puntaje global de Rendimiento subió levemente a **56** (debido a un **CLS perfecto de 0** en esta emulación), la experiencia de usuario real en dispositivos móviles bajo redes 4G es **extremadamente lenta y deficiente**.

### 2.1 Desglose de Métricas Clave

* **First Contentful Paint (FCP):** `9.9 s` 🚨 **CRÍTICO** (El usuario espera casi 10 segundos para ver el primer elemento de pantalla).
* **Largest Contentful Paint (LCP):** `10.9 s` 🚨 **CRÍTICO** (El contenido principal tarda cerca de 11 segundos en cargarse).
* **Speed Index (SI):** `9.9 s` 🚨 **CRÍTICO**.
* **Total Blocking Time (TBT):** `0 ms` (Excelente respuesta de interacción una vez cargado).
* **Cumulative Layout Shift (CLS):** `0` 🟢 **EXCELENTE** (No se observaron desplazamientos inestables de interfaz en la resolución mobile).

---

### 2.2 Diagnósticos e Insights de Performance Mobile

1. **Peticiones que Bloquean el Renderizado (Render-blocking requests):**
   * **Ahorro estimado enorme:** `7,540 ms` (~7.5 segundos desperdiciados).
   * **Análisis:** En redes móviles de 4G, el impacto de no diferir scripts/estilos se amplifica dramáticamente.
   * **Principales culpables por latencia de transferencia:**
     * `http://147.15.127.238:5173/app.js?v=1.6.0` (93.2 KiB | **2,190 ms**)
     * `cdn.jsdelivr.net/npm/chart.js` (70.9 KiB | **3,040 ms**)
     * `fonts.googleapis.com` (2.0 KiB | **1,000 ms**)
     * `cdn.tailwindcss.com` (127.2 KiB | **780 ms**)

2. **Procesamiento de JavaScript y Trabajo en Hilo Principal (Main-Thread Work):**
   * **Tiempo total de trabajo en Hilo Principal:** `10.5 s` (en procesador móvil Moto G Power).
   * **Tiempo de Ejecución de JS (Execution Time):** `4.1 s`.
   * **Evaluación de Scripts:** `3,526 ms`.
   * **Cálculo de Estilos y Layout:** `2,945 ms`.

3. **Carga y Despliegue de Fuentes (Font display):**
   * **Ahorro estimado:** `210 ms`.
   * **Peso en red:** Las tipografías de Google Fonts (`.woff2`) suman **1,210.3 KiB** (~1.2 MB), representando el **72.5% del total consumido** en datos móviles.

4. **Payload de Red en Móviles:**
   * **Total descargado:** `1,669 KiB` (~1.67 MB).
   * **Diagnóstico QA:** Cargar 1.7 MB en una conexión móvil 4G limita severamente la conversión y la retención de usuarios.

---

## 3. Accesibilidad (Accessibility: 87/100)

Mantiene los mismos hallazgos que la versión de escritorio, con un impacto mayor en dispositivos táctiles de pantallas pequeñas.

### 3.1 Deficiencias Detectadas

1. **Botones sin Nombre Accesible (Names and Labels):**
   * **Elemento:** `button#btn-status-trigger.sidebar-nav-item...`
   * **Impacto:** Lectores de pantalla en móviles (TalkBack / VoiceOver) no pueden anunciar la función del botón.

2. **Falta de Contraste de Color (WCAG 2.1 AA):**
   * Varios badges y textos en tarjetas de historial presentan bajo contraste visual, afectando la legibilidad bajo la luz solar directa en pantallas móviles:
     * `span.text-sky-700.dark:text-sky-400...`
     * `p.history-card-body.text-on-surface-variant...opacity-80`
     * `button.btn-delete-entry.bg-rose-500/15...`

3. **Auditorías Aprobadas en Mobile:**
   * ✅ Los objetivos de toque (*Touch targets*) poseen tamaño y espaciado adecuado.
   * ✅ La etiqueta `<meta name="viewport">` permite la amplificación/zoom adecuada del usuario (`user-scalable` habilitado).

---

## 4. Buenas Prácticas (Best Practices: 74/100)

Se replican las vulnerabilidades encontradas en la versión desktop.

### 4.1 Brechas de Seguridad y Red

1. **Uso de HTTP Inseguro (6 solicitudes Inseguras):**
   * Servido sobre `http://147.15.127.238:5173` sin cifrado SSL/TLS ni redirección forzada a HTTPS.
2. **Ausencia de Cabeceras de Seguridad:**
   * Sin `Content Security Policy (CSP)`, `HSTS`, `COOP`, ni `X-Frame-Options`.
3. **Mapeo de Código Fallido:**
   * Error 404 al intentar obtener Source Map de `chart.umd.min.js.map`.

---

## 5. SEO (Search Engine Optimization: 90/100)

### 5.1 Oportunidad de Mejora
* **Falta de Meta Description:** Mantenemos la observación de agregar la etiqueta `<meta name="description" content="...">` para mejorar la presencia en buscadores móviles.

### 5.2 Puntos Fuertes
* Diseño responsivo adaptado correctamente al Viewport móvil.
* Estructura jerárquica de encabezados correcta (`<h1>`-`<h3>`).

---

## 6. Comparativa QA: Escritorio vs. Mobile

| Métrica / Aspecto | Desktop | Mobile (4G) | Impacto / Conclusión QA |
| :--- | :---: | :---: | :--- |
| **Score Performance** | 51 | **56** | Ligera mejora por CLS=0 en mobile. |
| **FCP (First Contentful Paint)** | 2.2 s | **9.9 s** | 🚨 **+350% más lento** en red móvil. |
| **LCP (Largest Contentful Paint)** | 2.3 s | **10.9 s** | 🚨 **Inaceptable para producción móvil**. |
| **CLS (Inestabilidad Visual)** | 1.516 | **0** | ✅ Mobile no presenta saltos visuales. |
| **Trabajo en Hilo Principal** | 2.5 s | **10.5 s** | 🚨 La CPU móvil se satura procesando JS/CSS. |

---

## 7. Plan de Acción y Priorización Técnica QA (Mobile First)

1. **🔴 URGENTE - Bundle Optimization & Lazy Loading:**
   * Reemplazar Tailwind CDN (`cdn.tailwindcss.com`) por CSS compilado y purgado en build time. Esto ahorrará más de 7 segundos en FCP/LCP mobile.
   * Servir Google Fonts localmente utilizando únicamente la subserie de caracteres requeridos (*font-subsetting*).
2. **🔴 URGENTE - Implementación de HTTPS:**
   * Configurar certificado SSL en servidor web.
3. **🟡 MEDIA - Diferir JavaScript No Esencial:**
   * Aplicar `defer` o `async` al script de `chart.js` para evitar bloquear el pintado inicial de la interfaz mobile.
4. **🟢 BAJA - Accesibilidad y Metadata:**
   * Agregar `aria-label` a botones de la barra lateral y agregar la etiqueta `<meta name="description">`.

---
*Informe generado por el equipo de Quality Assurance de TechMind.*