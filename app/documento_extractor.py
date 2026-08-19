"""
app/documento_extractor.py
Módulo de extracción de texto de documentos PDF y DOCX — TechMind

Funciones públicas:
    extraer_pdf(file_bytes, filename, max_pages)  → ExtraerResultado
    extraer_docx(file_bytes, filename, max_words) → ExtraerResultado

Constantes de límite (sobreescribibles por app/main.py):
    MAX_PAGES_PDF   = 15
    MAX_WORDS_DOCX  = 4500   (~15 páginas a ~300 palabras/página)
    MAX_CHARS_TEXTO = 20_000
    MIN_WORDS_PARA_CLASIFICAR = 10
"""

import io
import re
from dataclasses import dataclass

# ── Constantes de límite ─────────────────────────────────────────────────────
MAX_PAGES_PDF: int = 15
MAX_WORDS_DOCX: int = 4500
MAX_CHARS_TEXTO: int = 20_000
MIN_WORDS_PARA_CLASIFICAR: int = 10


# ── Resultado unificado ───────────────────────────────────────────────────────
@dataclass
class ExtraerResultado:
    titulo: str
    texto: str
    paginas_procesadas: int          # páginas (PDF) o bloques de 300 palabras (DOCX)
    formato: str                     # "pdf" | "docx"
    texto_truncado: bool = False     # True si se recortó por límite de páginas/palabras
    advertencia: str = ""            # mensaje opcional para el frontend


# ── Helpers internos ──────────────────────────────────────────────────────────

def _limpiar_texto_extraido(texto: str) -> str:
    """
    Limpieza liviana del texto crudo extraído:
    - Colapsa líneas en blanco múltiples en una sola.
    - Elimina caracteres de control invisibles (excepto \\n y \\t).
    - Recorta espacios al inicio y fin.
    No aplica stopwords ni stemming; eso lo hace el pipeline de FastAPI.
    """
    texto = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', '', texto)
    texto = re.sub(r'\n{3,}', '\n\n', texto)
    texto = re.sub(r'[ \t]{2,}', ' ', texto)
    return texto.strip()


def _inferir_titulo(candidatos: list, filename: str) -> str:
    """
    Selecciona el primer candidato no vacío con al menos 3 palabras.
    Si ninguno aplica, usa el nombre de archivo sin extensión.
    El filename se sanitiza aquí como segunda línea de defensa
    (la primera está en el endpoint de FastAPI).
    """
    for candidato in candidatos:
        if candidato and len(candidato.split()) >= 3:
            return candidato[:200].strip()
    # Sanitizar filename: eliminar separadores de path y puntos iniciales
    safe_filename = re.sub(r'[\\/]', '_', filename).lstrip('.')
    nombre_limpio = re.sub(r'\.[^.]+$', '', safe_filename)   # quitar extensión
    nombre_limpio = re.sub(r'[_\-]+', ' ', nombre_limpio).strip()
    return nombre_limpio[:200] if nombre_limpio else "Documento sin título"


def _truncar_texto(texto: str):
    """Trunca el texto a MAX_CHARS_TEXTO. Retorna (texto, fue_truncado)."""
    if len(texto) > MAX_CHARS_TEXTO:
        return texto[:MAX_CHARS_TEXTO], True
    return texto, False


# ── Extracción PDF ────────────────────────────────────────────────────────────

