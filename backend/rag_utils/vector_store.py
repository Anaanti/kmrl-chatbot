# rag_utils/vector_store.py
import os
import numpy as np
from rag_utils.embeddings import get_embedding
from rag_utils.loaders.txt_loader import load_txt_file  # or load multiple if you want

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def load_documents_from_folder(folder_path="backend/docs"):
    documents = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            content = load_txt_file(os.path.join(folder_path, filename))
            documents.append({
                "name": filename,
                "text": content,
                "embedding": get_embedding(content)
            })
        elif filename.endswith(".pdf"):
            from rag_utils.load_pdfs import load_pdf_text
            content = load_pdf_text(os.path.join(folder_path, filename))
            documents.append({
                "name": filename,
                "text": content,
                "embedding": get_embedding(content)
            })
    return documents

def query_documents(query, documents=None, top_k=2):
    # Load docs if none provided
    if documents is None:
        documents = load_documents_from_folder()

    query_vec = get_embedding(query)
    similarities = [(doc, cosine_similarity(query_vec, doc["embedding"])) for doc in documents]
    similarities.sort(key=lambda x: x[1], reverse=True)
    return similarities[:top_k]
