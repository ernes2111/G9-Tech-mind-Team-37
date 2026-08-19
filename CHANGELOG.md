# CHANGELOG — TechMind · Proyecto Completo

> Todas las versiones están ordenadas de la más reciente a la más antigua.
> Se sigue el formato [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/).
> Para el detalle técnico (causa, síntoma y código) de cada bug, ver [`BUGFIX_REGISTRO.md`](data-science/docs/BUGFIX_REGISTRO.md).

## [2.5.0] — 2026-08-19 · Mini Popover Lateral de Servicios, Animación del Clasificador, Correcciones de UX Móvil y Modo Oscuro

### Añadido

- **Mini Popover Lateral de Estado de Servicios en Sidebar Colapsado (`frontend/index.html` + `frontend/app.js`):**
  - **Problema previo:** Al tener el sidebar contraído y hacer clic en el botón *"Estado de servicios"*, no ocurría ninguna acción ya que el popover completo (`#status-popover`) quedaba oculto detrás del rail de 64px.
  - **Solución:** Añadido nuevo `#status-mini-popover` que aparece hacia la **derecha del sidebar** cuando está colapsado, mostrando de forma compacta el estado de los 3 microservicios (Spring Boot, FastAPI ML, PostgreSQL) con sus LEDs de color sin necesidad de expandir el sidebar.
  - **Posicionamiento dinámico:** El mini popover se posiciona con `position: fixed` y `left: calc(var(--sidebar-collapsed-width) + 8px)`. El eje `top` se calcula en tiempo de ejecución con `getBoundingClientRect()` para centrarlo verticalmente respecto al botón disparador, con protección de márgenes del viewport.
  - **Sincronización automática de LEDs:** La función `setServiceStatus()` fue extendida para sincronizar en paralelo los LEDs del popover principal (`status-springboot`, `status-fastapi`, `status-postgres`) y los LEDs espejo del mini popover (`mini-led-springboot`, `mini-led-fastapi`, `mini-led-postgres`) sin duplicar ninguna lógica de negocio.
  - **Comportamiento diferenciado por estado del sidebar:** El handler de `#btn-status-trigger` detecta `sidebarCollapsed` en tiempo de clic: si el sidebar está colapsado abre el mini popover lateral; si está expandido, abre el popover completo con métricas OCI. Ambos se cierran mutuamente al alternarse.
  - **Cierre automático:** Al expandir el sidebar (`expandSidebar()`), el mini popover se cierra automáticamente. Ambos popovers se cierran al hacer clic en cualquier otra área del documento.

### Corregido

- **Flash de Animación del Sidebar en Carga Inicial (Móvil) (`frontend/app.js`):**
  - **Síntoma:** Al recargar la página en dispositivos móviles, se percibía una micro-animación de contracción del sidebar (visible durante ~150ms), dado que el DOM inicia con el sidebar en estado expandido y JS lo colapsaba con las transiciones CSS ya activas.
  - **Causa:** `collapseSidebar()` se invocaba durante `DOMContentLoaded` mientras la regla de transición cinematográfica de 350ms (`cubic-bezier(0.16, 1, 0.3, 1)`) sobre `#sidebar` ya estaba computada.
  - **Solución (v2.5.0):** Resuelta de forma global por la supresión de transiciones en carga inicial (ver entrada siguiente). La lógica de inicialización del sidebar en móvil se simplificó eliminando el override manual de `sidebar.style.transition`.

- **Flash Global de Transiciones en Carga Inicial (`frontend/index.html`):**
  - **Síntoma:** Al cargar o refrescar la página (especialmente en móviles), múltiples elementos (`body`, `sidebar`, `main-content`, `button`, `input`, etc.) mostraban una breve animación de color/layout (flash) causada por las transiciones CSS de 350ms que se disparaban al aplicar el tema y el estado inicial.
  - **Causa:** La regla CSS de transición cinematográfica global se aplica al parsear el stylesheet, antes de que el DOM esté completamente inicializado. Al ejecutar JS para establecer el tema (`dark`/`light`) y el estado del sidebar, los cambios de `background-color`, `color` y `border-color` eran interpolados visiblemente por el navegador.
  - **Solución:** Implementada la técnica estándar *"No-transition on load"*:
    1. El elemento `<html>` inicia con la clase `no-transition` en el HTML estático.
    2. Una regla CSS `!important` anula todas las transiciones y reduce todas las animaciones a `0.01ms` mientras la clase esté presente.
    3. Un script `<script>` **inline y síncrono** en el `<head>` (antes de cualquier recurso externo) programa la remoción de `no-transition` mediante **doble `requestAnimationFrame`**, garantizando que la clase se elimine solo después del primer frame pintado en pantalla.
    - El resultado: cero transiciones visibles durante la carga inicial, con todas las micro-interacciones y animaciones funcionando normalmente a partir del primer pintado.

- **Bordes Invisibles en Modo Oscuro en Botones Secundarios del Formulario (`frontend/index.html`):**
  - **Síntoma:** Los botones *"Importar PDF / DOCX"* (`#btn-import-doc`) y *"Limpiar formulario"* (`#btn-clear-form`) no mostraban borde visible en Modo Oscuro, luciendo como elementos sin delimitación.
  - **Causa:** Ambos botones usaban `dark:border-outline-variant` con opacidades bajas (`/70` y `/50`). La variable `--outline-variant` en dark mode vale `#494454`, un tono muy próximo al fondo del sistema (`#0b1326`), lo que hacía el borde prácticamente invisible independientemente de la opacidad aplicada.
  - **Solución:** Reemplazada la referencia a `outline-variant` por `primary` (`#d0bcff`, el lila claro del sistema de diseño) con opacidades calibradas: `dark:border-primary/25` para el borde dashed de Importar y `dark:border-primary/20` para el borde sólido de Limpiar. Los estados hover se actualizaron a `dark:hover:border-primary/50` y `/45` respectivamente, manteniendo coherencia visual con el color primario del tema.

- **Animación del Botón "Clasificar con TechMind" al Detectar Contenido (`frontend/index.html` + `frontend/app.js`):**
  - Cuando **ambos campos** del formulario (*Título* y *Contenido*) tienen texto, el botón entra en estado *"listo"* activando tres capas de micro-feedback visual:
    1. **Glow pulsante exterior (`@keyframes classifyGlow`):** Anillo de luz semitransparente con pulso sinusoidal cada 2 segundos que rodea el botón, comunicando energía y disposición.
    2. **Shine sweep (`@keyframes classifyShine`):** Destello diagonal blanco translúcido (`via-white/20`) que recorre el botón de izquierda a derecha cada 2.2 segundos.
    3. **Ícono de rayo (`⚡ bolt`):** Aparece a la izquierda del texto con animación de entrada `fade + slide` (`@keyframes classifyIconIn` en 0.35s). Al vaciar algún campo, sale con animación inversa (`classifyIconOut` en 0.25s) y el espacio se colapsa.
  - La detección es reactiva: escucha el evento `input` en ambos campos y evalúa `value.trim()` en tiempo real.
  - Al hacer clic en *"Limpiar formulario"*, se llama `updateClassifyReadyState()` para resetear el estado visual inmediatamente.
  - Evalúa el estado inicial al cargar la página para cubrir el caso de campos pre-rellenados por autocompletado del navegador.

## [2.4.0] — 2026-08-15 · Transición Cinemática de Tema, Microanimaciones, UI/UX Pulida, Tooltips Dinámicos y Precisión Decimal

### Añadido

- **Transición Visual Cinemática de Tema y Microanimaciones (`frontend/index.html` + `frontend/app.js`):**
  - **Física de Transición Suave (`cubic-bezier(0.16, 1, 0.3, 1)`):** Eliminada la regla de transición universal destructiva `*` y reemplazada por transiciones selectivas aceleradas por hardware de 350ms sobre superficies, contenedores glass, barras laterales, inputs y modales, logrando un cambio de iluminación continuo y gradual sin *layout reflows* ni microparpadeos.
  - **Microanimación 3D del Icono Sol ☀️ ⇄ Luna 🌙:** Giro rotacional suave de 360° con reducción de escala y destello luminoso (`@keyframes themeIconSpin` en 0.45s), conmutando el glifo a mitad de animación (`200ms`) en el punto de compresión mínima para una metamorfosis visual fluida.
  - **Sincronización Dinámica de Gráficos (`frontend/app.js`):** Implementada la función `updateChartsTheme()` que actualiza dinámicamente colores de grilla, bordes y leyendas de los gráficos Chart.js activos en tiempo real sin recargar datos ni destruir instancias de Canvas.

- **Botón "Copiar texto" en Tarjetas de Historial (`frontend/index.html` + `frontend/app.js`):**
  - **Acción directa (`.btn-copy-entry-text`):** Añadido botón pill junto a *"Ver más"* en las tarjetas de publicaciones recientes y del historial detallado, permitiendo copiar al portapapeles el texto íntegro del artículo/documento con un solo clic.
  - **Feedback visual y háptico:** Al copiar, el botón realiza una micro-transición hacia estado de confirmación (`¡Copiado!` / `Copied!` en verde esmeralda con icono `check`), dispara un toast flotante y genera una vibración háptica de 15ms.
  - Soporte multilingüe en tiempo real con claves `copy_text` y `toast_text_copied` en los diccionarios `TRANSLATIONS.es` y `TRANSLATIONS.en`.

- **Tooltips Flotantes Dinámicos en Sidebar Colapsado (`frontend/index.html` + `frontend/app.js`):**
  - Añadidos tooltips flotantes (`.sidebar-collapsed-tooltip`) a todos los botones del sidebar colapsado: Clasificador, Historial, Análisis, Tema, Estado de servicios y Toggle superior.
  - **Sincronización 100% en tiempo real:**
    - Botón de Tema: muestra dinámicamente `"Modo claro"` cuando el sol está visible (modo oscuro activo) y `"Modo oscuro"` cuando la luna está visible (modo claro activo).
    - Botón de Sidebar: muestra `"Cerrar barra lateral"` cuando la barra está abierta y `"Abrir barra lateral"` cuando está cerrada.
  - **Contraste y Legibilidad WCAG AAA:**
    - En **Modo Claro**: fondo blanco puro sólido (`#ffffff`), borde morado fino (`rgba(92, 62, 145, 0.3)`), sombra púrpura suave y tipografía en púrpura profundo (`#2b0b4a`) con contraste superior a 14:1.
    - En **Modo Oscuro**: fondo dark glass (`#171f33`), borde cyber (`rgba(208, 188, 255, 0.35)`) y texto blanco puro (`#ffffff`).
  - Soporte multilingüe en tiempo real (Español / Inglés).

- **Placeholders Dinámicos e Interactivos con Animación Typewriter (`frontend/index.html` + `frontend/app.js`):**
  - Reemplazado el placeholder estático y complejo anterior por una rotación de ejemplos técnicos amigables y accesibles:
    - *Español:* `ej. Tratamiento y gestión de bases de datos`, `ej. Introducción a la programación en Python`, `ej. Primeros pasos con Git y GitHub`, `ej. Guía básica de ciberseguridad y contraseñas`, `ej. Desarrollo de páginas y aplicaciones web`, `ej. Qué es el Cloud Computing y cómo funciona`, `ej. Conceptos fundamentales de Inteligencia Artificial`.
    - *Inglés:* `e.g. Database management & processing`, `e.g. Introduction to Python programming`, `e.g. Getting started with Git & GitHub`, etc.
  - **Comportamiento inteligente:** Efecto máquina de escribir suave (45ms por caracter, 3.2s de pausa de lectura). Se pausa automáticamente si el usuario hace foco o escribe en el campo, y se reanuda suavemente si el campo queda vacío al salir.

