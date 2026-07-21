"""
app/database.py
Módulo de conexión a PostgreSQL para el microservicio FastAPI de TechMind.

Lee las credenciales desde variables de entorno (.env).
"""

import os
import psycopg2


def get_connection():
    """Abre y devuelve una conexión a PostgreSQL usando las variables de entorno."""
    return psycopg2.connect(
        host=os.getenv("PG_HOST", "localhost"),
        port=int(os.getenv("PG_PORT", 5432)),
        dbname=os.getenv("PG_DB", "techmind"),
        user=os.getenv("PG_USER", "techmind_user"),
        password=os.getenv("PG_PASSWORD", "techmind_pass"),
    )


def init_db():
    """
    Crea la tabla `predicciones` si no existe.
    Se llama una sola vez al arrancar FastAPI (lifespan).
    """
    con = get_connection()
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS predicciones (
            id              SERIAL PRIMARY KEY,
            titulo          TEXT        NOT NULL,
            texto           TEXT        NOT NULL,
            categoria       TEXT        NOT NULL,
            probabilidad    FLOAT       NOT NULL,
            keywords        TEXT[]      NOT NULL,
            created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
        );

        CREATE INDEX IF NOT EXISTS idx_predicciones_categoria
            ON predicciones (categoria);

        CREATE INDEX IF NOT EXISTS idx_predicciones_fecha
            ON predicciones (created_at DESC);
    """)
    con.commit()
    cur.close()
    con.close()
    print("✅  Tabla 'predicciones' lista en PostgreSQL")


def log_prediccion(
    titulo: str,
    texto: str,
    categoria: str,
    probabilidad: float,
    keywords: list,
) -> None:
    """
    Persiste una predicción en la tabla `predicciones`.
    Los errores de escritura se loguean pero NO interrumpen la respuesta al cliente.
    """
    try:
        con = get_connection()
        cur = con.cursor()
        cur.execute(
            """
            INSERT INTO predicciones (titulo, texto, categoria, probabilidad, keywords)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (titulo, texto, categoria, probabilidad, keywords),
        )
        con.commit()
        cur.close()
        con.close()
    except Exception as exc:
        print(f"⚠️  Error al guardar predicción en PostgreSQL: {exc}")
