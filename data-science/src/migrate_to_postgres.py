"""
migrate_to_postgres.py
Migra el dataset de TechMind a PostgreSQL.

Lee desde techmind.db (SQLite) si existe, o desde contenidos_tecnicos.csv como fallback.
Crea las tablas `contenidos` y `predicciones` si no existen.

Uso:
    cp .env.example .env        # configurar credenciales
    python3 migrate_to_postgres.py
"""

import csv
import os
from datetime import datetime, timezone
from pathlib import Path

import psycopg2
from dotenv import load_dotenv

load_dotenv()

BASE_DIR  = Path(__file__).parent
CSV_PATH  = BASE_DIR.parent / "data" / "raw" / "contenidos_tecnicos.csv"


# ── 1. Conexión a PostgreSQL ──────────────────────────────────────────────────

def get_pg_connection():
    return psycopg2.connect(
        host=os.getenv("PG_HOST", "localhost"),
        port=int(os.getenv("PG_PORT", 5432)),
        dbname=os.getenv("PG_DB", "techmind"),
        user=os.getenv("PG_USER", "techmind_user"),
        password=os.getenv("PG_PASSWORD", "techmind_pass"),
    )


# ── 2. Crear esquema ─────────────────────────────────────────────────────────

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS contenidos (
    id          SERIAL PRIMARY KEY,
    titulo      TEXT        NOT NULL,
    texto       TEXT        NOT NULL,
    categoria   TEXT        NOT NULL,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS predicciones (
    id                        SERIAL PRIMARY KEY,
    titulo                    TEXT        NOT NULL,
    texto                     TEXT        NOT NULL,
    categoria                 TEXT        NOT NULL,
    probabilidad              FLOAT       NOT NULL,
    informaciones_adicionales TEXT[]      NOT NULL,
    created_at                TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_contenidos_categoria   ON contenidos  (categoria);
CREATE INDEX IF NOT EXISTS idx_predicciones_categoria ON predicciones (categoria);
CREATE INDEX IF NOT EXISTS idx_predicciones_fecha     ON predicciones (created_at DESC);
"""

pg_con = get_pg_connection()
pg_cur = pg_con.cursor()
pg_cur.execute(SCHEMA_SQL)
pg_con.commit()
print("✅  Esquema creado/verificado en PostgreSQL")


# ── 3. Leer registros de la fuente disponible ─────────────────────────────────

rows = []
timestamp = datetime.now(timezone.utc).isoformat()

print(f"📂  Leyendo dataset desde CSV: {CSV_PATH.name}")
with open(CSV_PATH, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row["titulo"].strip():
            rows.append((row["titulo"].strip(), row["texto"].strip(), row["categoria"].strip(), timestamp))

print(f"    {len(rows)} registros leídos")


# ── 4. Verificar si ya hay datos en PostgreSQL ────────────────────────────────

pg_cur.execute("SELECT COUNT(*) FROM contenidos")
existing = pg_cur.fetchone()[0]

if existing > 0:
    print(f"\n⚠️  La tabla 'contenidos' ya tiene {existing} registros.")
    resp = input("   ¿Querés reemplazarlos? (s/N): ").strip().lower()
    if resp != "s":
        print("   Migración cancelada — datos existentes conservados.")
        pg_cur.close()
        pg_con.close()
        exit(0)
    pg_cur.execute("TRUNCATE TABLE contenidos RESTART IDENTITY CASCADE")
    pg_con.commit()
    print("   Tabla vaciada.")


# ── 5. Insertar registros ─────────────────────────────────────────────────────

pg_cur.executemany(
    "INSERT INTO contenidos (titulo, texto, categoria, created_at) VALUES (%s, %s, %s, %s)",
    rows,
)
pg_con.commit()
print(f"✅  {len(rows)} registros insertados en PostgreSQL")


# ── 6. Verificación ───────────────────────────────────────────────────────────

print("\n📊  Distribución por categoría:")
pg_cur.execute("SELECT categoria, COUNT(*) AS n FROM contenidos GROUP BY categoria ORDER BY n DESC")
for cat, count in pg_cur.fetchall():
    print(f"    {cat:<20} {count} registros")

pg_cur.execute("SELECT COUNT(*) FROM contenidos")
total = pg_cur.fetchone()[0]
print(f"\n    TOTAL: {total} registros")

print("\n🔍  Ejemplo — primeros 3 registros:")
pg_cur.execute("SELECT id, titulo, categoria FROM contenidos LIMIT 3")
for row in pg_cur.fetchall():
    print(f"    [{row[0]}] {row[2]:<20} | {row[1]}")

pg_cur.close()
pg_con.close()
print("\n✅  Migración a PostgreSQL completada.")