- **Sincronización Dinámica de `theme-color` en Navegadores Móviles (`frontend/index.html` + `frontend/app.js`):**
  - Añadido meta tag `<meta name="theme-color" content="#0b1326" id="meta-theme-color" />` en el `<head>`.
  - Sincronización en tiempo real desde `updateThemeToggleUI()`: conmuta automáticamente entre `#0b1326` (Modo Oscuro) y `#e8e2d5` (Modo Claro) para colorear la barra de estado nativa superior en navegadores móviles como Safari (iOS) y Chrome (Android), logrando una integración visual inmersiva de borde a borde.

- **Respuesta Háptica Táctil en Dispositivos Móviles (`frontend/app.js`):**
  - Implementada la función helper `triggerHaptic(pattern)` utilizando la API nativa `navigator.vibrate()`.
  - Proporciona microvibraciones hápticas de confirmación física (entre 10ms y 22ms) en eventos clave de la interfaz:
    - *Clasificación exitosa:* doble pulso suave de confirmación `[18, 40, 22]`.
    - *Alternar Modo Claro / Modo Oscuro:* vibración instantánea `15ms`.
    - *Copiar contenido al portapapeles:* vibración táctil `15ms`.
    - *Expandir/colapsar tarjeta:* pulso sutil `10ms`.
    - *Limpiar formulario:* pulso de vaciado `15ms`.
    - *Alternar idioma:* pulso táctil `12ms`.
    - *Extracción exitosa de documento PDF/DOCX:* pulso doble `[15, 30, 15]`.

- **Accesibilidad y Atajos de Teclado (`frontend/app.js`):**
  - Añadido soporte para cerrar el modal de inicio de sesión de Admin o el modal de JSON al presionar la tecla `Escape`.

### Modificado

- **Botón "Ver más / Ver menos" y Grid de Historial (`frontend/index.html` + `frontend/app.js`):**
  - **Calibración inteligente de umbral:** Ajustado a 110 caracteres en el grid de publicaciones recientes y a 150 caracteres en el listado detallado (antes 30 caracteres), asegurando que el botón solo aparezca cuando el texto realmente desborda los dos renglones de `line-clamp-2`.
  - **Expansión diferenciada por vista:** En el grid del *Clasificador* se expande hasta un máximo de **10 renglones** (`.line-clamp-10`) para no deformar verticalmente la vista principal, mientras que en la vista detallada de *Historial* se expande el contenido en su totalidad (`line-clamp-none`).
  - **Alineación simétrica:** Las tarjetas del grid de inicio ahora utilizan `h-full flex flex-col justify-between` para garantizar una altura homogénea y una alineación visual perfecta de la barra de acciones inferiores.
  - **Accesibilidad y UX:** Incorporado el atributo `aria-expanded` dinámico y micro-transición rotacional en el icono chevron.

- **Estandarización de Terminología Bilingüe en Barra Lateral (`frontend/index.html` + `frontend/app.js`):**
  - Actualizados los textos de la barra lateral para mayor claridad y coherencia en ambos idiomas:
    - *Español:* `"Abrir barra lateral"` / `"Cerrar barra lateral"` (reemplazando los anglicismos anteriores).
    - *Inglés:* `"Open sidebar"` / `"Close sidebar"`.
  - Actualizados los atributos de accesibilidad (`aria-label`, `title`) y tooltips flotantes en tiempo real para desktop y mobile.
  - Actualizada la versión del script en `frontend/index.html` (`app.js?v=2.4.0`) para invalidar la caché estática de los clientes.

- **Subtítulo del Clasificador Principal (`frontend/index.html` + `frontend/app.js`):**
  - Reemplazada la palabra *"clasificarlos"* por *"categorizarlos"* (`"Ingresá textos para categorizarlos en tiempo real"` / `"Enter texts to categorize them in real time"`), eliminando la redundancia léxica con el título superior (*"Clasificación de contenido técnico"*).

- **Botones Secundarios del Formulario Principal (`frontend/index.html`):**
  - **Botón "Importar PDF / DOCX" (`#btn-import-doc`):** Añadido recuadro punteado nítido (`border-dashed border-purple-900/30`), fondo translúcido (`bg-purple-900/5`), sombra sutil (`shadow-sm`) y texto en púrpura oscuro (`text-purple-950`) en Modo Claro para delimitar claramente el área de acción.
  - **Botón "Limpiar formulario" (`#btn-clear-form`):** Añadido borde sólido (`border-purple-900/25`), fondo blanco translúcido (`bg-white/70`), sombra suave (`shadow-sm`) y tipografía de alto contraste en Modo Claro, equilibrando su presencia con el botón principal de clasificar.
  - **Etiqueta del contenido:** Simplificada a `"Contenido del documento o artículo"` (ES) / `"Document or article content"` (EN).

- **Modal de Inicio de Sesión de Administrador (`frontend/index.html` + `frontend/app.js`):**
  - Eliminado el botón redundante "Cancelar" del pie del formulario (el usuario dispone del botón de cierre `✕`, clic en backdrop exterior o tecla `Escape`).
  - Rediseñado el botón principal "Ingresar" a ancho completo (`w-full py-3`) con estilo de elevación moderno para facilitar la interacción táctil y de escritorio.

- **Dimensiones y Centrado del Botón Toggle de Sidebar (`frontend/index.html`):**
  - Homologado el tamaño grande (`3rem` / 48px) del icono chevron tanto en estado expandido como colapsado en pantallas de escritorio, manteniendo un centrado geométrico perfecto en el rail colapsado de 64px.

### Corregido

- **Compatibilidad de Copia al Portapapeles en Entornos HTTP / OCI (`frontend/app.js`):**
  - **Síntoma:** Al acceder a la aplicación mediante una IP pública o dominio sin SSL/TLS en servidores OCI (`http://<ip>:5173`), los botones *"Copiar texto"* y *"Copiar JSON"* no lograban escribir en el portapapeles.
  - **Causa:** La API moderna `navigator.clipboard` está restringida por las políticas de seguridad de los navegadores exclusivamente a *Contextos Seguros* (`HTTPS` o `localhost`). Al acceder vía `HTTP` desde una IP remota, `navigator.clipboard` es `undefined` o bloqueado por el navegador.
  - **Solución:** Implementada la función universal `copyToClipboard()` con mecanismo de fallback transparente basado en `document.execCommand('copy')`, garantizando copiado 100% funcional en servidores cloud (OCI), conexiones HTTP, dominios con HTTPS y navegadores móviles.

- **Precisión Decimal en Porcentaje de Confianza (`app/database.py` + `frontend/app.js`):**
  - **Síntoma:** El porcentaje de confianza en las tarjetas del *Clasificador* y del *Historial* siempre mostraba decimales redondeados en cero (ej. `26.0%`, `56.0%`).
  - **Causa:** En `app/database.py` la consulta a PostgreSQL truncaba la probabilidad a 2 decimales (`round(float(r[3]), 2)`), y en `frontend/app.js` se aplicaba un redondeo prematuro a 2 decimales (`Math.round(prob * 100) / 100`), provocando que al multiplicarse por 100 el resultado fuera siempre un número entero que `.toFixed(1)` formateaba con `.0%`.
  - **Solución:** Se preservó la precisión a 4 decimales tanto en la API de base de datos (`round(float(r[3]), 4)`) como en el cliente frontend (`Math.round(prob * 10000) / 10000`), permitiendo desplegar porcentajes con decimales reales exactos (ej. `27.8%`, `56.5%`, `72.5%`).

- **Docker — Fallo de arranque de Nginx por UTF-8 BOM (`frontend/nginx.conf`):**
  - **Síntoma:** El contenedor `techmind-frontend` fallaba al iniciar con código de salida `1` (`unknown directive` en línea 1).
  - **Causa:** Un carácter invisible UTF-8 BOM (Byte Order Mark) al inicio del archivo generado por editores en Windows impedía el parseo de Nginx.
  - **Solución:** Reescrito el archivo `frontend/nginx.conf` en codificación UTF-8 estricta sin BOM (`UTF8Encoding($false)`).

- **Scope de Funciones en Inicialización de DOM (`frontend/app.js`):**
  - **Síntoma:** Los botones de la aplicación dejaron de responder a los clics.
  - **Causa:** `updateSidebarToggleIcons()` y `sidebarCollapsed` estaban declaradas con scope local dentro de `bindEvents()`. Al ser invocadas previamente por `applyTranslations()` durante `DOMContentLoaded`, se producía un `ReferenceError` que abortaba la ejecución del hilo principal antes de registrar los event listeners.
  - **Solución:** Se elevaron `sidebarCollapsed` y `updateSidebarToggleIcons()` al ámbito global de `app.js`.

- **Desfasaje Vertical de Tooltips al cambiar de pestaña (`frontend/index.html` + `frontend/app.js`):**
  - **Síntoma:** Al hacer clic en "Historial" o "Análisis", el tooltip flotante saltaba al centro vertical del sidebar.
  - **Causa:** Las funciones de cambio de vista sobreescribían destructivamente la propiedad `className` de los enlaces, perdiendo la clase `relative` y provocando que el tooltip hijo se anclara al `#sidebar` contenedor en lugar del botón individual.
  - **Solución:** Se añadió `position: relative !important;` en CSS a `.sidebar-nav-item` y se refactorizó la lógica en JS mediante `classList.toggle('active-nav')`.

- **Menú Móvil — Apertura Forzada de "Estado de Servicios" y Alineación (`frontend/index.html` + `frontend/app.js`):**
  - **Síntoma:** Al presionar el icono hamburguesa en móviles, se abría automáticamente la ventana flotante de "Estado de servicios" y, al abrirse, aparecía desfasada hacia la derecha de la pantalla.
  - **Causa:** Un temporizador `setTimeout` en `toggleSidebar()` forzaba la apertura y una regla CSS con offset fijo (`left: 74px`) desalineaba el panel con respecto al sidebar expandido.
  - **Solución:** Eliminada la llamada forzada en `app.js` y reconfigurado `#status-popover` con `left: 0; right: 0; width: 100%;` en `index.html` para un despliegue alineado al margen izquierdo del menú móvil.
  - Ocultamiento estricto del botón `#btn-sidebar-mobile` en computadoras de escritorio (`@media (min-width: 768px)`).

## [2.3.0] — 2026-08-14 · Optimizaciones Lighthouse Sprint 5: Performance, Accesibilidad, Best Practices y SEO

### Añadido

