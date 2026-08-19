# 🎤 Guion y Estructura de Presentación de 5 Minutos — TechMind

> **Hackathon G9 LATAM · Equipo 37**  
> **Proyecto:** TechMind — Organización Inteligente del Conocimiento Técnico  
> **Duración Total:** 5 minutos (300 segundos)  
> **Objetivo:** Presentar el problema, la solución, la arquitectura técnica, la demo en vivo, el aseguramiento de calidad (QA) y el impacto del proyecto de forma clara, persuasiva y profesional.

---

## ⏱️ Distribución del Tiempo (Timeline)

```
[0:00 - 0:45] ➔ Slide 1: Introducción, El Problema y la Solución (45s)
[0:45 - 1:45] ➔ Slide 2: Demo en Vivo / Flujo de Usuario & UI Cyber AI (60s)
[1:45 - 3:00] ➔ Slide 3: Arquitectura de Microservicios & Modelo de ML NLP (75s)
[3:00 - 4:00] ➔ Slide 4: Aseguramiento de Calidad (QA), Auto-Healing & DevOps (60s)
[4:00 - 5:00] ➔ Slide 5: Equipo de Trabajo, Impacto & Cierre (60s)
```

---

## 📌 Ficha Técnica del Proyecto

- **Categoría:** Inteligencia Artificial / NLP / Desarrollo Fullstack.
- **Frontend:** HTML5, JavaScript Vanilla (ES6+), TailwindCSS (Diseño *Cyber AI* con Modo Oscuro/Claro e Internacionalización i18n ES/EN), Nginx Alpine.
- **Backend API:** Java 17 LTS, Spring Boot 4.x, Spring Data JPA / Hibernate, Flyway Migrations.
- **Microservicio ML:** Python 3.12, FastAPI, Scikit-Learn (TF-IDF + Ensamble Calibrado Soft Voting), Pandas, NumPy, Joblib.
- **Base de Datos:** PostgreSQL 16.
- **Infraestructura & DX:** Docker & Docker Compose, Script Orquestador Auto-Healing (`setup.py`).
- **Métricas del Modelo ML:** **87.28%** Accuracy en Validación Cruzada (K=5) y **90.38%** en Holdout test.

---

## 🚀 Guion Hablado Minuto a Minuto (Pitch Script)

### ⏱️ Minuto 0:00 - 0:45 | Bloque 1: El Problema y la Solución

**[Visual Sugerida: Diapositiva 1 / Portada con Logo de TechMind]**

> **🗣️ Guion Hablado (45 segundos):**  
> *"Buenas tardes a todos. ¿Cuántas veces en sus equipos de desarrollo o comunidades técnicas han perdido tiempo clasificando manualmente artículos, documentación o fragmentos de código para organizarlos en su base de conocimiento?*  
>  
> *Para resolver esta ineficiencia nace **TechMind**, una plataforma web inteligente diseñada para la **organización y clasificación automatizada de contenido técnico en tiempo real**.*  
>  
> *Con solo ingresar el título y el cuerpo de cualquier texto técnico, TechMind procesa el contenido mediante un pipeline de Procesamiento de Lenguaje Natural (NLP) y en cuestión de milisegundos entrega: la categoría temática exacta, un porcentaje de confianza calibrado y las palabras clave más representativas."*

---

### ⏱️ Minuto 0:45 - 1:45 | Bloque 2: Demostración en Vivo (Demo & UX)

**[Visual Sugerida: Pantalla del Frontend `http://localhost:5173` o Video de la UI]**

> **🗣️ Guion Hablado (60 segundos):**  
> *"Pasemos a ver la plataforma en acción.*  
>  
> *Nuestra interfaz fue construida con una estética **Cyber AI Dark Mode**, pensada para desarrolladores, con soporte completo para modo claro y un **sistema de internacionalización nativo en Español e Inglés (i18n)**.*  
>  
> *1. **Clasificación en tiempo real:** Si ingresamos un artículo como 'Inyección de dependencias en Spring Boot', hacemos clic en clasificar y observamos cómo el modelo identifica inmediatamente la categoría **Backend**, calcula un **88.8% de confianza** y extrae keywords clave como `spring boot`, `java` y `autowired`.*  
> *2. **Historial Persistente:** Todas las predicciones se almacenan en tiempo real en PostgreSQL. Desde la pestaña de Historial podemos filtrar por categorías, buscar texto en tiempo real y consultar el payload JSON completo.*  
> *3. **Panel de Analytics:** Contamos con visualizaciones dinámicas en Chart.js con la distribución de contenidos, tendencias y nivel de confianza promedio de la plataforma."*

---

### ⏱️ Minuto 1:45 - 3:00 | Bloque 3: Arquitectura Técnica & Machine Learning

**[Visual Sugerida: Diapositiva de Arquitectura Multicapa & Diagrama de Flujo]**

> **🗣️ Guion Hablado (75 segundos):**  
> *"Por detrás de la experiencia de usuario se encuentra una **arquitectura desacoplada y escalable de microservicios en contenedores Docker**:*  
>  
> *- **Backend Transaccional en Spring Boot (Java 17):** Actúa como API Gateway y capa de negocio, utilizando JPA para persistencia y Flyway para control de versiones de la base de datos.*  
> *- **Microservicio de Data Science en FastAPI (Python 3.12):** Expone un endpoint de inferencia `/predecir` ultra veloz.*  
> *- **Modelo de Machine Learning:** Implementa una vectorización TF-IDF sublineal de 6.000 características con n-gramas (1 a 3), combinada con un **Ensamble Calibrado (Soft Voting)** que integra Regresión Logística, Support Vector Machines (LinearSVC calibrado) y Naive Bayes Complementario.*  
>  
> *Gracias a esta arquitectura alcanzamos un **87.28% de precisión en Validación Cruzada (K=5)** y un **90.38% en prueba Holdout**, garantizando clasificaciones precisas y confiables entre 8 categorías técnicas distintas."*

