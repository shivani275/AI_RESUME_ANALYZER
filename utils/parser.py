# utils/parser.py

from typing import Optional, Dict, Union, List, IO
import io

import pdfplumber
from docx import Document

# OCR
import pytesseract
from pdf2image import convert_from_bytes


def parse_resume(uploaded_file: Union[str, IO]) -> Optional[Dict[str, Union[str, List[str]]]]:
    """
    Robust resume parser:
    - Supports PDF (text + scanned via OCR)
    - Supports DOCX
    """

    try:
        filename = getattr(uploaded_file, "name", None)

        if not filename and isinstance(uploaded_file, str):
            filename = uploaded_file

        if not filename:
            raise ValueError("Unable to determine file type")

        filename = filename.lower()

        if filename.endswith(".pdf"):
            text = _parse_pdf_with_ocr(uploaded_file)
        elif filename.endswith(".docx"):
            text = _parse_docx(uploaded_file)
        else:
            raise ValueError("Unsupported file format")

        # Validation
        if not text or len(text.strip()) < 200:
            return None

        return {
            "raw_text": text,
            "experience": []
        }

    except Exception as e:
        print(f"[ERROR] Resume parsing failed: {e}")
        return None


# ==================================================
# PDF Parsing
# ==================================================
def _parse_pdf_with_ocr(file: IO) -> str:
    text = _parse_pdf_text(file)

    # OCR fallback only if needed
    if len(text.strip()) < 100:
        print("[INFO] Falling back to OCR")
        file.seek(0)
        text = _parse_pdf_ocr(file)

    return text


def _parse_pdf_text(file: IO) -> str:
    pages: List[str] = []

    try:
        file.seek(0)
        pdf_bytes = file.read()

        with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
            for page in pdf.pages:
                t = page.extract_text()
                if t:
                    pages.append(t)

    except Exception as e:
        print(f"[ERROR] PDF text extraction failed: {e}")

    return "\n".join(pages).strip()


def _parse_pdf_ocr(file: IO) -> str:
    pages: List[str] = []

    try:
        file.seek(0)
        images = convert_from_bytes(
            file.read(),
            dpi=200,
            first_page=1,
            last_page=3  # ⚡ speed boost
        )

        for img in images:
            text = pytesseract.image_to_string(
                img,
                config="--oem 3 --psm 6"
            )
            if text.strip():
                pages.append(text)

    except Exception as e:
        print(f"[ERROR] OCR failed: {e}")

    return "\n".join(pages).strip()


# ==================================================
# DOCX Parsing
# ==================================================
def _parse_docx(file: IO) -> str:
    try:
        doc = Document(file)
        return "\n".join(
            p.text.strip()
            for p in doc.paragraphs
            if p.text.strip()
        )
    except Exception as e:
        print(f"[ERROR] DOCX parsing failed: {e}")
        return ""