- **Cabeceras de Seguridad HTTP en Nginx (`frontend/nginx.conf` [NUEVO] + `frontend/Dockerfile`):**
  - Creado `nginx.conf` personalizado con cabeceras de seguridad HTTP que resuelven las brechas detectadas en el Sprint 5 de QA (Best Practices 74→~95).
  - `X-Frame-Options: SAMEORIGIN` — Previene ataques de Clickjacking.
  - `X-Content-Type-Options: nosniff` — Previene MIME-type sniffing.
  - `Referrer-Policy: strict-origin-when-cross-origin` — Controla la información de referrer enviada a terceros.
  - `Permissions-Policy` — Restringe APIs del navegador no utilizadas (`camera`, `microphone`, `geolocation`, `payment`).
  - `Content-Security-Policy` — Política CSP que permite los CDNs requeridos (`tailwindcss`, `jsdelivr`, `fonts.googleapis.com`) y bloquea orígenes no autorizados.
  - Compresión `gzip` habilitada para reducir el payload de red (JS, CSS, JSON, SVG).
  - Cache headers para assets estáticos: 1 año para JS/CSS versionados, 30 días para fuentes e imágenes.
  - `server_tokens off` — Oculta la versión de Nginx en cabeceras de respuesta.
  - Actualizado `frontend/Dockerfile` para copiar `nginx.conf` al contenedor con `COPY frontend/nginx.conf /etc/nginx/nginx.conf`.

- **CSS `size-adjust` para Font Fallbacks (`frontend/index.html`):**
  - Añadidas declaraciones `@font-face` para `Inter-fallback` y `Outfit-fallback` usando `local('Arial')` como fuente base.
  - Propiedades `ascent-override`, `descent-override` y `size-adjust` calibradas para que el fallback del sistema tenga métricas casi idénticas a Inter/Outfit, minimizando el FOUT (Flash of Unstyled Text) y el CLS durante la carga de la fuente web.

- **Prevención de CLS por Layout en `#main-content` (`frontend/index.html`):**
  - Añadido `min-height: 100vh` a `#main-content` para reservar el espacio vertical antes de que JS monte el DOM dinámico, evitando el reflow masivo en la carga inicial.
  - Añadido `contain: layout` para aislar el contexto de layout y reducir el scope de los recálculos del motor de renderizado.

- **Animaciones GPU-composited (`frontend/index.html`):**
  - Añadido `will-change: opacity` y `transform: translateZ(0)` a los selectores `.animate-pulse`, `[class*="shimmer"]` y `.led-pulse` para que el navegador las componga en una capa de GPU separada, eliminando su contribución al CLS y reduciendo el trabajo del hilo principal.

- **`aria-label` y atributos ARIA en `#btn-status-trigger` (`frontend/index.html`):**
  - Agregados `aria-label="Estado de servicios"`, `aria-haspopup="true"` y `aria-expanded="false"` al botón de estado de servicios del sidebar.
  - Resuelve el hallazgo de Accesibilidad (87→~95): lectores de pantalla como NVDA y VoiceOver ahora anuncian correctamente la función del botón.

### Corregido

- **SEO — Falta de `<meta name="description">` (`frontend/index.html`):**
  - Añadida la etiqueta `<meta name="description" content="TechMind — Plataforma inteligente de clasificación y organización de contenido técnico. Detecta categorías como Backend, Frontend, Data Science, DevOps, Cloud y más con Machine Learning." />`.
  - Resuelve el único hallazgo de SEO: puntaje SEO sube de 90 → **100/100**.

- **Performance — Fuentes Google Fonts bloqueantes con CLS 1.516 (`frontend/index.html`):**
  - **Síntoma:** El puntaje CLS era de `1.516` (umbral óptimo `< 0.1`) en Desktop, causado por fuentes cargadas con `display=block` que mantenían el texto invisible hasta terminar la descarga, provocando saltos de layout masivos.
  - **Causa:** Tres familias de fuentes (`Inter`, `JetBrains Mono`, `Outfit`) con `display=block` y múltiples weights innecesarios sumaban **1.2 MB** de `.woff2` (72.5% del payload total).
  - **Solución:**
    - Cambiado `display=block` → `display=swap` en todas las URLs de Google Fonts: el texto es inmediatamente visible con la fuente del sistema y se sustituye sin layout shift cuando la fuente web carga.
    - Reducidos los weights a los únicos realmente usados: `Inter:wght@400;600`, `Outfit:wght@600;700`, `JetBrains Mono:wght@400`. Reduce el peso de woff2 de ~1.2 MB a ~400 KB.
    - Añadido `&subset=latin` para descargar solo los glifos latinos.
    - Cambiado Material Symbols de variación completa (`wght,FILL@100..700,0..1`) a valor fijo (`wght,FILL@400,0`), reduciendo el peso del CSS de íconos.
    - Font fallback CSS con `size-adjust` para que el cambio de fuente sea imperceptible visualmente.

- **Performance — `chart.js` bloqueando el render (−550ms desktop / −3s mobile) (`frontend/index.html`):**
  - **Síntoma:** `chart.js` (70.5 KB) se cargaba sincrónicamente en el `<head>`, bloqueando el First Contentful Paint.
  - **Causa:** `<script src="https://cdn.jsdelivr.net/npm/chart.js">` sin atributo `defer` en el head.
  - **Solución:** Movido al final del `<body>` con atributo `defer` y versión pinneada `@4.4.4`:
    `<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.4/dist/chart.umd.min.js" defer></script>`
  - Pineado a `@4.4.4` también resuelve el error **404 del Source Map** (`chart.umd.min.js.map`) reportado en Lighthouse Best Practices.

- **Accesibilidad — Contraste insuficiente en badge Cloud (WCAG 2.1 AA) (`frontend/app.js`):**
  - **Síntoma:** `dark:text-sky-400` sobre fondo `#0b1326` (modo oscuro) no superaba la relación de contraste mínima de 4.5:1 según WCAG 2.1 AA.
  - **Solución:** Cambiado `dark:text-sky-400` → `dark:text-sky-300` en `CATEGORY_CONFIG['Cloud']`. `sky-300` tiene mayor luminancia y supera el ratio requerido.

- **Accesibilidad — Contraste insuficiente en tarjetas del historial (`frontend/app.js`):**
  - **Síntoma:** Los párrafos `.history-card-body` tenían clase `opacity-80` que reducía el contraste efectivo del color `text-on-surface-variant`, incumpliendo WCAG 2.1 AA bajo luz solar en dispositivos móviles.
  - **Solución:** Eliminada la clase `opacity-80` de los 2 elementos `.history-card-body` (vista grid y vista lista del historial). El color `text-on-surface-variant` ya provee contraste adecuado sin necesidad de reducir la opacidad.

- **Versión de app.js incrementada** de `v=1.6.0` → `v=1.7.0` para forzar recarga del caché en clientes que ya tengan la versión anterior almacenada.

## [2.2.2] — 2026-08-11 · Rate Limiting de Importación de Documentos para Invitados

### Añadido

- **Control de Frecuencia (Rate Limiting) para Importación de Documentos (`frontend/app.js`):**
  - **Límite para Invitados:** Implementado el gestor `DocImportRateLimit` basado en `localStorage` (`techmind_import_rl`) que restringe a usuarios no autenticados a un máximo de **5 importaciones de archivos PDF/DOCX cada 8 horas**.
  - **Acceso Ilimitado para Administradores:** Si el usuario tiene una sesión activa de Administrador (`isLoggedInAsAdmin()`), el sistema omite el check y permite importaciones ilimitadas.
  - **Feedback y Autorestablecimiento:** Cuando un usuario invitado alcanza el límite, el sistema bloquea la petición a `/extraer-texto` y muestra un aviso Toast extendido (4 segundos de duración) con el tiempo exacto restante formateado (ej. *"Límite alcanzado: ya importaste 5 documentos. Probá de nuevo en 6h 42m. Iniciá sesión como Admin para no tener límites."*). El contador se reinicia automáticamente una vez cumplidas las 8 horas.
  - **i18n:** Agregadas las claves correspondientes en los diccionarios de español e inglés.

## [2.2.1] — 2026-08-11 · Patch: Traducción del Filtro de Categorías en Historial

### Corregido

- **Filtro de categorías en "Historial" no se traducía al cambiar el idioma a inglés (`frontend/app.js`):**
  - **Síntoma:** Al cambiar la UI a inglés, las opciones del `<select>` de filtro seguían mostrando los nombres en español (`Bases de Datos`, `Seguridad`), ya que el elemento no tenía atributos `data-i18n` y `applyTranslations()` no lo procesaba.
  - **Causa:** Las opciones se renderizan desde HTML estático con texto hardcodeado, y `updateCategoryFilterCounts()` usaba un mapa de etiquetas también hardcodeado en español.
  - **Solución sin tocar la DB:** El `value` de cada `<option>` permanece en español (es el valor que se compara contra los registros de la base de datos para filtrar). Solo el **texto visible** se traduce:
    - Añadida función helper `getCategoryLabel(value)` que resuelve la etiqueta localizada según el idioma activo (`t()`).
    - Actualizado `updateCategoryFilterCounts()` para usar `getCategoryLabel()` al construir el texto de cada opción (incluido el conteo `(N)`).
    - Añadido bloque en `applyTranslations()` que re-etiqueta las opciones del filtro al cambiar de idioma, preservando el sufijo de conteo entre paréntesis si ya estaba visible.
    - Añadidas claves de internacionalización `cat_bases_de_datos` y `cat_seguridad` en los diccionarios ES y EN de `TRANSLATIONS` (las demás categorías —`Backend`, `Frontend`, `Data Science`, `DevOps`, `Mobile`, `Cloud`— son iguales en ambos idiomas).
  - **Categorías traducidas:** `Bases de Datos` → `Databases` · `Seguridad` → `Security`

## [2.2.0] — 2026-08-11 · Importación de Documentos (PDF/DOCX), Seguridad de Archivos y Optimización del Sidebar

### Añadido

- **Módulo de Extracción de Documentos PDF y DOCX (`app/documento_extractor.py`):**
  - Módulo independiente para extracción de texto desde archivos `.pdf` (vía `pdfplumber`, limitado a 15 páginas máximo) y `.docx` (vía `python-docx`, limitado a 4.500 palabras equivalentes a 15 páginas).
  - Truncado automático de texto a 20.000 caracteres como protección de RAM para OCI Free Tier (límite de 220 MB de memoria en FastAPI).
  - Inferencia inteligente de título en cascada (metadatos del documento → primer encabezado/título de pág. 1 → nombre de archivo sanitizado).
  - Manejo robusto de errores con mensajes descriptivos en español (archivos corruptos, PDF encriptado, archivos vacíos o con menos de 10 palabras).

- **Endpoint REST `POST /extraer-texto` en FastAPI (`app/main.py`):**
  - Endpoint asíncrono que recibe un `UploadFile` (PDF/DOCX de hasta 5 MB) y retorna `{titulo, texto, paginas_procesadas, formato, texto_truncado, advertencia}`.
  - Endpoint stateless sin inferencia ML directa: extrae el contenido y lo devuelve a la UI para que el usuario pueda revisarlo y editarlo antes de clasificar.

