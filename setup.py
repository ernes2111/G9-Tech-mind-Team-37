#!/usr/bin/env python3
"""
setup.py — TechMind · Script de instalación y arranque automático
================================================================
Ejecutá con:
    python setup.py          ← primera vez (instala todo y arranca)
    python setup.py --start  ← veces siguientes (solo arranca)

Compatible con Windows y macOS/Linux.
"""

import os
import sys
import subprocess
import platform
import time
import shutil
import argparse

# ─── Configuración ────────────────────────────────────────────────────────────

IS_WINDOWS  = platform.system() == "Windows"
VENV_DIR    = "venv"
SCRIPTS_DIR = "Scripts" if IS_WINDOWS else "bin"

VENV_PYTHON   = os.path.join(VENV_DIR, SCRIPTS_DIR, "python.exe" if IS_WINDOWS else "python")
VENV_PIP      = os.path.join(VENV_DIR, SCRIPTS_DIR, "pip.exe"    if IS_WINDOWS else "pip")
VENV_UVICORN  = os.path.join(VENV_DIR, SCRIPTS_DIR, "uvicorn.exe" if IS_WINDOWS else "uvicorn")

REQUIREMENTS  = os.path.join("data-science", "requirements.txt")
MIGRATE_SCRIPT = os.path.join("data-science", "src", "migrate_to_postgres.py")

TOTAL_STEPS   = 7


# ─── Helpers de output ────────────────────────────────────────────────────────

def header(n, msg):
    print(f"\n{'─' * 60}")
    print(f"  [{n}/{TOTAL_STEPS}] {msg}")
    print(f"{'─' * 60}")

def ok(msg):    print(f"  ✅  {msg}")
def warn(msg):  print(f"  ⚠️   {msg}")
def info(msg):  print(f"  ℹ️   {msg}")

def fail(msg):
    print(f"\n  ❌  {msg}")
    print("  Revisá el error anterior y volvé a intentar.")
    sys.exit(1)

def run(cmd, **kwargs):
    """Ejecuta un comando como string. Devuelve CompletedProcess."""
    return subprocess.run(cmd, shell=True, **kwargs)

def run_or_fail(cmd, error_msg, **kwargs):
    """Ejecuta un comando y termina el script si falla."""
    result = run(cmd, **kwargs)
    if result.returncode != 0:
        fail(error_msg)
    return result


# ─── Paso 1 — Verificar Python ───────────────────────────────────────────────

def check_python():
    header(1, "Verificando Python")
    v = sys.version_info
    if v.major < 3 or (v.major == 3 and v.minor < 10):
        fail(
            f"Se requiere Python 3.10 o superior. Tenés Python {v.major}.{v.minor}.\n"
            "  Descargalo desde https://www.python.org/downloads/\n"
            "  (En Windows: marcá 'Add Python to PATH' durante la instalación)"
        )
    ok(f"Python {v.major}.{v.minor}.{v.micro} — OK")


# ─── Paso 2 — Entorno virtual ────────────────────────────────────────────────

def create_venv():
    header(2, "Preparando entorno virtual de Python")
    if os.path.exists(VENV_PYTHON):
        ok("El entorno virtual ya existe — omitiendo creación")
        return
    info("Creando entorno virtual en ./venv ...")
    run_or_fail(
        f"{sys.executable} -m venv {VENV_DIR}",
        "No se pudo crear el entorno virtual."
    )
    ok("Entorno virtual creado en ./venv")


# ─── Paso 3 — Instalar dependencias ──────────────────────────────────────────

def install_deps():
    header(3, "Instalando dependencias de Python")
    if not os.path.exists(REQUIREMENTS):
        fail(f"No se encontró el archivo {REQUIREMENTS}")
    info("Esto puede tardar 1-2 minutos la primera vez...")
    run_or_fail(
        f'"{VENV_PIP}" install -r "{REQUIREMENTS}" --quiet',
        f"Error al instalar dependencias desde {REQUIREMENTS}"
    )
    ok("Todas las dependencias instaladas")


# ─── Paso 4 — Variables de entorno ───────────────────────────────────────────

def setup_env():
    header(4, "Configurando variables de entorno")
    if os.path.exists(".env"):
        ok(".env ya existe — omitiendo copia")
        return
    if not os.path.exists(".env.example"):
        fail("No se encontró .env.example en la raíz del proyecto.")
    shutil.copy(".env.example", ".env")
    ok(".env creado desde .env.example (configuración local lista)")


# ─── Paso 5 — Docker / PostgreSQL ────────────────────────────────────────────