def extraer_pdf(
    file_bytes: bytes,
    filename: str = "documento.pdf",
    max_pages: int = MAX_PAGES_PDF,
) -> ExtraerResultado:
    """
    Extrae texto de un PDF usando pdfplumber.

    Args:
        file_bytes: contenido del archivo en bytes (ya leído del UploadFile).
        filename:   nombre original del archivo (para inferir título).
        max_pages:  máximo de páginas a procesar.

    Returns:
        ExtraerResultado con titulo, texto, paginas_procesadas y advertencias.

    Raises:
        ValueError: si el archivo está protegido, es un PDF inválido o tiene
                    menos de MIN_WORDS_PARA_CLASIFICAR palabras útiles.
    """
    try:
        import pdfplumber
    except ImportError:
        raise ImportError("pdfplumber no está instalado. Verificá requirements.txt.")

    try:
        pdf_stream = io.BytesIO(file_bytes)
        pdf = pdfplumber.open(pdf_stream)
    except Exception as exc:
        raise ValueError(f"No se pudo abrir el PDF: {exc}") from exc

    total_paginas = len(pdf.pages)
    paginas_a_procesar = min(total_paginas, max_pages)
    texto_truncado = total_paginas > max_pages

    bloques_texto = []
    titulo_candidato_primera_pagina = ""

    try:
        for i, pagina in enumerate(pdf.pages[:paginas_a_procesar]):
            try:
                texto_pagina = pagina.extract_text() or ""
            except Exception:
                continue

            if texto_pagina.strip():
                bloques_texto.append(texto_pagina)

                if i == 0 and not titulo_candidato_primera_pagina:
                    primera_linea = texto_pagina.strip().splitlines()[0].strip()
                    if len(primera_linea.split()) >= 3:
                        titulo_candidato_primera_pagina = primera_linea

    finally:
        pdf.close()

    if not bloques_texto:
        raise ValueError(
            "El PDF no contiene texto extraíble. "
            "Puede estar escaneado como imagen o protegido con contraseña."
        )

    texto_completo = _limpiar_texto_extraido("\n\n".join(bloques_texto))

    palabras = texto_completo.split()
    if len(palabras) < MIN_WORDS_PARA_CLASIFICAR:
        raise ValueError(
            f"El documento tiene muy poco texto ({len(palabras)} palabras). "
            "Se necesitan al menos 10 palabras para clasificar."
        )

    texto_final, fue_truncado_chars = _truncar_texto(texto_completo)
    fue_truncado = texto_truncado or fue_truncado_chars

    titulo_metadata = ""
    try:
        pdf_stream2 = io.BytesIO(file_bytes)
        with pdfplumber.open(pdf_stream2) as pdf_meta:
            meta = pdf_meta.metadata or {}
            titulo_metadata = (meta.get("Title") or meta.get("title") or "").strip()
    except Exception:
        pass

    titulo = _inferir_titulo(
        [titulo_metadata, titulo_candidato_primera_pagina],
        filename
    )

    advertencia = ""
    if texto_truncado:
        advertencia = (
            f"El PDF tiene {total_paginas} páginas. "
            f"Se procesaron las primeras {max_pages} páginas."
        )

    return ExtraerResultado(
        titulo=titulo,
        texto=texto_final,
        paginas_procesadas=paginas_a_procesar,
        formato="pdf",
        texto_truncado=fue_truncado,
        advertencia=advertencia,
    )


# ── Extracción DOCX ───────────────────────────────────────────────────────────

def extraer_docx(
    file_bytes: bytes,
    filename: str = "documento.docx",
    max_words: int = MAX_WORDS_DOCX,
) -> ExtraerResultado:
    """
    Extrae texto de un archivo DOCX usando python-docx.

    Los DOCX no tienen "páginas" nativas, así que se limita por cantidad de
    palabras (~300 palabras/página × 15 páginas = 4500 palabras).

    Args:
        file_bytes: contenido del archivo en bytes.
        filename:   nombre original del archivo.
        max_words:  máximo de palabras a incluir.

    Returns:
        ExtraerResultado con titulo, texto y páginas_procesadas aproximadas.

    Raises:
        ValueError: si el archivo es inválido o tiene poco texto.
    """
    try:
        from docx import Document
    except ImportError:
        raise ImportError("python-docx no está instalado. Verificá requirements.txt.")

    try:
        doc = Document(io.BytesIO(file_bytes))
    except Exception as exc:
        raise ValueError(f"No se pudo abrir el DOCX: {exc}") from exc

    titulo_metadata = ""
    try:
        titulo_metadata = (doc.core_properties.title or "").strip()
    except Exception:
        pass

    parrafos = []
    titulo_primer_heading = ""
    total_palabras = 0
    fue_truncado = False

    for para in doc.paragraphs:
        texto_para = para.text.strip()
        if not texto_para:
            continue

        if not titulo_primer_heading:
            estilo = (para.style.name or "").lower()
            if "heading" in estilo or len(texto_para.split()) >= 5:
                titulo_primer_heading = texto_para

        palabras_para = len(texto_para.split())
        if total_palabras + palabras_para > max_words:
            restantes = max_words - total_palabras
            if restantes > 0:
                palabras_lista = texto_para.split()
                parrafos.append(" ".join(palabras_lista[:restantes]))
            fue_truncado = True
            break

        parrafos.append(texto_para)
        total_palabras += palabras_para

    if not parrafos:
        raise ValueError(
            "El DOCX no contiene texto extraíble o está vacío."
        )

    texto_completo = _limpiar_texto_extraido("\n\n".join(parrafos))

    if len(texto_completo.split()) < MIN_WORDS_PARA_CLASIFICAR:
        raise ValueError(
            "El documento tiene muy poco texto. "
            "Se necesitan al menos 10 palabras para clasificar."
        )

    texto_final, fue_truncado_chars = _truncar_texto(texto_completo)
    fue_truncado = fue_truncado or fue_truncado_chars

    titulo = _inferir_titulo(
        [titulo_metadata, titulo_primer_heading],
        filename
    )

    PALABRAS_POR_PAGINA = 300
    paginas_equiv = max(1, round(total_palabras / PALABRAS_POR_PAGINA))

    advertencia = ""
    if fue_truncado:
        advertencia = (
            f"El documento es extenso. "
            f"Se procesaron las primeras ~{max_words} palabras "
            f"(equivalente a ~{paginas_equiv} páginas)."
        )

    return ExtraerResultado(
        titulo=titulo,
        texto=texto_final,
        paginas_procesadas=paginas_equiv,
        formato="docx",
        texto_truncado=fue_truncado,
        advertencia=advertencia,
    )