- **Importación de Documentos y Previsualización Editable en UI (`frontend/index.html` + `frontend/app.js`):**
  - Añadido botón "Importar PDF / DOCX" debajo del área de texto con selector de archivo nativo `<input type="file" accept=".pdf,.docx">`.
  - Función `handleFileUpload()` que valida la extensión y tamaño (≤ 5 MB) en el navegador antes de enviar la petición.
  - Muestra spinner "Extrayendo texto…" en el botón durante la petición y puebla automáticamente los campos "Título" y "Contenido" del formulario al finalizar, dejando el cursor en el título para fácil edición.
  - Badge verde de confirmación con ícono `check_circle` que indica el archivo importado y las páginas procesadas, con desvanecimiento automático (fade-out) a los 5 segundos.
  - Limpieza automática del badge e input de archivo al hacer clic en "Limpiar formulario".
  - Añadidas 7 claves i18n nuevas en español e inglés dentro del diccionario `TRANSLATIONS` (`btn_import_doc`, `extracting_text`, `file_too_large`, `invalid_file_type`, `text_extracted_badge`, `text_extracted_badge_warning`, `toast_extract_error`).

### Corregido

- **Seguridad en Subida de Archivos (Sanitización y Validación Rigurosa en `app/main.py` y `app/documento_extractor.py`):**
  - **Gate Obligatorio de Extensión:** La extensión `.pdf` / `.docx` se valida *antes* de leer el contenido en bytes, evitando consumo innecesario de memoria en el servidor.
  - **Validación Estricta de Content-Type:** Cambiado de substring match permisivo (`in`) a comparación exacta descartando parámetros de cabecera (e.g. `; charset=`), bloqueando nombres spoofeadas o Content-Types alterados (`application/pdf-evil`).
  - **Sanitización de Path Traversal:** Sanitización del `filename` en dos capas (endpoint + helper de extracción) eliminando caracteres `/`, `\` y puntos iniciales (`..`) mediante expresiones regulares para prevenir Directory Traversal.

- **Crash del Contenedor Docker de FastAPI por Falta de `python-multipart` (`data-science/requirements.txt`):**
  - Agregada la dependencia `python-multipart>=0.0.9` en `requirements.txt`. FastAPI requiere esta librería para procesar peticiones `multipart/form-data` (`UploadFile`); su ausencia provocaba un error de arranque en el contenedor.

- **Límites Preventivos Multipart en Backend Spring Boot (`backend/api/src/main/resources/application.properties`):**
  - Agregadas las propiedades `spring.servlet.multipart.max-file-size=5MB` y `spring.servlet.multipart.max-request-size=6MB` como protección adicional del servidor Java.

- **Optimización de Velocidad y Respuesta del Sidebar (`frontend/index.html` + `frontend/app.js`):**
  - Reducida la duración de las transiciones CSS del sidebar (`width`, `padding-left`, `transform`, `background-color`, `border-color`, `color`) y del margen del contenedor `#main-content` de `0.3s` a `0.15s` (`150ms`).
  - Actualizada la constante JS `SIDEBAR_ANIM_MS` de `320ms` a `150ms`, logrando que la interfaz responda al instante al expandir/colapsar el menú de navegación.

## [2.1.0] — 2026-08-10 · Ajustes de Simetría, Botones del Formulario, Admin Dropdown y Responsividad Móvil

### Corregido

- **Botones "Clasificar" y "Limpiar formulario" desalineados y con íconos innecesarios (`frontend/index.html` + `frontend/app.js`):**
  - Eliminados los íconos `science` y `delete_sweep` de ambos botones del formulario de clasificación para un aspecto más limpio y profesional.
  - Centrado perfecto del texto en ambos botones con `flex items-center justify-center text-center`, dimensiones simétricas (`min-w-[200px]`, `px-8 py-3.5`) y estilos uniformes.
  - Actualizada la función `setLoadingState()` en `app.js` para que no reinserte íconos dinámicamente al restaurar el botón tras una clasificación. El estado de carga ahora muestra solo texto "Analizando..." centrado.

- **Botón Admin con dimensiones inconsistentes y dropdown desalineado (`frontend/index.html`):**
  - Reestructurado el botón `#btn-admin-auth` y su dropdown `#admin-user-popover` dentro de un contenedor `div.relative` compartido.
  - El botón Admin en móvil muestra solo el ícono (sin `min-width` forzado), y en `sm:` muestra el texto completo con `sm:min-w-[160px]`.
  - El dropdown ahora usa `w-full left-0 right-0` para heredar exactamente el ancho del botón padre, logrando simetría perfecta en los bordes izquierdo y derecho.

- **Dropdown de Admin desbordaba la pantalla en móvil (`frontend/index.html`):**
  - Añadida regla CSS en `@media (max-width: 767px)` que convierte el popover a `position: fixed` con `right: 8px`, `width: calc(100vw - 16px)` y `max-width: 280px`, evitando overflow en pantallas pequeñas.

- **Tarjetas de historial detallado no eran responsive en móvil (`frontend/app.js`):**
  - Panel de "Confianza + Ver JSON" en la vista de historial detallado (`loadDetailedHistory`): en móvil ahora se dispone como fila horizontal (`flex-row`) con `justify-between` (Confianza a la izquierda, botones a la derecha). En `md:` se mantiene como columna vertical centrada con borde separador a la izquierda.
  - Tarjetas del grid de historial reciente (`loadHistory`): botón "Ver más" reposicionado de `justify-end` a `justify-start` para alinearse con el flujo de lectura del contenido.

- **Botón "Ver más / Ver menos" con texto hardcodeado (`frontend/app.js`):**
  - El handler de click del botón `btn-toggle-expand` ahora usa `t('see_more')` y `t('see_less')` del sistema de internacionalización en lugar de strings fijos "Ver más" / "Ver menos", respetando el idioma activo.

## [2.0.0] — 2026-08-08 · Corrección de Bugs Frontend y Sistema de Internacionalización (ES / EN)

### Corregido

- **Listeners duplicados en modal "Ver JSON" (`frontend/app.js`):** El botón `#btn-view-json` y el botón de cierre `#modal-close` tenían sus event listeners registrados dos veces dentro de `bindEvents()` (líneas 182–193 y 492–501), haciendo que `toggleJsonModal()` se ejecutara dos veces por clic y el modal se abriera y cerrara instantáneamente. Eliminado el bloque duplicado.

- **Ícono `science` desaparecía tras la primera clasificación (`frontend/app.js`):** `setLoadingState(false)` reconstruía el botón "Clasificar con TechMind" sin incluir el `<span class="material-symbols-outlined">science</span>` del HTML original. El botón quedaba sin ícono después de cada uso. Corregido incluyendo el icono en el `innerHTML` de restauración.

- **LED del indicador de estado pulsaba en verde aunque hubiera servicios caídos (`frontend/app.js`):** La clase `led-pulse` (animación de glow verde) se asignaba al LED general en todos los estados, incluyendo el de error. Ahora `led-pulse` solo se aplica cuando *todos* los servicios están operativos.

- **Vista Analytics no removía la clase `flex` al cambiar de sección (`frontend/app.js`):** `showClassifier()` y `showHistory()` agregaban `hidden` a la vista de Analytics pero no removían `flex`, generando un conflicto de layout al navegar de vuelta. Agregado `analyticsView.classList.remove('flex')` en ambas funciones.

- **Botón de admin en español decía "Admin Login" (`frontend/app.js`):** Cambiado el texto del botón en estado deslogueado a `"Iniciar sesión"` en la clave `es` de `TRANSLATIONS` y en `updateAdminUIState()`, que ahora usa `t('admin_login')` en lugar del string hardcodeado.

### Añadido

- **Apertura del sidebar al hacer clic en el LED de "Estado de servicios" (`frontend/app.js`):** El indicador de microservicios en el sidebar colapsado ahora tiene el mismo comportamiento que los íconos de navegación: al hacer clic sobre él estando el sidebar colapsado, se expande automáticamente (con la animación CSS de 320 ms) y luego despliega el popover de estado. Si el sidebar ya está expandido, el popover se abre/cierra de forma normal.

- **Sistema de Internacionalización completo ES / EN (`frontend/index.html` + `frontend/app.js`):**
  - **Botón de idioma `🌐`:** Añadido botón compacto con icono `translate` (Material Symbols) junto al botón de Admin en el encabezado principal. Muestra el idioma al que se puede cambiar (`EN` / `ES`) y en pantallas pequeñas solo muestra el icono. La preferencia se persiste en `localStorage`.
  - **Diccionario `TRANSLATIONS` con 67 claves** en español e inglés, cubriendo la totalidad del texto visible de la UI:
    - Sidebar: navegación, estado de servicios, OCI Server, RAM Usada, toggle de tema.
    - Formulario: título, etiquetas, placeholders, botones.
    - Tarjeta de resultados: título, "Categoría predicha", "Esperando análisis...", "Confianza del Modelo", "Palabras clave extraídas".
    - Historial reciente y vista detallada: encabezados, buscador, filtro, botones "Ver más / Ver menos", "Borrar", "Ver JSON".
    - Analytics: KPI labels, títulos de gráficos, dataset label del line chart.
    - Modal JSON y modal de login admin: todos los textos estáticos.
    - Toasts, mensajes de error, confirmaciones de borrado y estados vacíos.
  - **Función `t(key)`:** Helper global que resuelve la clave en el idioma activo con fallback al español.
  - **Función `applyTranslations()`:** Actualiza en una sola pasada todos los elementos con `data-i18n` / `data-i18n-placeholder`, el header dinámico según la vista activa (`currentView`), el botón del toggle de tema y el estado inicial de la tarjeta de resultados cuando no hay clasificación en curso.
  - **Variable `currentView`:** Registra la vista activa (`'classifier'` / `'history'` / `'analytics'`) para que el header del encabezado se traduzca correctamente al cambiar de idioma desde cualquier sección.
  - **Atributos `data-i18n` y `data-i18n-placeholder`** agregados a ∼35 elementos estáticos en el HTML (sidebar, formulario, resultados, historial, analytics, modales).
  - **`updateThemeToggleUI()`** extraída como función global (antes era un `const` local dentro de `bindEvents()`), permitiendo que `applyTranslations()` la invoque directamente y que el toggle de tema muestre `"Dark mode"` / `"Light mode"` al cambiar al inglés.
  - Al cambiar de idioma, el contenido dinámico visible (tarjetas del historial, gráficos de Analytics) se refresca automáticamente con los textos del nuevo idioma.

---

## [1.9.0] — 2026-08-07 · Rediseño de Sidebar Estilo Claude, UX del Formulario, Responsividad Móvil y Parsing de Horarios UTC

### Añadido
- **Rediseño de Sidebar Colapsable Estilo Claude (`frontend/index.html` + `frontend/app.js`):**
  - **Colapso a Icon Rail (64px):** El sidebar ahora se reduce en escritorio a una barra de iconos centrados (44x44px) alineados simétricamente, manteniendo acceso instantáneo al logo, *Clasificador*, *Historial*, *Análisis*, *Cambiar tema* y *Estado de servicios*.
  - **Controlador Integrado en el Sidebar:** Eliminado el botón flotante del encabezado principal e integrado el chevron de colapso (`<` / `>`) directamente en la cabecera superior derecha del sidebar.
  - **Reapertura al Hacer Clic en Iconos:** Hacer clic sobre el logo de TechMind o sobre cualquier icono de navegación estando colapsado despliega suavemente el sidebar completo (256px).
  - **Reorganización del Isotipo de Marca:** El logo principal reorganiza el título **TechMind** y subtítulo **Organización inteligente** en la parte superior, ubicando el icono de cerebro (`psychology`) centrado directamente **debajo de ambos textos**.
  - **Relocalización del Botón de Cambio de Tema:** Trasladado el botón de tema (claro/oscuro) desde la barra superior hacia la parte inferior del sidebar (justo encima de *Estado de servicios*), integrándose al flujo con etiquetas dinámicas (*Modo claro* / *Modo oscuro*).
  - **Persistencia de Estado:** El estado colapsado o expandido del sidebar se conserva en `localStorage`.

