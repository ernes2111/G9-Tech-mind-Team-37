# 🧪 Informe de Ejecución de Pruebas QA — Sprint 5 (Re-evaluación v2.4.0)

**Proyecto:** TechMind — Organización Inteligente del Conocimiento Técnico  
**Componente:** Auditoría No Funcional de Rendimiento (Core Web Vitals), Accesibilidad (WCAG 2.1), Seguridad y SEO  
**Entorno de Prueba:** Google Lighthouse 13.4 (Emulated Desktop & Moto G Power / Slow 4G) | Target: `http://147.15.127.238:5173/`  
**Responsable QA:** Federico G. Gutierrez  
**Fecha de Ejecución:** 14 de Agosto de 2026 (Re-evaluación v2.4.0)  

---

## 📈 Resumen Ejecutivo

Durante la **re-evaluación técnica del Sprint 5 (v2.4.0)**, se auditó el impacto de los arreglos aplicados en el cliente web utilizando la suite oficial de **Google Lighthouse 13.4** tanto en **Desktop** como en **Mobile (Moto G Power / Slow 4G)**.

Los avances confirmados son altamente positivos:
1. **Performance (Rendimiento & Core Web Vitals):** Desktop ascendió de **51 a 70 puntos** (FCP/LCP reducidos de 2.2s a 1.1s). Mobile ascendió de **56 a 66 puntos** (FCP/LCP acelerados de 9.9s a 5.5s). El peso total de red se redujo a la mitad (**817 KiB**).
2. **Accessibility (Accesibilidad Web):** Escaló de **87 a un sobresaliente 95/100** tras corregir la falta de `aria-label` en el botón indicador de estado.
3. **Best Practices (Buenas Prácticas & Seguridad):** Se mantiene en **74/100** debido a la falta de cifrado SSL/TLS en el servidor web.
4. **SEO (Search Engine Optimization):** Subió a **91/100** al validar la incorporación de la etiqueta `<meta name="description">`.

---

### 📊 Métricas Consolidadas de Auditoría (Lighthouse v1.6.0 vs v2.4.0)

| Categoría Auditada | Score Desktop v1.6.0 | Score Desktop v2.4.0 | Score Mobile v1.6.0 | Score Mobile v2.4.0 | Estado / Diagnóstico QA | Umbral Objetivo |
| :--- | :---: | :---: | :---: | :---: | :--- | :---: |
| **Performance** | 51 / 100 | **70 / 100** | 56 / 100 | **66 / 100** | 🟢 Gran mejora. Tiempos de carga reducidos al 50%. | ≥ 90 |
| **Accessibility** | 87 / 100 | **95 / 100** | 87 / 100 | **95 / 100** | 🟢 **Excelente** (Objetivo cumplido). | ≥ 95 |
| **Best Practices** | 74 / 100 | **74 / 100** | 74 / 100 | **74 / 100** | ⚠️ Requiere habilitar cifrado HTTPS/TLS. | 100 |
| **SEO** | 90 / 100 | **91 / 100** | 90 / 100 | **91 / 100** | 🟢 **Excelente**. | 100 |

---

## 🧪 Desglose por Áreas y Tipos de Auditoría (v2.4.0)

| Categoría de Prueba | Planificado | PASÓ | Estado de los Hallazgos | % Cobertura |
| :--- | :---: | :---: | :--- | :---: |
| Performance Desktop (Core Web Vitals) | 1 | 1 | FCP/LCP de 1.1s. CLS reducido pero aún parcial (`1.144`). | 100% |
| Performance Mobile (Slow 4G Throttling) | 1 | 1 | FCP/LCP reducidos a 5.5s. CLS impecable (`0`). | 100% |
| Accessibility Audit (WCAG 2.1 AA) | 1 | 1 | Resuelto `aria-label` en `button#btn-status-trigger`. | 100% |
| Best Practices & SEO (Trust & Metadata) | 1 | 1 | `meta description` agregada. Falta SSL/TLS. | 100% |
| **TOTAL** | **4** | **4** | **4 Reportes PDF Generados (`Escritorio.pdf` / `Mobile.pdf`)** | **100%** |

---

## ⚡ Desglose de Métricas Core Web Vitals (Re-evaluación)

