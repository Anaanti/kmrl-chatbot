# rag_utils/ingest.py
from .embedder import embed_text
from .models import Document  # Your Django model
import math

def split_into_chunks(text, chunk_size=500, overlap=50):
    """
    Splits text into chunks of chunk_size with overlap.
    """
    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = min(start + chunk_size, text_length)
        chunk = text[start:end]
        chunks.append(chunk)
        start += chunk_size - overlap

    return chunks

def cmrf(document_text, title=None):
    """
    Chunk, embed, and store a document in Postgres.
    Maintains 384-dimensional embeddings.
    """
    chunks = split_into_chunks(document_text)
    for i, chunk in enumerate(chunks):
        embedding = embed_text(chunk)  # 384-dim vector
        Document.objects.create(
            title=title or f"chunk-{i}",
            content=chunk,
            embedding=embedding  # make sure your DB column supports 384-dim
        )

    return f"{len(chunks)} chunks ingested successfully."

# Example usage:
# cmrf("This is a long document text...", title="Sample Doc")