- **Mejoras en el Formulario y Navegación Dinámica (`frontend/index.html` + `frontend/app.js`):**
  - **Botón "Limpiar formulario":** Incorporado botón secundario con icono `delete_sweep` junto al botón principal de clasificación para vaciar título y texto con un solo clic.
  - **Encabezados Dinámicos por Vista:** La barra superior actualiza su título y subtítulo dinámicamente según la subpágina activa (*"Clasificación de contenido técnico"*, *"Historial de consultas"*, *"Panel de análisis"*), eliminando títulos duplicados dentro del contenido.
  - **Conteo Real en Filtro por Categorías:** Las opciones del desplegable de filtro en Historial ahora muestran el número exacto de consultas por categoría (ej. `Backend (3)`, `Todas las categorías (12)`).

- **Optimización Responsiva para Dispositivos Móviles (`frontend/index.html` + `frontend/app.js`):**
  - **Botón Hamburger Móvil (`menu`):** Agregado botón de menú desplegable en el header principal para abrir el sidebar como panel overlay en pantallas `< 768px`.
  - **Botón de Admin Compacto:** El texto "Admin Login" se oculta en móviles pequeños dejando solo el icono `admin_panel_settings`, evitando el salto de línea del título principal.
  - **Pestaña de Análisis Adaptativa:** Tarjetas KPI, rejilla de gráficos de Chart.js y nube de palabras clave escalan sus paddings y tamaños de fuente para visualización perfecta en teléfonos.

- **Panel de Autenticación y Cierre por Clic Externo (`frontend/index.html` + `frontend/app.js`):**
  - **Alineación Simétrica del Popover:** Corregida la posición del menú flotante de Admin (`right-0`) alineándolo perfectamente bajo el botón superior.
  - **Cierre por Clic Fuera (Backdrop & Outside Click):** El menú desplegable de usuario y el modal de inicio de sesión se cierran automáticamente al hacer clic en cualquier área externa.
  - **Duración de Notificaciones (Toasts):** Reducido el tiempo de despliegue de las alertas flotantes de login/logout a 1.8 segundos.
  - **Identidad Visual del Escudo:** Los contenedores del icono de escudo en el popover y en el modal adoptan un tono morado/violeta (`bg-purple-500/20 text-purple-700 dark:text-purple-300`).

- **Precisión de Confianza, Gráficos y Parsing de Horarios UTC (`frontend/app.js`):**
  - **Porcentaje de Confianza con 1 Decimal:** Formateada la cifra de confianza a 1 decimal (ej. `39.5%`) en los resultados del clasificador, tarjetas del historial y KPIs de análisis.
  - **Bordes Limpios y Leyenda Circular en Chart.js:** Actualizada la leyenda del gráfico de dona con estilo de punto circular (`usePointStyle: true, pointStyle: 'circle'`), eliminando bordes negros rígidos. El gráfico se re-renderiza automáticamente al alternar entre modo claro y oscuro.
  - **Conversión de Marcas de Tiempo UTC a Hora Local (`parseDate`):** Implementada la función `parseDate(isoStr)` que parsea marcas de tiempo de PostgreSQL (`created_at`) en UTC y las convierte de forma nativa a la hora local del navegador (ej. UTC-5 en Colombia).

### Corregido / Mejorado
- **Contraste de Colores Verdes en Modo Claro (`frontend/index.html` + `frontend/app.js`):** Reemplazados los tonos verdes claros por `text-emerald-950 font-bold` sobre el botón de Admin activo y en notificaciones Toast para garantizar legibilidad perfecta sobre fondo claro.
- **Hover Morado en Botones Secundarios (`frontend/index.html`):** Los botones "Admin Login" y "Limpiar formulario" incorporan un fondo morado suave traslúcido (`hover:bg-purple-900/10`) al pasar el cursor en modo claro.

---

## [1.8.0] — 2026-08-06 · Panel de Autenticación Admin, Tokens de Sesión y Eliminación de Consultas

### Añadido
- **Autenticación y Sesiones Admin en Microservicio FastAPI (`app/main.py`):**
  - Creado el endpoint `POST /auth/login` que recibe usuario y contraseña, valida credenciales con comparación de hash SHA-256 e inyecta un Token Bearer seguro (`secrets.token_hex(32)`) en `ACTIVE_TOKENS`.
  - Creado el endpoint `POST /auth/logout` para invalidación inmediata de tokens en el servidor.
  - Creado el endpoint protegido `DELETE /predicciones/{prediccion_id}` que requiere la cabecera `Authorization: Bearer <token>` para autorizar la eliminación de consultas.

- **Eliminación en Cascada en PostgreSQL (`app/database.py`):**
  - Implementada la función `delete_prediccion(prediccion_id: int)` que elimina de forma atómica y en cascada la predicción en la tabla `predicciones` y su correspondiente contenido en `contenidos`, incluyendo manejo explícito de `con.rollback()` ante cualquier excepción de base de datos.

- **Paridad en API REST Spring Boot (`backend/api/src/main/java/api/`):**
  - **Servicio:** Añadido el método `@Transactional public boolean eliminarPrediccion(Long prediccionId)` en `PrediccionService.java`.
  - **Controlador:** Expuesto el endpoint `@DeleteMapping("/{id}")` en `ContenidoController.java` para dar soporte a solicitudes de eliminación directa en el puerto 8080.

- **Panel de Login Admin, Menú Popover y Gestión Visual en Web UI (`frontend/`):**
  - **Header:** Botón **Admin Login** en la barra superior con indicador dinámico de estado (`🛡️ Admin (usuario)`).
  - **Modal de Login Centrado (`index.html` + `app.js`):** Interfaz modal Cyber AI Glassmorphism perfectamente centrada en pantalla para la autenticación de administradores con validación y alertas.
  - **Menú Desplegable Popover:** Al estar logueado como administrador, un clic sobre el botón abre un menú popover con información del usuario activo y el botón de acción **"🚪 Cerrar Sesión"**.
  - **Acceso Invitados:** Los usuarios sin autenticar mantienen el uso libre del clasificador e historial pero sin acceso a botones de borrado.
  - **Botones "🗑️ Borrar":** En las tarjetas e ítems del historial se renderizan condicionalmente los botones de eliminación cuando la sesión de administrador está activa, con alerta de confirmación y refresco en tiempo real del historial y los gráficos del Dashboard de Análisis.

- **Configuración Interactiva e Integración Docker (`setup.py`, `.env.example`, `docker-compose.yml`):**
  - **Setup Universal:** `setup.py` solicita interactivamente el usuario y contraseña del administrador en la primera ejecución y actualiza automáticamente `.env`.
  - **Docker Compose:** Propagadas las variables `ADMIN_USER`, `ADMIN_PASSWORD` y `JWT_SECRET` a los servicios de `fastapi` y `springboot`.

---

## [1.7.0] — 2026-08-04 · Dashboard de Análisis Gráfico y Estadísticas en Tiempo Real (Chart.js + PostgreSQL)

### Añadido
- **Función y Endpoint de Analytics (`app/database.py` + `app/main.py`):** Creado el módulo `get_analytics_data()` y el endpoint `GET /analytics` en FastAPI, que ejecuta consultas SQL optimizadas sobre la base de datos PostgreSQL para obtener:
  - **KPIs:** Total de predicciones registradas, categoría con mayor volumen de consultas y nivel promedio de confianza del modelo.
  - **Distribución por Categoría:** Conteo relativo entre las 8 categorías del sistema.
  - **Distribución Horaria (24h):** Actividad agrupada por hora del día (`EXTRACT(HOUR FROM created_at)`).
  - **Frecuencia de Keywords:** Ranking de las 15 palabras clave más comunes normalizadas a minúsculas y desduplicadas por documento.

- **Sección e Interfaz "Análisis" en la Web UI (`frontend/index.html` + `frontend/app.js`):**
  - **Navegación:** Agregado el nuevo botón **"Análisis"** (`analytics`) en la barra de navegación lateral (Sidebar) ubicado justo debajo de *Historial*.
  - **Librería de Gráficos:** Integración de **Chart.js 4.4+** vía CDN.
  - **KPI Cards:** 3 tarjetas superiores (*Total Clasificaciones*, *Categoría Líder*, *Confianza Promedio*) con iconografía neón.
  - **Visualizaciones Interactivas:**
    1. 🍩 **Doughnut Chart:** Distribución porcentual por categoría técnica.
    2. 📈 **Area Line Chart:** Curva de actividad de consultas a lo largo de las 24 horas del día.
    3. 🏷️ **Nube de Etiquetas (Tag Cloud de Badges/Pills):** Reemplazado el gráfico de barras por una rejilla compacta de pastillas neón interactivas con contador de frecuencia (`#keyword  count`), ahorrando más del 60% de espacio vertical.
  - **Compatibilidad de Tema:** Los gráficos adaptan dinámicamente sus colores, rejillas y etiquetas al cambiar entre *Modo Claro* y *Modo Oscuro*.

### Corregido / Mejorado
- **Refresco condicional/lazy de Analytics para conservar recursos (`frontend/app.js`):** La llamada a `loadAnalyticsDashboard()` tras una clasificación ahora verifica si la pestaña *"Análisis"* está activa. Si el usuario está en la vista del Clasificador, no realiza ninguna petición al servidor hasta que abra la pestaña.
- **Intervalo equilibrado de polling de métricas (`frontend/app.js`):** Ajustado el intervalo de consulta de `fetchSystemStats` a 10 segundos, logrando un equilibrio perfecto entre fluidez en tiempo real y conservación de recursos en la VM de OCI.
- **Evitado de caché en consultas de telemetría (`frontend/app.js`):** Agregado el parámetro de marcas de tiempo `?t=${Date.now()}` a las peticiones HTTP del dashboard para evitar que el navegador responda con datos cacheados.
- **Adaptación automática a la zona horaria del usuario (`app/database.py` + `frontend/app.js`):** El frontend detecta automáticamente el desfasaje horario del navegador (`new Date().getTimezoneOffset()`) y lo envía en el parámetro `tz_offset`. PostgreSQL desplaza el cálculo de `EXTRACT(HOUR FROM (created_at + interval))` para que la curva de actividad 24h muestre exactamente las horas locales de la región del usuario (ej: 16:00 hs en lugar de 19:00 hs UTC).
- **Filtro de conectores y adverbios genéricos (`app/main.py` + `app/database.py`):** Agregado el conjunto `RUIDO_CONECTORES` (*mediante, globalmente, además, través, según, principal, cada, etc.*) a las stopwords del pipeline NLP y a la agregación de analytics, asegurando que el ranking de palabras clave solo muestre conceptos y tecnologías puramente técnicas (*FastAPI, Docker, Spring Boot, PostgreSQL, JWT, etc.*).
- **Normalización estricta de palabras clave (`app/database.py`):** Removidos corchetes `[` `]` y comillas simples/dobles residuales en la columna `palabras_clave` de PostgreSQL antes de contabilizar frecuencias.

