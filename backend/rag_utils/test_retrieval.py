# backend/rag_utils/test_retrieval.py

import psycopg2
from sentence_transformers import SentenceTransformer
from rag_utils.query_llm import get_conn  # only DB connection, not actual LLM

def get_top_k_chunks(query, k=3):
    model = SentenceTransformer("all-MiniLM-L6-v2")
    query_embedding = model.encode(query).tolist()

    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT doc_name, content, embeddings <-> (%s)::vector AS distance
        FROM document_embedding
        ORDER BY embeddings <-> (%s)::vector
        LIMIT %s;
    """, (query_embedding, query_embedding, k))


    rows = cur.fetchall()
    conn.close()
    return rows


if __name__ == "__main__":
    query = input("Enter your query: ")
    results = get_top_k_chunks(query)

    print("\nTop chunks:")
    for doc_name, content, distance in results:
        print("-" * 40)
        print("Document:", doc_name)
        print("Distance:", distance)
        print("Content snippet:", content[:200])