---

### ⏱️ Minuto 3:00 - 4:00 | Bloque 4: Aseguramiento de Calidad (QA), Auto-Healing y Despliegue

**[Visual Sugerida: Diapositiva de Calidad / Cobertura QA / Docker / CLI]**

> **🗣️ Guion Hablado (60 segundos):**  
> *"Un aspecto diferencial de TechMind es nuestro enfoque en **Calidad de Software y Experiencia de Desarrollo (DX)**:*  
>  
> *- **QA Riguroso:** Durante 4 Sprints de desarrollo, nuestro equipo de QA ejecutó matrices de casos de prueba v4.0, validaciones de API en Swagger y seguimiento continuo en matriz de bugs.*  
> *- **Auto-Healing Orchestrator (`setup.py`):** Creamos un instalador multiplataforma capaz de verificar el entorno, entrenar modelos faltantes en segundos, gestionar la base de datos y autorecuperar servicios si se detecta alguna falla.*  
> *- **Despliegue Multi-Contenedor:** Toda la solución (Frontend, Spring Boot, FastAPI y PostgreSQL) se despliega con un solo comando mediante Docker Compose, lista para ser alojada en nubes como Oracle Cloud Infrastructure (OCI)."*

---

### ⏱️ Minuto 4:00 - 5:00 | Bloque 5: Equipo de Trabajo, Impacto y Cierre

**[Visual Sugerida: Diapositiva del Equipo 37 & Contacto / Cierre]**

> **🗣️ Guion Hablado (60 segundos):**  
> *"Todo esto fue posible gracias al **Equipo 37 del Hackathon G9 LATAM**, conformado por 8 integrantes trabajando de manera coordinada en Data Science, Backend Java, QA y Frontend UI/UX:*  
>  
> *- **Ernesto Llampa & Leandro Villamil & Rómulo García** en Data Science, ML y Fullstack.*  
> *- **Sergio Vilte, Andrés Rojas, Noelia Rementeria & Camila Fagina** en Backend Java y Spring Boot.*  
> *- **Federico Gutierrez** liderando la estrategia de Quality Assurance (QA).*  
>  
> *TechMind no es solo una prueba de concepto: es una **herramienta lista para integrarse vía API REST** en plataformas e-learning, gestores de conocimiento corporativo y comunidades dev.*  
>  
> *¡Muchas gracias por su atención! Quedamos abiertos a sus preguntas."*

---

## 📊 Resumen Estructurado para Diapositivas (Slides Outline)

Si vas a acompañar la charla con una presentación visual (PowerPoint, Keynote, Canvab o Google Slides), utilizá estas 5 diapositivas:

| # | Título de la Slide | Contenido Visual Principal | Frase Clave / Key Message |
|---|-------------------|----------------------------|---------------------------|
| **1** | **TechMind: Inteligencia Técnica** | Logo de TechMind, 8 Badges de Categorías | *"De texto no estructurado a conocimiento categorizado en milisegundos."* |
| **2** | **Demostración en Vivo** | Captura / Gif interactivo de la UI (Dark/Light + i18n) | *"Clasificación, probabilidad de confianza y keywords al instante."* |
| **3** | **Arquitectura & ML Pipeline** | Diagrama de bloques (Frontend ➔ Spring Boot ➔ FastAPI ➔ Postgres) | *"Soft Voting Ensemble + TF-IDF: 90.38% de precisión en Holdout."* |
| **4** | **Calidad, QA & Deployment** | Matriz QA, Logs de Docker y `python setup.py --docker` | *"Zero setup friction: Auto-healing y despliegue en 1 solo comando."* |
| **5** | **Equipo 37 & Escalabilidad** | Foto/Tabla del equipo multidisciplinario | *"Una API REST universal para la gestión del conocimiento técnico."* |

---

## 🧠 Cheat Sheet de Respuestas Rápidas (FAQ del Jurado)

Ante eventuales preguntas al finalizar la exposición de 5 minutos:

1. **¿Por qué eligieron un Ensamble Calibrado (Soft Voting)?**
   - *Respuesta:* Porque combina la capacidad lineal de Logistic Regression, la separación marginal de SVM y el manejo del desbalance de ComplementNB. Además, la calibración de probabilidades nos da una métrica real de confianza, no solo una predicción dura.

2. **¿Cómo se realiza la integración entre Java y Python?**
   - *Respuesta:* El backend Spring Boot expone la API pública REST y consume internamente la API de FastAPI mediante clientes HTTP asíncronos. Esto separa el dominio transaccional de la inferencia ML.

3. **¿Cómo manejan la persistencia y migraciones?**
   - *Respuesta:* PostgreSQL 16 maneja las tablas de contenidos y predicciones, y Flyway ejecuta las migraciones SQL automáticas al arrancar Spring Boot.

4. **¿El sistema soporta varios idiomas en la UI?**
   - *Respuesta:* Sí, la interfaz cuenta con un diccionario i18n nativo con 67 claves traducidas al español e inglés, persistiéndose la preferencia del usuario en `localStorage`.

---

> 📝 **Nota para el presentador:** Recordá mantener un ritmo pausado pero firme, destinar exactamente 1 minuto a la demo en vivo y mostrar entusiasmo por la integración de tecnologías (Java + Python + Docker + QA). ¡Éxitos en la presentación!