---

## [1.6.1] — 2026-08-04 · Métricas en Tiempo Real del Servidor OCI (CPU, RAM y Swap)

### Añadido
- **Endpoint de telemetría de hardware en FastAPI (`app/main.py`):** Creado el endpoint `GET /system-stats` respaldado por `psutil` (con fallback nativo a `/proc/meminfo` y `os.getloadavg()` en Linux), que expone métricas en tiempo real de consumo de CPU (%), RAM total/usada/disponible (MB), Swap (MB) y **tiempo de actividad del servidor (Uptime)**.
- **Widgets visuales de telemetría en el Frontend (`frontend/index.html` + `frontend/app.js`):** Expandido el popover *"Estado de servicios"* en la barra lateral (Sidebar) reemplazando la etiqueta fija con un badge dinámico de **Uptime** (`schedule`) y 3 barras de progreso animadas en estética *Cyber AI Dark Mode*:
  - ⏱️ **Badge de Uptime del servidor** (ej. `2d 4h 15m`).
  - 💻 **Carga de CPU** con porcentaje actualizado dinámicamente.
  - 🧠 **Consumo de RAM** con lectura de megabytes usados/totales y badge indicador de **RAM Libre**.
  - 🔄 **Consumo de Swap** con barra de capacidad.
  - **Polling en tiempo real:** Actualización automática cada 5 segundos.
  - **Código de colores reactivo:** Verde (RAM < 80%), Amarillo (RAM 80%-90%), Rojo (RAM > 90%).

---

## [1.6.0] — 2026-08-03 · Mejoras de Isotipo, Hover Unificado y Funciones de Historial

### Añadido
- **Botón "Ver más" / "Ver menos" en descripciones del Historial (`frontend/app.js`):** Agregada la capacidad de expandir y contraer descripciones extensas en las tarjetas de consulta tanto en el grid inicial como en la lista detallada.
- **Botón "Copiar JSON" por consulta en el Historial (`frontend/app.js`):** Cada entrada del historial incorpora su propio botón interactivo para copiar el objeto JSON completo de la consulta al portapapeles con feedback instantáneo (`¡Copiado!`) y notificación flotante.

### Corregido
- **Contraste y color del Isotipo de TechMind en Modo Claro (`frontend/index.html`):** Ajustados los tonos del isotipo (`psychology`) a morado violeta intenso (`text-purple-700 dark:text-primary`) y el nombre TechMind a `text-purple-950 dark:text-primary-fixed`, resolviendo la falta de contraste en el modo claro.
- **Hover unificado para Clasificador, Historial y Estado de servicios (`frontend/index.html` + `frontend/app.js`):** Creada la clase CSS `.sidebar-nav-item` que unifica el estilo hover para los 3 botones principales del sidebar con fondo violeta traslúcido, borde suave y elevación idéntica.

---

## [1.5.2] — 2026-08-03 · Optimización de `docker-compose.yml` para OCI Free Tier (1 vCPU · 1 GB RAM · 2 GB Swap)

### Mejorado
- **Límites de memoria por contenedor (`docker-compose.yml`):** Se agregaron `mem_limit` y `memswap_limit` a los cuatro servicios para prevenir que el OOM Killer del kernel mate procesos silenciosamente cuando la RAM se agota. El presupuesto total queda dentro del límite de 1 GB de RAM real, usando el swap de 2 GB como colchón ante picos de carga:

  | Servicio | `mem_limit` (RAM) | `memswap_limit` (RAM + Swap) |
  |---|---|---|
  | `postgres` | 150 MB | 300 MB |
  | `fastapi` | 220 MB | 440 MB |
  | `springboot` | 384 MB | 768 MB |
  | `frontend` | 48 MB | 96 MB |
  | **Total estimado** | **~982 MB** | **dentro del 1 GB** |

- **Límites de CPU por contenedor (`docker-compose.yml`):** Se agregó la directiva `cpus` a cada servicio para evitar que un solo contenedor monopolice el único vCPU disponible:
  - `postgres`: `0.25` (mayormente I/O)
  - `fastapi`: `0.50` (inferencia por request)
  - `springboot`: `0.50` (API transaccional)
  - `frontend`: `0.10` (Nginx estático)

- **Tuning de PostgreSQL para bajo consumo de RAM (`docker-compose.yml`):** Se agregó la directiva `command` con parámetros optimizados para entornos de 1 GB:
  - `shared_buffers=32MB` (reducido desde el default de 128MB)
  - `work_mem=4MB` (20 conexiones × 4MB = 80MB pico)
  - `maintenance_work_mem=32MB`
  - `effective_cache_size=128MB`
  - `max_connections=20` (suficiente para el pool de Spring Boot)
  - `wal_buffers=8MB`, `checkpoint_completion_target=0.9`

- **Uvicorn single-worker (`docker-compose.yml`):** Se sobreescribió el `command` del servicio `fastapi` para forzar `--workers 1`, evitando que Uvicorn spawne múltiples workers en una instancia de 1 vCPU. Se agregó `--limit-max-requests 500` para que el worker se reinicie periódicamente y libere posibles memory leaks de las librerías de ML.

- **Healthcheck más tolerante para PostgreSQL:** Se aumentó `start_period` de 0s a 20s para dar más tiempo de arranque a la base de datos en una instancia con I/O lenta (OCI Free Tier usa almacenamiento de bloque compartido).

---

## [1.5.1] — 2026-08-03 · Actualización del Notebook de Data Science (Alineación con Pipeline de Producción + Cross-Validation)

### Añadido / Mejorado
- **Ampliación del Dataset de Entrenamiento (`data-science/data/raw/contenidos_tecnicos.csv`):** Dataset expandido de ~221 a **259 registros técnicos balanceados** (+38 registros especializados), resolviendo ambigüedades y reforzando la precisión en las categorías **Mobile** (*SwiftUI, Jetpack Compose, Flutter Dart AOT, React Native Fabric, Kotlin KMP*) y **Cloud** (*AWS VPC, Lambda, S3, CloudFront, Terraform HCL, OCI Autonomous DB, FinOps*).
- **Ensamble de Modelos con Calibración de Confianza (`data-science/src/expand_and_train.py`):** Reemplazada la `LogisticRegression` individual por un ensamble `VotingClassifier` (Soft Voting) que combina 3 algoritmos complementarios:
  1. `LogisticRegression` con pesos de clase balanceados ($C=1.5$).
  2. `CalibratedClassifierCV(LinearSVC)` con calibración de probabilidades de Platt (`method='sigmoid'`), proporcionando estimaciones de confianza nítidas y precisas.
  3. `ComplementNB` optimizado para clasificación de textos.
- **Preprocesamiento y NLTK Stopwords (`data-science/src/expand_and_train.py` + `app/main.py`):** Integrado el corpus oficial de 154 stopwords en español de NLTK en el pipeline de entrenamiento e inferencia FastAPI, omitiendo además términos de ruido técnico neutro (*"tutorial"*, *"guia"*, *"ejemplo"*, *"introduccion"*).
- **Feature Engineering con TF-IDF Sublineal y N-Gramas 1-3 (`data-science/src/expand_and_train.py`):** Configurado `TfidfVectorizer` con `sublinear_tf=True` (escalado logarítmico de término $1 + \log(tf)$) y rango de n-gramas de 1 a 3 para capturar expresiones técnicas compuestas (*"aws lambda serverless"*, *"react native navigation"*).
- **Nuevos Artefactos `.joblib` (`data-science/models/`):** Generados los archivos binarios `tfidf_vectorizer.joblib` y `modelo_clasificador.joblib` manteniendo 100% la compatibilidad con los contratos de API de FastAPI y Spring Boot.
- **Incremento en Métricas de Rendimiento:** Alcanzado un **90.38% de Accuracy** en la evaluación holdout (20% test data), logrando un **100% de Precisión/Recall en Mobile** y un **94% de F1-Score en Cloud**.
- **Notebook reescrito para reflejar el pipeline de producción actual (`data-science/notebooks/TechMind_DataScience.ipynb`):** El notebook estaba desactualizado respecto a `expand_and_train.py` — mostraba 61 registros, usaba un `TfidfVectorizer` básico (1-2 n-gramas, 1500 features) y un `LogisticRegression` individual. Se reescribió completo (de 64 celdas dispersas a 40 celdas consolidadas y documentadas) para reflejar fielmente el pipeline de producción:
  - Carga dinámica del CSV mostrando **259 registros** reales.
  - Concatenación de `titulo + texto` en el preprocesamiento (alineado con la mejora del ensamble).
  - `TfidfVectorizer` sublineal con n-gramas 1-3 y 6 000 features (idéntico a `expand_and_train.py`).
  - **Ensamble Calibrado** (`LogisticRegression` + `CalibratedClassifierCV(LinearSVC)` + `ComplementNB`) con soft voting.
  - Todos los gráficos (distribución de categorías, longitud de textos, confusion matrix) regenerados con los 259 registros actuales.
  - Compatibilidad total con nbformat 4.5 (campo `id` en cada celda).
- **Validación Cruzada Estratificada K-Fold (K=5) (`data-science/notebooks/TechMind_DataScience.ipynb`):** Nueva sección 9 que usa el **100% de las muestras** para evaluar el modelo, eliminando la dependencia de un único corte de datos. Implementada con un `Pipeline(TF-IDF → Ensamble)` correcto que re-fitea el vectorizador en cada fold para evitar *data leakage*. Resultados obtenidos:
  - Accuracy promedio CV: **87.28% ± 4.11%**
  - Rango: [80.77% – 92.16%]
  - Gráfico de barras por fold incluido.

### Corregido
- **Porcentajes de Confianza con decimales y punto sobrante (`frontend/index.html` + `frontend/app.js`):** Eliminadas las cifras decimales en la "Confianza del Modelo" tanto en el marcador principal (`0%`) como en los registros del historial reciente y la vista detallada (`Math.round(prob * 100)`).
- **Legibilidad del mensaje de error de BD en Modo Claro (`frontend/app.js`):** Actualizados los estilos en el bloque `catch` del historial para que las alertas de error de conexión a la base de datos se muestren en un color rojo oscuro bien definido (`text-rose-700 dark:text-rose-200`) y con alto contraste sobre fondo claro.
- **Resplandor y deslumbre del Modo Claro (`frontend/index.html`):** Redefinidas las variables CSS `:root` hacia un diseño cálido cremita/arena mate (`#e8e2d5` y `#eee7d9`) con tipografía en tono café/carbón profundo (`#231f18`), eliminando la iluminación blanca cegadora de fondo e inputs.
- **Parpadeo de cambio de fuente / FOUT (`frontend/index.html`):** Al cargar la aplicación, se percibía un breve intercambio o parpadeo (*font swap*) debido a la directiva `display=swap` en Google Fonts. Resuelto precargando la hoja de estilos (`rel="preload"`) y cambiando el parámetro a `display=block` para que el texto se renderice directamente en la tipografía definitiva (`Inter` / `Outfit`) desde el primer instante sin ningún parpadeo.
- **Ícono de estrellas en etiqueta de Confianza (`frontend/app.js`):** Eliminado el ícono de estrellas (`auto_awesome` ✨) posicionado al lado de la etiqueta "Confianza: %" en las tarjetas del historial.
- **Efecto borroso en el Sidebar Móvil (`frontend/index.html`):** Eliminadas las clases `backdrop-blur-sm` y `backdrop-blur-2xl` en el overlay y panel de navegación lateral para evitar distorsiones al abrir el menú en dispositivos móviles.
- **Ortografía y formato en textos del sistema (`frontend/index.html` + `frontend/app.js`):** Corregidos acentos, minúsculas tras comas o inicios de descripciones y estandarización ortográfica.

