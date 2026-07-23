"""
app/main.py
Microservicio FastAPI — TechMind · Ciencia de Datos

Endpoints:
    POST /predecir   — inferencia (consumido internamente por Spring Boot)
    GET  /health     — health check
    GET  /categorias — lista las 8 categorías disponibles
    GET  /docs       — documentación Swagger (automática)

Uso:
    uvicorn app.main:app --reload --port 8000
"""

import os
import re
from contextlib import asynccontextmanager

import joblib
import numpy as np
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, field_validator

from app.database import init_db, log_prediccion

load_dotenv()

# ── Estado global del modelo ──────────────────────────────────────────────────
vectorizer = None
modelo = None

# ── Stopwords en español (igual que en el notebook) ───────────────────────────
STOPWORDS_ES = {
    "el","la","los","las","un","una","unos","unas","de","del","al","a","en","y","o",
    "que","con","para","por","se","su","sus","es","son","este","esta","estos","estas",
    "como","más","mas","muy","entre","sobre","desde","hasta","tambien","también","ser",
    "utilizando","utiliza","permite","contenido","introduccion","introducción","tutorial",
    "cómo","como","así","asi",
}


# ── Funciones del pipeline (replicadas del notebook) ─────────────────────────

def limpiar_texto(texto: str) -> str:
    texto = texto.lower()
    texto = re.sub(r"[^a-záéíóúñü0-9\s]", " ", texto)
    palabras = texto.split()
    palabras = [p for p in palabras if p not in STOPWORDS_ES and len(p) > 2]
    return " ".join(palabras)


def extraer_keywords(texto_limpio: str, top_n: int = 5) -> list:
    vector = vectorizer.transform([texto_limpio])
    feature_names = vectorizer.get_feature_names_out()
    scores = vector.toarray()[0]
    top_indices = scores.argsort()[::-1][:top_n]
    return [feature_names[i] for i in top_indices if scores[i] > 0]


# ── Lifespan: carga el modelo al arrancar ─────────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    global vectorizer, modelo
    model_path = os.getenv("MODEL_PATH", "./")
    try:
        vectorizer = joblib.load(os.path.join(model_path, "tfidf_vectorizer.joblib"))
        modelo     = joblib.load(os.path.join(model_path, "modelo_clasificador.joblib"))
        print("✅  Modelos cargados correctamente")
    except FileNotFoundError as e:
        print(f"❌  No se encontraron los .joblib: {e}")
        print("    Ejecutá el notebook TechMind_DataScience.ipynb para generarlos.")
        raise
    init_db()
    yield
    vectorizer = None
    modelo = None


# ── Aplicación FastAPI ────────────────────────────────────────────────────────

app = FastAPI(
    title="TechMind — API de Ciencia de Datos",
    description="Microservicio interno de clasificación de contenidos técnicos. Consumido por Spring Boot.",
    version="0.4.0",
    lifespan=lifespan,
)


# ── Schemas Pydantic ──────────────────────────────────────────────────────────

class ContenidoRequest(BaseModel):
    titulo: str
    texto:  str

    @field_validator("titulo", "texto")
    @classmethod
    def no_vacio(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("El campo no puede estar vacío")
        return v.strip()


class PrediccionResponse(BaseModel):
    categoria:               str
    probabilidad:            float
    informaciones_adicionales: list


# ── Endpoints ─────────────────────────────────────────────────────────────────

@app.post(
    "/predecir",
    response_model=PrediccionResponse,
    summary="Clasificar un contenido técnico",
    description="""
Recibe el **título** y **texto** de un contenido técnico y devuelve:
- `categoria` — una de las 8 categorías del modelo
- `probabilidad` — confianza del modelo (0 a 1)
- `informaciones_adicionales` — top 5 palabras clave por peso TF-IDF

Cada predicción se persiste automáticamente en la tabla `predicciones` de PostgreSQL.
""",
)
def predecir(req: ContenidoRequest):
    if vectorizer is None or modelo is None:
        raise HTTPException(status_code=503, detail="Modelo no disponible. Revisá los .joblib.")

    texto_completo = f"{req.titulo}. {req.texto}"
    texto_limpio   = limpiar_texto(texto_completo)

    vector       = vectorizer.transform([texto_limpio])
    categoria    = modelo.predict(vector)[0]
    proba_arr    = modelo.predict_proba(vector)[0]
    probabilidad = float(proba_arr.max())
    informaciones_adicionales = extraer_keywords(texto_limpio)

    log_prediccion(req.titulo, req.texto, categoria, probabilidad, informaciones_adicionales)

    return PrediccionResponse(
        categoria=categoria,
        probabilidad=round(probabilidad, 4),
        informaciones_adicionales=informaciones_adicionales,
    )


@app.get(
    "/health",
    summary="Health check",
    description="Verificá que FastAPI y el modelo están operativos. Spring Boot debe llamar este endpoint antes de hacer predicciones.",
)
def health():
    return {
        "status":       "ok" if vectorizer is not None else "degraded",
        "model_loaded": vectorizer is not None,
        "version":      "0.4.0",
    }


@app.get(
    "/categorias",
    summary="Lista de categorías disponibles",
    description="Devuelve las 8 categorías en las que el modelo puede clasificar un contenido.",
)
def categorias():
    if modelo is None:
        raise HTTPException(status_code=503, detail="Modelo no cargado")
    return {"categorias": sorted(modelo.classes_.tolist())}
