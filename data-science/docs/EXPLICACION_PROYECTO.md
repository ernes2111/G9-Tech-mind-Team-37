# 🧠 TechMind — Explicación del Proyecto

> **¿Para quién es este documento?**
> Para cualquier persona que quiera entender qué es TechMind, cómo funciona y qué problema resuelve,
> sin necesidad de saber programar.

---

## 🎯 ¿Qué problema resuelve TechMind?

Imaginate que sos estudiante o profesional de tecnología.
Cada día leés artículos, tutoriales, documentación de herramientas, resúmenes de cursos…
Con el tiempo, tenés cientos de notas y materiales guardados en distintos lugares,
y cuando querés volver a encontrar algo, **no sabés ni por dónde empezar**.

**TechMind resuelve exactamente ese problema.**

Le mandás un texto técnico — puede ser el título de un artículo y su descripción —
y el sistema te dice automáticamente:

- 📂 **De qué tema trata** (por ejemplo: Backend, Data Science, DevOps, etc.)
- 🔑 **Cuáles son las palabras clave más importantes** del texto
- 📊 **Qué tan seguro está** de esa clasificación

Todo esto en menos de un segundo, sin que ninguna persona tenga que leerlo y etiquetarlo a mano.

---

## 🏗️ ¿Cómo está construido el proyecto?

TechMind tiene tres partes que trabajan juntas, como los engranajes de una máquina:

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   📝 VOS escribís un texto técnico                         │
│                    │                                        │
│                    ▼                                        │
│   🔵 BACKEND (Java) — recibe el texto y lo envía           │
│                    │                                        │
│                    ▼                                        │
│   🟣 CIENCIA DE DATOS (Python) — analiza y clasifica       │
│                    │                                        │
│                    ▼                                        │
│   📦 NUBE (OCI) — guarda los modelos entrenados            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

| Parte | ¿Quién lo hace? | ¿Qué hace? |
|-------|-----------------|------------|
| **Backend** | Equipo de Java | Recibe los textos, los envía al modelo y devuelve la respuesta al usuario |
| **Ciencia de Datos** | Ernesto | Entrena el modelo que aprende a clasificar textos y extraer palabras clave |
| **Base de datos** | Ernesto | Guarda todos los contenidos técnicos en una base de datos PostgreSQL, accesible por todo el equipo |
| **Nube (OCI)** | Todo el equipo | Guarda los modelos entrenados para que estén disponibles en internet |

---

## 🧪 ¿Qué es la parte de Ciencia de Datos?

Esta es la parte que hace la "magia" del proyecto. Acá es donde el sistema **aprende** a reconocer de qué tema habla un texto.

### Paso a paso, ¿cómo aprende la máquina?

#### 🗃️ Paso 1 — Alimentarla con ejemplos
Primero necesitamos darle al sistema muchos ejemplos ya etiquetados.
Estos contenidos están guardados en una **base de datos PostgreSQL** — como una
hoja de cálculo organizada y conectada en red, accesible simultáneamente por el modelo de
Ciencia de Datos y por la API de Back-End.
Empezamos con 61 textos técnicos donde ya sabemos la categoría correcta:

| Título | Texto | Categoría |
|--------|-------|-----------|
| Introducción a Spring Boot | APIs REST con Java y Spring Boot | **Backend** |
| Vectorización con TF-IDF | Técnica para convertir texto en números para ML | **Data Science** |
| Contenedores con Docker | Crear imágenes y desplegar aplicaciones | **DevOps** |
| … | … | … |

Esto se llama **dataset de entrenamiento** — es como el libro de texto del que aprende el sistema.
A diferencia de un archivo de texto o CSV, una base de datos PostgreSQL
permite al sistema **buscar, agregar y filtrar** contenidos automáticamente, y además
guarda un historial de todas las predicciones que el modelo realiza en producción.

---

#### 🧹 Paso 2 — Limpiar los textos
Antes de que el sistema pueda entender los textos, hay que "limpiarlos":

- Se pasan **todo a minúsculas** → `"Spring Boot"` se convierte en `"spring boot"`
- Se eliminan **signos de puntuación** → `,`, `.`, `!` desaparecen
- Se eliminan **palabras vacías** → palabras como *"el"*, *"la"*, *"que"*, *"se explica"* que no aportan significado se descartan

**¿Por qué?** Porque la computadora no entiende el lenguaje como nosotros. Necesita que el texto esté lo más "limpio" posible para identificar las palabras que realmente importan.

---

#### 🔢 Paso 3 — Convertir palabras en números (TF-IDF)
Las computadoras no entienden palabras, solo entienden números.
Usamos una técnica llamada **TF-IDF** (suena complicado, pero la idea es simple):

> **Cada palabra importante del texto se convierte en un número.**
> Cuanto más relevante es una palabra para ESE texto en particular, mayor es su número.

Por ejemplo, si un texto habla de *"kubernetes"* y *"pods"*, esas palabras van a tener números altos en ese texto, y eso le dice al modelo que probablemente sea de **DevOps**.

---

