# rag_utils/ingest_documents.py

import os
from glob import glob
from rag_utils.llm import get_embedding
from rag_utils.query_llm import get_conn
from rag_utils.load_pdfs import load_pdf_chunks
from rag_utils.load_txt import load_txt_chunks

BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # backend/
DATA_DIR = os.path.join(BASE_DIR, "docs")

# Chunk size
CHUNK_SIZE = 500

def ingest_documents():
    conn = get_conn()
    cur = conn.cursor()

    # Supported file types
    pdf_files = glob(os.path.join(DATA_DIR, "*.pdf"))
    txt_files = glob(os.path.join(DATA_DIR, "*.txt"))

    for file_path in pdf_files + txt_files:
        file_name = os.path.basename(file_path)

        if file_path.endswith(".pdf"):
            chunks = load_pdf_chunks(file_path, CHUNK_SIZE)
        else:
            chunks = load_txt_chunks(file_path, CHUNK_SIZE)

        for chunk in chunks:
            # Generate embedding
            embedding = get_embedding(chunk)

            # Insert into PostgreSQL
            cur.execute(
                """
                INSERT INTO document_embedding (doc_name, content, embeddings)
                VALUES (%s, %s, %s)
                ON CONFLICT DO NOTHING
                """,
                (file_name, chunk, embedding)
                
            )

    conn.commit()
    cur.close()
    conn.close()
    print("Ingestion complete!")


if __name__ == "__main__":
    ingest_documents()
