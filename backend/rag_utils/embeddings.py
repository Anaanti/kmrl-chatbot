# rag_utils/embeddings.py
from sentence_transformers import SentenceTransformer

# 384-dimensional model
model = SentenceTransformer("all-MiniLM-L6-v2")

def get_embedding(text: str):
    emb = model.encode(text)
    return emb.tolist()
