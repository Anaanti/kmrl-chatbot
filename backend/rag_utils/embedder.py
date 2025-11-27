# rag_utils/embedder.py
from .embeddings import get_embedding

def embed_text(text):
    """
    Returns embedding as a list (384-dim).
    """
    return get_embedding(text)
