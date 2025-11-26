from django.db import connection
from .embeddings import get_embedding

def search_similar_documents(query: str, limit: int = 5):
    """
    Performs a vector similarity search using pgvector.
    """
    embedding = get_embedding(query)

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id, content,
                   1 - (embedding <=> %s) AS similarity
            FROM api_document
            ORDER BY embedding <=> %s
            LIMIT %s
        """, [embedding, embedding, limit])

        rows = cursor.fetchall()

    return [
        {"id": r[0], "content": r[1], "similarity": float(r[2])}
        for r in rows
    ]


def build_context(query: str):
    results = search_similar_documents(query)
    context = "\n\n".join([r["content"] for r in results])
    return context
