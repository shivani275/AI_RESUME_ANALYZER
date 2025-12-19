import fitz  # PyMuPDF

def extract_text_from_pdf(file):
    """
    Extract text from a PDF file (path or BytesIO/Streamlit file).
    """
    text = ""
    try:
        if hasattr(file, "read"):
            file.seek(0)
            pdf = fitz.open(stream=file.read(), filetype="pdf")
        else:
            pdf = fitz.open(file)

        for page in pdf:
            text += page.get_text()
        pdf.close()
    except Exception as e:
        print(f"Error reading PDF: {e}")
    return text