def start_docker():
    header(5, "Levantando PostgreSQL con Docker")

    # Verificar que Docker esté disponible
    result = run("docker --version", capture_output=True)
    if result.returncode != 0:
        fail(
            "Docker no está instalado o no está en el PATH.\n"
            "  Instalá Docker Desktop desde https://www.docker.com/products/docker-desktop/\n"
            "  (En Windows: puede requerir habilitar WSL 2)"
        )

    # Verificar que Docker Desktop esté corriendo
    result = run("docker ps", capture_output=True)
    if result.returncode != 0:
        fail(
            "Docker está instalado pero no está corriendo.\n"
            "  Abrí Docker Desktop y esperá a que el ícono esté en verde, luego volvé a ejecutar este script."
        )

    # Levantar el contenedor
    info("Ejecutando docker-compose up -d ...")
    result = run("docker-compose up -d")
    if result.returncode != 0:
        # Puede ser que ya exista el contenedor con otro nombre de proyecto — intentar iniciarlo
        info("Intentando iniciar contenedor existente 'techmind-postgres'...")
        result = run("docker start techmind-postgres", capture_output=True)
        if result.returncode != 0:
            fail("No se pudo levantar PostgreSQL con Docker.")

    # Esperar a que PostgreSQL esté listo (health check)
    print(f"  ⏳ Esperando que PostgreSQL esté listo", end="", flush=True)
    for _ in range(30):
        time.sleep(1)
        result = run(
            "docker exec techmind-postgres pg_isready -U techmind_user -d techmind",
            capture_output=True
        )
        if result.returncode == 0:
            print(" ✅")
            ok("PostgreSQL listo en localhost:5432")
            return
        print(".", end="", flush=True)

    print()
    warn("PostgreSQL tardó más de lo esperado. Continuando de todas formas...")


# ─── Paso 6 — Migración de datos ─────────────────────────────────────────────

def migrate_db():
    header(6, "Cargando datos iniciales en PostgreSQL")
    if not os.path.exists(MIGRATE_SCRIPT):
        fail(f"No se encontró el script de migración: {MIGRATE_SCRIPT}")

    info("Ejecutando script de migración...")
    info("(Si los datos ya existen se conservarán — no se borrarán)")

    # Pasamos "N\n" al stdin para responder automáticamente
    # a la pregunta interactiva "¿Querés reemplazarlos? (s/N)"
    result = subprocess.run(
        [VENV_PYTHON, MIGRATE_SCRIPT],
        input="N\n",
        text=True
    )

    if result.returncode != 0:
        warn("El script de migración terminó con un aviso. Revisá la salida anterior.")
    else:
        ok("Base de datos lista")


# ─── Paso 7 — Iniciar FastAPI ────────────────────────────────────────────────

def start_api():
    header(7, "Iniciando el microservicio FastAPI")
    print()
    print("  La API va a quedar corriendo en: http://localhost:8000")
    print("  Documentación Swagger:           http://localhost:8000/docs")
    print("  Para detener el servidor:        CTRL + C")
    print()

    cmd = [VENV_UVICORN, "app.main:app", "--reload", "--port", "8000"]

    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\n\n  🛑 Servidor detenido por el usuario.")
        sys.exit(0)
    except FileNotFoundError:
        fail(
            f"No se encontró uvicorn en {VENV_UVICORN}\n"
            "  Asegurate de haber completado el Paso 3 (instalación de dependencias)."
        )


# ─── Modo --start (solo arranca, sin setup) ──────────────────────────────────

def quick_start():
    """Verifica que todo esté instalado y arranca directamente."""
    print()
    print("  🧠 TechMind — Inicio rápido")
    print()

    if not os.path.exists(VENV_PYTHON):
        fail(
            "El entorno virtual no existe. Ejecutá primero:\n"
            "    python setup.py"
        )

    header(1, "Verificando Docker / PostgreSQL")
    result = run("docker ps --filter name=techmind-postgres --format '{{.Status}}'",
                 capture_output=True, text=True)
    if "Up" not in result.stdout:
        info("PostgreSQL no está corriendo — levantándolo...")
        run("docker-compose up -d")
        time.sleep(5)
    ok("PostgreSQL activo")

    start_api()


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="TechMind — Script de setup y arranque del microservicio Python"
    )
    parser.add_argument(
        "--start",
        action="store_true",
        help="Solo arranca el servidor (omite instalación). Usalo las veces siguientes."
    )
    args = parser.parse_args()

    print()
    print("╔══════════════════════════════════════════════════════════╗")
    print("║   🧠 TechMind — Setup del Microservicio Python           ║")
    print("║   Hackathon G9 LATAM · Equipo 37                         ║")
    print("╚══════════════════════════════════════════════════════════╝")

    if args.start:
        quick_start()
        return

    # Setup completo
    check_python()
    create_venv()
    install_deps()
    setup_env()
    start_docker()
    migrate_db()
    start_api()


if __name__ == "__main__":
    main()
