from rag_utils.llm import get_embedding, ask_llm
import psycopg2
import numpy as np
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

def get_conn():
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
    )

def cosine_similarity(vec1, vec2):
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

def query_documents(user_query, top_k=5):
    query_vector = get_embedding(user_query)
    
    conn = get_conn()
    cur = conn.cursor()
    
    # Fetch all embeddings from DB
    cur.execute("SELECT doc_name, content, embeddings FROM document_embedding")
    rows = cur.fetchall()
    
    results = []
    for doc_name, content, embeddings in rows:
        sim = cosine_similarity(query_vector, embeddings)
        results.append({"doc_name": doc_name, "content": content, "similarity": sim})
    
    # Sort by similarity descending and return top_k
    results.sort(key=lambda x: x["similarity"], reverse=True)
    
    cur.close()
    conn.close()
    
    return results[:top_k]

def answer_query(user_query):
    top_docs = query_documents(user_query)
    context = "\n\n".join([doc['content'] for doc in top_docs])
    answer = ask_llm(f"Answer the question using the context below:\n\n{context}\n\nQuestion: {user_query}")
    return {"answer": answer, "sources": top_docs}