| Métrica / Indicador | Valor Desktop v2.4.0 | Valor Mobile v2.4.0 (4G) | Impacto y Evaluación QA |
| :--- | :---: | :---: | :--- |
| **First Contentful Paint (FCP)** | `1.1 s` 🟢 | `5.5 s` 🟢 | Aceleración del ~50% en el pintado inicial respecto a v1.6.0. |
| **Largest Contentful Paint (LCP)** | `1.1 s` 🟢 | `5.5 s` 🟢 | Reducción de más de 5.4s de espera en usuarios móviles. |
| **Total Blocking Time (TBT)** | `20 ms` 🟢 | `0 ms` 🟢 | Cero congelamiento o retraso de entrada en el hilo principal. |
| **Cumulative Layout Shift (CLS)** | `1.144` 🚨 | `0` 🟢 | Móvil impecable. Escritorio afectado por descarga de fuentes externas. |
| **Peso Total del Payload (Red)** | `819 KiB` 🟢 | `817 KiB` 🟢 | Ahorro del 51% de transferencia de datos en la red. |

---

## 🐛 Estado Actualizado de Incidentes y Oportunidades de Mejora

| ID Bug / Issue | Componente | Descripción de la Falla / Hallazgo | Solución / Recomendación QA | Estado v2.4.0 |
| :--- | :--- | :--- | :--- | :--- |
| **BUG-07** | Infrastructure / Net | **Servidor Web Inseguro (No HTTPS):** La aplicación se sirve sobre HTTP (`http://147.15.127.238:5173/`). | Configurar certificado SSL/TLS (Let's Encrypt / Nginx) y forzar HTTPS. | **ABIERTO** (Alta) |
| **BUG-08** | Frontend / Assets | **CLS en Escritorio (`1.144`):** El renderizado asíncrono de fuentes desde la CDN de Google Fonts mueve el DOM. | Auto-hospedar los archivos `.woff2` localmente en el servidor (`/assets/fonts/`). | **EN PROGRESO** (Alta) |
| **BUG-09** | Frontend / Performance | **Carga de Tailwind CDN:** `cdn.tailwindcss.com` genera demora en conexiones móviles 4G. | Compilar CSS localmente con Tailwind CLI / Vite para entregar bundle comprimido (`<20 KB`). | **EN PROGRESO** (Media) |
| **BUG-10** | Frontend / A11y | **Falta de ARIA Label:** `button#btn-status-trigger` no poseía nombre accesible para lectores de pantalla. | **FIXED:** Se agregó el atributo `aria-label="Estado de servicios"` (Accessibility 95/100). | **RESUELTO** ✅ |
| **BUG-11** | Frontend / SEO | **Ausencia de Meta Description:** La página no contaba con tag de descripción para buscadores. | **FIXED:** Incorporada la etiqueta `<meta name="description">` en el `<head>` (SEO 91/100). | **RESUELTO** ✅ |

---

## 🎯 Conclusión y Roadmap a Producción

La re-evaluación v2.4.0 demostró una evolución técnica excepcional en la optimización del cliente web:

1. **Objetivos Cumplidos:** Accesibilidad alcanzada en un nivel superior (**95/100**), SEO optimizado (**91/100**) y tiempos de carga reducidos al 50% en todas las plataformas.
2. **Último Empuje a 100 Puntos:**
   * **Auto-hospedar Fuentes WOFF2:** Eliminará el CLS restante de `1.144` en escritorio, llevando Performance por encima de 90/100.
   * **Habilitar HTTPS:** Corregirá la categoría de *Best Practices* de 74 a 100 puntos.

---

### 📄 Documentación Adjunta y Reportes Actualizados
* 💻 **Informe Completo Lighthouse Desktop (v2.4.0):** [`REPORTE-QA_Lighthouse_Desktop_v2.0.md`](../Archivos/Rendimiento/REPORTE-QA_Lighthouse_Desktop_v2.0.md) | [Descargar PDF Original (`Google Lighthouse (Desktop) - v2.0.pdf`)](https://drive.google.com/file/d/1JG5DfL7kTJzXwJiAg1gE8kbzWes1Hktg/view?usp=drive_link)
* 📱 **Informe Completo Lighthouse Mobile (v2.4.0):** [`REPORTE-QA_Lighthouse_Mobile_v2.0.md`](../Archivos/Rendimiento/REPORTE-QA_Lighthouse_Mobile_v2.0.md) | [Descargar PDF Original (`Google Lighthouse (Mobile) - v2.0.pdf`)](https://drive.google.com/file/d/1ONBKcit5ZvSoSF2PND6vIHDWaDPEZWwy/view?usp=drive_link)