#### 🤖 Paso 4 — Entrenar el modelo clasificador
Con todos los textos ya convertidos en números, entrenamos un algoritmo llamado
**Regresión Logística** — que básicamente aprende los patrones:

> *"Cuando aparecen estas palabras juntas → probablemente es Backend"*
> *"Cuando aparecen estas otras → probablemente es Data Science"*

Es similar a cómo aprende un humano con la práctica: cuantos más ejemplos ve, mejor clasifica.

---

#### 📊 Paso 5 — Evaluar qué tan bien aprendió
Una vez entrenado, lo ponemos a prueba con textos que **nunca había visto antes**
y medimos cuántos acierta. Con el dataset actual (pequeño, de práctica) acierta en el **69%** de los casos.
Con más datos reales, ese número sube significativamente.

---

#### 🔑 Paso 6 — Extraer palabras clave
Para las palabras clave usamos otra lógica: buscamos cuáles son los términos con
mayor "peso" dentro del texto ingresado — las palabras más representativas y únicas
de ese documento en particular.

---

#### 💾 Paso 7 — Guardar el modelo entrenado
Una vez que el modelo aprendió, lo guardamos en un archivo (como si fuera una foto de su conocimiento).
Ese archivo es el que usa el Backend para responder en tiempo real, sin tener que volver a entrenar cada vez.

---

## 📬 ¿Cómo se usa en la práctica?

El sistema expone lo que se llama una **API** — una especie de "ventanilla" por la que otras aplicaciones pueden hablar con él.

**¿Qué le mandás?**
```
Título: "Introducción a Spring Boot"
Texto:  "Conceptos básicos para crear APIs REST con Java y Spring Boot."
```

**¿Qué te devuelve?**
```
Categoría:            Backend
Confianza:            88.9%
Palabras clave:       spring boot, java, api rest, creación apis, spring
```

Eso es todo. En menos de un segundo, el sistema leyó el texto, lo entendió y lo clasificó.

---

## 🗂️ Las 8 categorías que reconoce

| Categoría | ¿De qué trata? | Ejemplo |
|-----------|----------------|---------|
| **Backend** | Lógica del servidor, APIs, bases de datos desde el código | Spring Boot, Node.js, JWT |
| **Frontend** | Interfaces web y experiencia visual del usuario | React, Vue.js, CSS |
| **Data Science** | Análisis de datos e inteligencia artificial | Pandas, Scikit-Learn, ML |
| **DevOps** | Automatización, despliegues y operaciones | Docker, Kubernetes, CI/CD |
| **Mobile** | Aplicaciones para celulares | React Native, Flutter, Swift |
| **Bases de Datos** | Almacenamiento y consulta de datos | SQL, MongoDB, Redis |
| **Seguridad** | Protección de sistemas y datos | JWT, OWASP, cifrado |
| **Cloud** | Servicios en la nube | OCI, servidores, serverless |

---

## ☁️ ¿Dónde vive el proyecto?

Los archivos del modelo entrenado se guardan en **OCI** (Oracle Cloud Infrastructure),
que es básicamente un espacio de almacenamiento en internet. Así el Backend puede
acceder al modelo desde cualquier lugar, sin depender de la computadora de ningún integrante del equipo.

---

## 👥 ¿Qué hizo cada parte del equipo?

```
TechMind
├── 🟣 Ciencia de Datos (Ernesto)
│   ├── Creó el dataset de entrenamiento
│   ├── Migró los datos a PostgreSQL (tabla: contenidos)
│   ├── Construyó el pipeline de análisis en Jupyter
│   ├── Entrenó y evaluó el modelo (TF-IDF + Regresión Logística)
│   ├── Implementó el microservicio FastAPI (/predecir, /health, /categorias)
│   └── Definió el contrato de respuesta JSON para el equipo de Backend
│
├── 🔵 Backend (equipo Java)
│   ├── Construyó la API REST con Spring Boot
│   ├── Llama a FastAPI internamente para clasificar textos
│   └── Valida entradas y maneja errores
│
└── ☁️ OCI (todo el equipo)
    └── Almacena los modelos y aloja la aplicación
```

---

## 🚀 ¿Qué podría mejorar a futuro?

| Mejora | ¿Qué significa en simple? |
|--------|--------------------------|
| **PostgreSQL + FastAPI** | ✅ Ya implementado — base de datos compartida con el equipo, y un servicio Python que clasifica textos en tiempo real |
| **Más datos reales** | Con más ejemplos, el modelo acierta mucho más |
| **Búsqueda por similitud** | "Encontrá contenidos parecidos a este" |
| **Recomendaciones** | "Si leíste esto, también te puede interesar..." |
| **Procesar muchos a la vez** | Clasificar 100 textos de golpe mediante la propia base de datos |
| **Dashboard** | Una pantalla que muestre estadísticas de todo lo clasificado |

---

## 💡 En una sola frase

> **TechMind es un sistema que lee textos técnicos, entiende de qué tema tratan y devuelve esa información organizada automáticamente, ahorrando el trabajo manual de clasificar y etiquetar contenido.**

---

*Documento preparado para la presentación del Hackathon — TechMind G9 LATAM Team 37.*