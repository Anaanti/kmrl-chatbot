from rag_utils.embeddings_store import documents as default_documents
import numpy as np

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def query_documents(query, documents=None, top_k=2):
    from rag_utils.embeddings import get_embedding
    query_vec = get_embedding(query)
    
    # Use provided documents or default
    if documents is None:
        documents = default_documents
    
    # Compute similarity with all documents
    similarities = [(doc, cosine_similarity(query_vec, doc["embedding"])) for doc in documents]
    
    # Sort by similarity
    similarities.sort(key=lambda x: x[1], reverse=True)
    
    # Return top_k documents with scores
    return similarities[:top_k]
