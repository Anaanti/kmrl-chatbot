# rag_utils/vector_store.py
import json
from django.db import connection, transaction
from api.models import Document
from .embedder import embed_text

def _to_pgvector_str(vec):
    """
    Convert python list/iterable of floats to Postgres/pgvector literal.
    e.g. [0.1, 0.2] -> '[0.1,0.2]'
    """
    return "[" + ",".join(str(float(x)) for x in vec) + "]"

def upsert_document(filename: str, content: str, embedding: list):
    """
    Insert a document chunk into Postgres (Document model) using Django ORM.
    embedding: python list of floats
    """
    # You can use Document.objects.create(...) directly; django-pgvector will
    # handle conversion automatically if embedding is a list.
    doc = Document.objects.create(
        filename=filename,
        content=content,
        embedding=embedding
    )
    return doc

def search_similar(query_or_vec, top_k=5):
    """
    If query_or_vec is a string, it will be embedded using embed_text().
    Returns list of dicts: {"id":..., "filename":..., "content":..., "distance":...}
    Uses SQL: ORDER BY embedding <-> query_embedding
    """
    if isinstance(query_or_vec, str):
        query_vec = embed_text(query_or_vec)
    else:
        query_vec = query_or_vec

    # Convert to pgvector literal
    qvec = _to_pgvector_str(query_vec)

    sql = f"""
    SELECT id, filename, content, embedding <-> %s AS distance
    FROM api_document
    ORDER BY distance
    LIMIT %s;
    """

    with connection.cursor() as cur:
        cur.execute(sql, [qvec, top_k])
        rows = cur.fetchall()

    results = []
    for row in rows:
        doc_id, filename, content, distance = row
        results.append({
            "id": doc_id,
            "filename": filename,
            "content": content,
            "distance": float(distance),
        })
    return results
