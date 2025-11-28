from api.models import DocumentEmbedding
from rag_utils.llm import get_embedding  # your Ollama wrapper
from rag_utils.load_pdfs import load_pdf_chunks
from rag_utils.load_txt import load_txt_chunks

def ingest_document(file_path, doc_name):
    if file_path.endswith(".pdf"):
        chunks = load_pdf_chunks(file_path)
    elif file_path.endswith(".txt"):
        chunks = load_txt_chunks(file_path)
    else:
        raise ValueError("Unsupported file type")

    for chunk_text in chunks:
        embedding = get_embedding(chunk_text)  # automatically generated
        DocumentEmbedding.objects.create(
            doc_name=doc_name,
            content=chunk_text,
            embeddings=embedding
        )

def ingest_folder(folder_path):
    import os
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        ingest_document(file_path, doc_name=file_name)
