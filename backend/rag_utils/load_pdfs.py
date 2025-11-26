import os
import PyPDF2
from rag_utils.embeddings import get_embedding

DOCS_FOLDER = os.path.join(os.path.dirname(__file__), "..", "docs")

def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text

def chunk_text(text, chunk_size=500):
    words = text.split()
    chunks = []

    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i + chunk_size])
        if chunk.strip():
            chunks.append(chunk)

    return chunks

def load_all_pdfs():
    documents = []

    for filename in os.listdir(DOCS_FOLDER):
        if filename.lower().endswith(".pdf"):
            pdf_path = os.path.join(DOCS_FOLDER, filename)
            print(f"📄 Loading PDF: {filename}")

            text = extract_text_from_pdf(pdf_path)
            chunks = chunk_text(text)

            for idx, chunk in enumerate(chunks):
                doc = {
                    "id": f"{filename}_chunk_{idx}",
                    "text": chunk,
                    "embedding": get_embedding(chunk)
                }
                documents.append(doc)

    print(f"Loaded {len(documents)} chunks from all PDFs.")
    return documents

if __name__ == "__main__":
    docs = load_all_pdfs()
    print("Example loaded document:", docs[0] if docs else "No documents found")
