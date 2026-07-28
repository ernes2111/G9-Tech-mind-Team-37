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
    Verifica la conexión a PostgreSQL al arrancar FastAPI.

    NOTA (BUG-5 — resuelto 2026-07-27):
    FastAPI ya NO crea ni gestiona la tabla `predicciones`.
    Esa tabla es responsabilidad exclusiva de Flyway (Spring Boot), que la
    crea con el schema correcto (contenido_id FK, palabras_clave TEXT, etc.).
    Crear la tabla desde aquí generaba un conflicto de schemas incompatibles.

    FastAPI solo persiste predicciones a través de log_prediccion(),
    que escribe en la tabla `predicciones` ya creada por Flyway.
    """
    con = get_connection()
    cur = con.cursor()
    cur.execute("""
        SELECT 1;
    """)
    cur.close()
    con.close()
    print("✅  Conexión a PostgreSQL verificada correctamente")


def get_predicciones(limit: int = 50):
    """
    Obtiene el historial de predicciones guardadas en PostgreSQL
    uniendo la tabla predicciones con contenidos por contenido_id.
    """
    try:
        con = get_connection()
        cur = con.cursor()
        cur.execute(
            """
            SELECT p.id, c.titulo, p.categoria, p.probabilidad, p.palabras_clave, p.created_at
            FROM predicciones p
            JOIN contenidos c ON c.id = p.contenido_id
            ORDER BY p.created_at DESC
            LIMIT %s
            """,
            (limit,),
        )
        rows = cur.fetchall()
        cur.close()
        con.close()
        return [
            {
                "id": r[0],
                "titulo": r[1],
                "categoria": r[2],
                "probabilidad": float(r[3]),
                "keywords": r[4].split(",") if r[4] else [],
                "created_at": r[5].isoformat() if r[5] else ""
            }
            for r in rows
        ]
    except Exception as exc:
        print(f"⚠️ Error al obtener predicciones de PostgreSQL: {exc}")
        return []