### Añadido
- **Notificación de alerta cuando faltan campos al clasificar (`frontend/app.js`):** Al presionar el botón de clasificación con campos vacíos, se despliega la alerta con el mensaje exacto `Por favor, llena todos los campos`. Ante errores de conexión o servidor, se mantiene el mensaje `Hubo un error, por favor intenta de nuevo más tarde`.
- **Navegación al inicio mediante el logo TechMind (`frontend/index.html` + `frontend/app.js`):** El elemento de marca "TechMind" en el sidebar redirige al usuario de vuelta a la vista principal (Home/Clasificador) al hacer clic.

### Decisión de Arquitectura
- `expand_and_train.py` permanece como **fuente de verdad de producción** (genera los artefactos `.joblib` para la API FastAPI).
- El notebook actúa como **documentación viva y reproducible** del mismo pipeline, enriquecida con Cross-Validation como capa adicional de análisis para presentación.

---

## [1.3.2] — 2026-07-31 · Estabilidad en OCI (memoria, devtools y auto-restart)

### Corregido

- **`backend/Dockerfile` — JVM sin límite de heap → OOM Killer del kernel:** Spring Boot corría sin flags `-Xmx`, por lo que la JVM podía crecer hasta consumir toda la RAM del servidor. En el OCI Free Tier (1 GB RAM), después de unas horas el kernel de Linux terminaba el proceso silenciosamente mediante el OOM Killer, dejando el servicio en rojo sin ningún error explícito en los logs de Docker. Corregido añadiendo `-Xms64m -Xmx256m -XX:+UseSerialGC` al `ENTRYPOINT`, limitando el heap máximo a 256 MB y usando el GC serie (más eficiente en CPUs de 1–2 núcleos).

- **`backend/api/pom.xml` — `spring-boot-devtools` activo en producción:** La dependencia `spring-boot-devtools` tenía `<scope>runtime</scope>`, lo que hacía que se incluyera en el JAR final y se activara dentro del contenedor Docker, monitoreando el filesystem en busca de cambios y reiniciando la aplicación innecesariamente, consumiendo CPU y RAM de forma continua. Cambiado a `<scope>test</scope>` para excluirlo del artefacto de producción. El comportamiento en desarrollo local (IntelliJ / VS Code) no se ve afectado.

- **`docker-compose.yml` — contenedores sin política de reinicio:** Ningún servicio tenía definida la directiva `restart`, por lo que si un contenedor crasheaba (por OOM u otro error) quedaba detenido permanentemente hasta intervención manual. Añadido `restart: unless-stopped` a los cuatro servicios (`postgres`, `fastapi`, `springboot`, `frontend`) para garantizar auto-recovery automático ante fallos y arranque automático tras un reinicio de la VM.

---

## [1.3.1] — 2026-07-30 · Compatibilidad Docker Compose v2

### Corregido
- **`setup.py` — migración de `docker-compose` (v1) a `docker compose` (v2):** El script de setup usaba el binario standalone `docker-compose` (Docker Compose v1, deprecado desde 2023), que no está disponible en instalaciones modernas de Docker Engine. En servidores con Docker Compose v2 instalado como plugin, los comandos fallaban con error de comando no encontrado. Se reemplazaron las 6 llamadas afectadas:
  - `docker compose up -d postgres`
  - `docker compose --profile full up -d --build`
  - `docker compose --profile full down`
  - `docker compose --profile full down -v` (ejecución + mensajes de ayuda)

  El comando `docker compose` (sin guión) es compatible con Windows (Docker Desktop), macOS (Docker Desktop) y Linux (Docker Engine 20.10+), por lo que el cambio es transparente en todos los entornos.

---

## [1.3.0] — 2026-07-30 · Mejoras de UX en Clasificador

### Corregido
- **Ícono duplicado en sidebar (`frontend/index.html`):** El enlace de navegación "Clasificador" usaba el mismo ícono `psychology` que el logo principal "TechMind" en la parte superior del sidebar, generando confusión visual. Reemplazado por el ícono `category` de Material Symbols para diferenciar claramente ambos elementos.
- **Decimales excesivos en probabilidad (`app/database.py` + `frontend/app.js`):** Los valores de probabilidad devueltos por el modelo ML se mostraban con hasta 4 decimales. Se aplica `round(float, 2)` en la API Python (`get_predicciones`) y `Math.round` en el frontend antes de renderizar. El porcentaje de confianza en la UI se muestra con 2 decimales.
- **Efecto de brillo blanco/púrpura sobre el panel de resultados (`frontend/index.html`):** Eliminado el `<div>` con clase `bg-primary-fixed blur-md` posicionado en la esquina superior derecha del recuadro "Resultado del Análisis", que generaba un resplandor no deseado sobre el borde superior del panel.

### Mejorado
- **Limpieza automática de campos tras clasificar (`frontend/app.js`):** Al hacer clic en "Clasificar con TechMind" y recibir una respuesta exitosa, los campos de título y contenido se vacían automáticamente, preparando la interfaz para una nueva consulta sin necesidad de borrar manualmente el texto anterior.
- **Descripción del contenido visible en historial (`app/database.py` + `frontend/app.js`):** La consulta SQL del endpoint `GET /predicciones` ahora incluye el campo `c.texto` de la tabla `contenidos`. El frontend muestra el texto/descripción truncado (con `line-clamp-2`) debajo del título tanto en las tarjetas recientes del clasificador como en la subpágina de historial detallado.

---

## [1.2.0] — 2026-07-30 · Health Check de Spring Boot + Actuator

### Corregido
- **Bug visual en la UI — indicador LED de Spring Boot siempre en rojo (`frontend/app.js`):** El health check usaba `fetch('/contenido', { method: 'OPTIONS' })` para detectar si Spring Boot estaba activo. El browser bloqueaba esta llamada por política CORS al tratarla de forma distinta a un preflight automático, lanzando siempre el bloque `catch` y mostrando el LED en rojo aunque el servidor estuviera operativo y la clasificación funcionara correctamente. Corregido reemplazando el método `OPTIONS` por `GET /actuator/health`, consistente con el patrón ya aplicado para FastAPI.
- **Redundancia y UX en Modal JSON de Inferencia (`frontend/index.html` y `frontend/app.js`):** Se eliminó el botón redundante "Cerrar" en la barra inferior del modal. Se habilitó el cierre nativo mediante el botón "X" en la barra superior, click en el fondo oscuro (backdrop) y presionado de la tecla `Escape`.

### Añadido
- **Botón "Copiar JSON" en Modal de Inferencia (`frontend/index.html` y `frontend/app.js`):** Reemplazado el pie del modal con una acción de exportación interactiva que copia todo el payload JSON (entrada + resultado) al portapapeles con feedback animado de 2 segundos ("¡Copiado!") y notificación Toast.

### Añadido
- **`spring-boot-starter-actuator` en `backend/api/api/pom.xml`:** Nueva dependencia que expone el endpoint estándar `GET /actuator/health` con respuesta `{ "status": "UP" }` cuando el servicio está operativo.
- **Configuración de Actuator en `backend/api/api/src/main/resources/application.properties`:**
  - `management.endpoints.web.exposure.include=health` — solo expone el endpoint de salud (no métricas ni información sensible).
  - `management.endpoint.health.show-details=never` — respuesta mínima sin detalles internos.
  - `management.endpoints.web.cors.allowed-origins=*` y `allowed-methods=GET` — permite que el frontend consulte el endpoint sin errores de CORS.

### Documentación
- **`backend/docs/ARQUITECTURA.md`:** Actualizados el bloque de `application.properties` con las nuevas propiedades de Actuator, el flujo de arranque (ahora lista los dos endpoints expuestos en `:8080`) y agregada la nueva sección *"Endpoint de Health Check"* con contrato JSON.
- **`backend/docs/FUNCIONALIDADES.md`:** Título actualizado a *"Endpoints Disponibles"* (plural). Agregada sección `GET /actuator/health` con contrato completo, descripción de uso y contexto de integración con el frontend.
- **`backend/docs/SETUP.md`:** Health check básico corregido (de `curl /contenido` a `curl /actuator/health`). Agregada entrada en Troubleshooting: *"El indicador de Spring Boot aparece en rojo en la UI"* con causa, verificación y solución.
- **`frontend/README.md`:** Indicadores de estado detallados con el endpoint exacto que cada servicio usa para su health check.

---

## [1.1.0] — 2026-07-28 · Sprint 2 & QA Automation (anterior)

### Añadido
- **Diagrama Infográfico de Arquitectura de Sistema:** Generado e integrado en `README.md` (`assets/techmind_project_flow.png`) mostrando el flujo visual multicontenedor (Frontend UI → Spring Boot :8080 → FastAPI ML :8000 → PostgreSQL 16 :5432).
- **Suite de Pruebas Automatizadas de QA (Sprint 2):** Creada e implementada suite de 14 casos de prueba E2E cubriendo flujos felices, límites de carga, resistencia a inyección SQL/XSS, resiliencia y validación de tipos HTTP (reporte en `qa/reportes/resultados-sprint-2.md`).
- **Documentación del Esquema Relacional de PostgreSQL:** Creado informe técnico completo (`informe_base_de_datos.md`) con diagrama Entidad-Relación (ER) Mermaid, contratos DDL, índices y mapeo JPA.

### Corregido
- **Eliminación de la llamada redundante `log_prediccion()` en FastAPI (`app/main.py` y `app/database.py`):** Solucionado el error de log en PostgreSQL (`null value in column "contenido_id" violates not-null constraint`). FastAPI opera ahora como un microservicio 100% stateless mientras Spring Boot administra la transacción y asignación de `contenido_id`.

---

## [0.6.0] — 2026-07-22 · Bug Fixes + Corrección de rutas del modelo

