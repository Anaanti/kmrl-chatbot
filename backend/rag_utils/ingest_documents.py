# rag_utils/ingest_documents.py

import os
import sys

# ----------------------------------------------------------------------
# PATH FIX: Ensure 'backend' and 'rag_utils' are discoverable.
# ----------------------------------------------------------------------

# 1. Get the directory containing this script (rag_utils)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# 2. Get the directory containing the project root (kmrl-chatbot)
PROJECT_ROOT = os.path.join(SCRIPT_DIR, '..', '..')

# Add the project root to the system path
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
# Add the backend directory to the system path
BACKEND_DIR = os.path.join(SCRIPT_DIR, '..')
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

# ----------------------------------------------------------------------
# END PATH FIX
# ----------------------------------------------------------------------


# Now the imports should work:
from glob import glob
# Corrected imports
from rag_utils.query_llm import get_embedding, get_conn 
# These modules are now found via the sys.path changes
from rag_utils.load_pdfs import load_pdf_chunks
from rag_utils.load_txt import load_txt_chunks
import django
import psycopg2 


# Define Data Directory and Chunk Size
# DATA_DIR is now relative to the backend folder structure
DATA_DIR = os.path.join(PROJECT_ROOT, "backend", "docs") 
CHUNK_SIZE = 500

# Set the Django settings module and initialize Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
try:
    # Django initialization is needed for models or full environment setup
    django.setup()
except Exception as e:
    # This warning is acceptable if Django setup isn't strictly needed for psycopg2 functions
    print(f"Warning: Django setup failed ({e}), continuing with direct database access.")


def ingest_documents():
    """Reads documents from DATA_DIR, chunks, embeds, and inserts into PostgreSQL."""
    print("Starting ingestion...")
    conn = get_conn()
    cur = conn.cursor()

    # Clear old data before ingestion (clean slate)
    cur.execute("TRUNCATE TABLE document_embedding RESTART IDENTITY;")
    print("Cleared old document_embedding data.")
    
    # Supported file types
    pdf_files = glob(os.path.join(DATA_DIR, "*.pdf"))
    txt_files = glob(os.path.join(DATA_DIR, "*.txt"))

    if not pdf_files and not txt_files:
        print(f"No documents found in {DATA_DIR}. Please check path.")
        cur.close()
        conn.close()
        return

    for file_path in pdf_files + txt_files:
        file_name = os.path.basename(file_path)
        print(f"Processing: {file_name}")

        if file_path.endswith(".pdf"):
            chunks = load_pdf_chunks(file_path, CHUNK_SIZE)
        else:
            chunks = load_txt_chunks(file_path, CHUNK_SIZE)

        for chunk in chunks:
            # Generate embedding using the function from query_llm
            embedding = get_embedding(chunk)

            # Insert into PostgreSQL using parameter binding
            cur.execute(
                """
                INSERT INTO document_embedding (doc_name, content, embeddings)
                VALUES (%s, %s, %s)
                ON CONFLICT DO NOTHING;
                """,
                (file_name, chunk, embedding)
            )

    conn.commit()
    cur.close()
    conn.close()
    print("Ingestion complete!")


if __name__ == "__main__":
    ingest_documents()