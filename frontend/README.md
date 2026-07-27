# 🎨 TechMind — Módulo Frontend (Stitch UI)

> Interfaz web interactiva Cyber AI Dark Mode (Glassmorphism) importada desde **Google Stitch** e integrada con la API REST de Spring Boot (`http://localhost:8080/contenido`) y FastAPI (`http://localhost:8000`).

---

## 🏗️ Estructura del Módulo Frontend

```
frontend/
├── index.html        # Plantilla UI Cyber AI importada desde Google Stitch (TailwindCSS v3 CDN)
├── app.js            # Lógica cliente JS: Health checks, peticiones POST, renderizado dinámico y Modal de Historial BD
└── README.md         # Documentación del módulo
```

---

## ✨ Funcionalidades Principales

1. **Indicadores de Estado en Tiempo Real (Header):**
   * Luces LED verdes pulsantes verificando la salud de **Spring Boot :8080**, **FastAPI ML :8000** y **PostgreSQL :5432**.

2. **Formulario de Ingesta & Clasificación:**
   * Campos para Título y Contenido Técnico con botón de acción animado *"Clasificar con TechMind AI"*.

3. **Panel de Resultado del Análisis de IA:**
   * **Badge de Categoría Predicha:** Icono y color único según la clase (`Backend`, `Frontend`, `Data Science`, `DevOps`, `Mobile`, `Bases de Datos`, `Seguridad`, `Cloud`).
   * **Barra de Confianza:** Porcentaje animado de probabilidad devuelto por el modelo.
   * **Tags de Palabras Clave:** Términos TF-IDF más relevantes del texto.
   * **Modal JSON Crudo:** Permite a los evaluadores de la Hackathon inspeccionar la respuesta JSON completa.

4. **Historial Persistido en PostgreSQL:**
   * Consulta directa al endpoint `GET /predicciones` para listar los registros guardados en la base de datos.
   * **Modal de Historial Completo (`#history-modal`)** accesible con un solo click.

---

## 🚀 Ejecución del Frontend

El frontend se sirve localmente mediante un servidor web liviano en Python:

```bash
# Iniciar servidor web en el puerto 5173
python3 -m http.server 5173 --directory frontend
```

Acceso en el navegador:
👉 **[http://localhost:5173](http://localhost:5173)**
