from ..pdf_extractor import extract_text_from_pdf

def load_pdf_file(path: str) -> str:
    return extract_text_from_pdf(path)