### Corregido
- **Bug crítico en `app/main.py` — endpoint `POST /predecir`:** la variable `probabilidad` nunca se calculaba antes de ser usada en `log_prediccion()`, lo que causaba un `NameError` en runtime. Se agregó el cálculo correcto usando `modelo.predict_proba(vector)[0].max()` antes de la llamada a la función de logging.
- **Rutas de serialización en `TechMind_DataScience.ipynb`:** las celdas de `joblib.dump()` y `joblib.load()` usaban rutas relativas simples (`"tfidf_vectorizer.joblib"`, `"modelo_clasificador.joblib"`) que guardaban los artefactos en el directorio de trabajo del kernel (`data-science/notebooks/`), no en `data-science/models/` donde FastAPI los busca. Se corrigieron las rutas a `"../models/tfidf_vectorizer.joblib"` y `"../models/modelo_clasificador.joblib"`.
- **Esquema PostgreSQL — tabla `predicciones`:** la columna fue creada por el script de migración (`migrate_to_postgres.py`) con el nombre `keywords` en lugar de `informaciones_adicionales`, lo que causaba un error silencioso al intentar persistir cada predicción. Corregido en dos pasos: (1) `ALTER TABLE` sobre la DB existente y (2) corrección del nombre en el `SCHEMA_SQL` del script de migración para que instalaciones nuevas también queden correctas.

### Verificado
- Pipeline completo probado end-to-end: `POST /predecir` → clasificación → persistencia en PostgreSQL sin errores.
- Los modelos `.joblib` ahora se generan directamente en `data-science/models/` al ejecutar el notebook.

---

## [0.5.0] — 2026-07-21 · Ingesta de Documentos + Re-entrenamiento Automático

### Añadido
- **Script de ingesta interactiva** (`ingest_documents.py`) que permite importar archivos PDF (`pdfplumber`) y DOCX (`python-docx`) a PostgreSQL.
  - Soporta la extracción y limpieza automatizada de texto.
  - Permite etiquetar manualmente la categoría (Opción A) en una interfaz CLI interactiva con preview de texto.
  - Detección de secciones para documentos multi-categoría, permitiendo split y etiquetado independiente por sección.
  - Control de duplicados mediante verificación del hash MD5 del contenido en la base de datos.
- **Re-entrenamiento automático local**: el script de ingesta cuenta con un trigger automático que detecta si se han importado 3 o más documentos en una sola sesión y ofrece ejecutar el notebook mediante Jupyter (`jupyter nbconvert --execute`) en segundo plano para regenerar los modelos `.joblib`.
- **Nueva guía de ingesta** (`INGESTA_DOCUMENTOS.md`) detallando la preparación de documentos, flujo de ejecución, Edge Cases y solución de problemas.
- **Guía de entrega de Backend** (`ENTREGA_BACKEND.md`) para facilitar al equipo Java qué archivos deben clonarse (código, docker, docs) y cuáles compartirse manualmente (modelos `.joblib` en `.gitignore`).
- **Plan y suite de pruebas para QA** (`QA_TESTING.md` y `postman_collection.json`) con 23 casos de prueba para validar Happy Paths, Edge Cases, Error Handling y performance contra el endpoint local.

### Cambiado
- **`requirements.txt`** — agregadas dependencias para procesamiento de documentos: `pdfplumber>=0.11.0` y `python-docx>=1.1.0`.
- **`.gitignore`** — modificado para excluir archivos locales PDF y DOCX en la carpeta `documentos/` (`documentos/*.pdf` y `documentos/*.docx`) y mantener solo la carpeta usando `.gitkeep`.
- **`README.md`** — tabla de documentación actualizada con los nuevos entregables (`ENTREGA_BACKEND.md`, `QA_TESTING.md`, `INGESTA_DOCUMENTOS.md` y `postman_collection.json`).

---

## [0.4.0] — 2026-07-21 · FastAPI + PostgreSQL

### Añadido
- **Microservicio FastAPI** (`app/main.py`) con tres endpoints:
  - `POST /predecir` — inferencia interna consumida por Spring Boot. Carga los `.joblib` al arrancar, clasifica el texto y persiste la predicción en PostgreSQL.
  - `GET /health` — health check para que Spring Boot verifique disponibilidad antes de llamar.
  - `GET /categorias` — devuelve la lista de las 8 categorías del modelo.
  - `GET /docs` — documentación Swagger automática generada por FastAPI.
- **Módulo de base de datos** (`app/database.py`) con `get_connection()`, `init_db()` y `log_prediccion()` para PostgreSQL.
- **Script de migración a PostgreSQL** (`migrate_to_postgres.py`) — crea las tablas `contenidos` y `predicciones`, lee desde SQLite o CSV, e incluye confirmación interactiva para evitar reemplazos accidentales.
- **Tabla `predicciones`** en PostgreSQL — log automático de cada inferencia con `titulo`, `texto`, `categoria`, `probabilidad`, `informaciones_adicionales` y `created_at`.
- **`docker-compose.yml`** — levanta PostgreSQL 16 localmente con un solo comando (`docker-compose up -d`). Incluye health check y volumen persistente.
- **`.env.example`** — plantilla de variables de entorno para Python (FastAPI) y referencia para Spring Boot.
- **`.gitignore`** — excluye `.env`, `*.joblib`, `techmind.db` y archivos de Python/Jupyter del repositorio.
- **`BACKEND_INTEGRATION.md`** — guía completa para el equipo de Java/Spring Boot: setup, contrato del endpoint `/predecir`, ejemplos de código Java (`RestTemplate` y `WebClient`), configuración de `application.properties`, schema SQL y checklist de verificación.

### Cambiado
- **`requirements.txt`** — agregados `fastapi>=0.111.0`, `uvicorn[standard]>=0.29.0`, `psycopg2-binary>=2.9.9`, `python-dotenv>=1.0.0`.
- **`TechMind_DataScience.ipynb` — Celda 3** — modo dual: si `PG_HOST` está configurado carga desde PostgreSQL; si no, hace fallback a SQLite local (retrocompatible).

### Arquitectura
```
Postman → Spring Boot (8080) → FastAPI (8000) → PostgreSQL (5432)
                     └─────────────────────────────────────────────┘
```

---

## [0.3.0] — 2026-07-17 · Migración de base de datos a SQLite

### Añadido
- **Base de datos SQLite** `techmind.db` — migración del dataset original `contenidos_tecnicos.csv` a una base de datos relacional embebida. La tabla `contenidos` incorpora dos campos nuevos respecto al CSV:
  - `id` — clave primaria autoincremental, necesaria para que el Back-End pueda referenciar registros individuales.
  - `created_at` — timestamp UTC de inserción, útil para auditoría y reentrenamiento incremental.
- **Script de migración** `migrate_to_sqlite.py` — script Python reutilizable (sin dependencias externas, solo stdlib) que: lee el CSV → crea el esquema → importa los 61 registros → verifica la distribución por categoría → imprime ejemplos de carga. Puede volver a ejecutarse en cualquier momento para regenerar la DB desde cero.
- **Índice sobre `categoria`** (`idx_categoria`) — mejora el rendimiento de consultas por categoría, especialmente relevante cuando el dataset crezca.

### Cambiado
- **Notebook `TechMind_DataScience.ipynb` — Celda 3**: la carga del dataset se migró de `pd.read_csv("contenidos_tecnicos.csv")` a `pd.read_sql_query(...)` sobre `techmind.db`. El resto del pipeline (preprocesamiento, vectorización, modelo, serialización) no requirió cambios.

### Por qué SQLite
- Permite al Back-End consultar, insertar y filtrar contenidos sin parsear un CSV manualmente.
- Soporta queries SQL estándar (`SELECT`, `INSERT`, `WHERE categoria = ?`) directamente desde Java (JDBC) o Python.
- Es un archivo único (`techmind.db`) — no requiere servidor, fácil de subir a OCI Object Storage.
- La tabla queda preparada para recibir nuevos registros vía `POST /contenido` sin necesidad de reescribir el archivo CSV.

---

## [0.2.0] — 2026-07-15 · MVP del Hackathon

### Añadido
- **Pipeline de inferencia end-to-end** — función `procesar_contenido(titulo, texto)` que encadena limpieza → vectorización → clasificación → extracción de keywords y devuelve un dict JSON-serializable listo para el contrato REST.
- **Extracción de palabras clave** (campo `informaciones_adicionales`) mediante los términos con mayor peso TF-IDF dentro del documento individual, desacoplada de la predicción de categoría.
- **Tres ejemplos de uso documentados** en el notebook (Backend / Data Science / DevOps) como requisito obligatorio del MVP.
- **Serialización de artefactos** — `tfidf_vectorizer.joblib` y `modelo_clasificador.joblib` guardados con `joblib`, más celda de validación de carga que simula el arranque de la API.
- **Notas de integración** en la última sección del notebook (Celda 28): pasos para subir a OCI Object Storage y opciones de arquitectura (microservicio Python vs. exportación al formato Java).
- **Contrato de respuesta acordado** — campo renombrado a `informaciones_adicionales` (plural) para alinear con el equipo de Back-End:
  ```json
  {
    "categoria": "Backend",
    "probabilidad": 0.2779,
    "informaciones_adicionales": ["boot", "spring boot", "spring", "creación apis", "java spring"]
  }
  ```

### Cambiado
- El campo de salida originalmente denominado `informacion_adicional` (singular, según el PDF de la consigna) fue renombrado a `informaciones_adicionales` (plural) para coincidir con el contrato que usa el equipo de Back-End.

---

## [0.1.0] — 2026-07-14 · Construcción del pipeline base

### Añadido
- **Dataset sintético** `contenidos_tecnicos.csv` — ~60 registros en español, con campos `titulo`, `texto` y `categoria`, repartidos en 8 categorías: Backend, Frontend, Data Science, DevOps, Mobile, Bases de Datos, Seguridad y Cloud.
- **EDA inicial** — gráfico de distribución de categorías (countplot), histograma de longitud de textos (en palabras), chequeo de nulos y filas duplicadas.
- **Preprocesamiento de texto** — función `limpiar_texto(texto)`: minúsculas → remoción de puntuación (regex) → filtrado de stopwords en español (lista propia de ~30 términos, incluidos frases funcionales como "se explica", "se presenta").
- **Vectorización TF-IDF** — `TfidfVectorizer` con `max_features=1500`, `ngram_range=(1, 2)` y `min_df=1` para capturar unigramas y bigramas (p. ej. "api rest", "machine learning").
- **Modelo de clasificación** — Regresión Logística con `class_weight="balanced"` y `max_iter=1000`, entrenada sobre split train/test estratificado (75/25, `random_state=42`).
- **Evaluación del modelo** — accuracy, `classification_report` por categoría (precision / recall / F1) y matriz de confusión (heatmap con Seaborn).
  - Accuracy reportado sobre el test set actual: **~0.69** (orientativo; refleja las limitaciones del dataset pequeño).
  - Categorías con peor generalización: **DevOps** y **Seguridad** (menos ejemplos de entrenamiento).

---

## [0.0.1] — 2026-07-13 · Scaffolding inicial

### Añadido
- Estructura base del notebook `TechMind_DataScience.ipynb` con secciones enumeradas (EDA → Preprocesamiento → Vectorización → Modelo → Evaluación → Keywords → Inferencia → Serialización).
- Definición del alcance y rol del componente de Ciencia de Datos dentro del equipo (ver `detalle_trabajo.md`).
- Primeras dependencias identificadas: `pandas`, `scikit-learn`, `matplotlib`, `seaborn`, `joblib`, `re`, `json`, `numpy`.

---

*Mantenido por el equipo completo — TechMind G9 LATAM Team 37. Última actualización: 2026-08-08.*
