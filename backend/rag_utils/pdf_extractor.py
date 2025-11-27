# rag_utils/pdf_extractor.py
import fitz  # PyMuPDF

def extract_text_from_pdf(path):
    text = ""
    doc = fitz.open(path)
    for page in doc:
        text += page.get_text()
    return text
