# utils/pdf_parser.py
import fitz  # PyMuPDF
from typing import Union, IO
import logging


def extract_text_from_pdf(file: Union[str, IO]) -> str:
    """
    Extract text from a PDF file (file path or file-like object).

    Supports:
    - File paths (str)
    - Streamlit uploads / BytesIO

    Returns:
        str: Extracted text from all pages
    """

    if not file:
        return ""

    text_pages = []

    try:
        # Case 1: File-like object (Streamlit / BytesIO)
        if hasattr(file, "read"):
            file.seek(0)
            pdf_bytes = file.read()

            if not pdf_bytes:
                return ""

            pdf = fitz.open(stream=pdf_bytes, filetype="pdf")

        # Case 2: File path
        else:
            pdf = fitz.open(file)

        # Extract text page-by-page
        for page in pdf:
            page_text = page.get_text("text")
            if page_text:
                cleaned = page_text.strip()
                if cleaned:
                    text_pages.append(cleaned)

        pdf.close()

    except Exception as e:
        logging.error(f"PDF parsing failed: {e}")
        return ""

    return "\n\n".join(text_pages)
