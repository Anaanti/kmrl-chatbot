# backend/rag_utils/search.py

import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()  # loads DB credentials from .env

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT", 5432)  # default Postgres port

TOP_K = 3  # number of top results to return

def search_similar(query_embedding):
    """
    Fetch top-k documents from PostgreSQL whose embeddings are closest to query_embedding.
    Assumes your documents table has columns: id, filename, content, embedding (pgvector)
    """
    results = []

    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )

    cursor = conn.cursor(cursor_factory=RealDictCursor)

    # Make query_embedding a string representation for pgvector
    query_embedding_str = "[" + ",".join(str(x) for x in query_embedding) + "]"

    sql = f"""
        SELECT id, filename, content, embedding <#> '{query_embedding_str}' AS distance
        FROM documents
        ORDER BY distance ASC
        LIMIT {TOP_K};
    """

    cursor.execute(sql)
    rows = cursor.fetchall()

    for row in rows:
        results.append({
            "id": row["id"],
            "filename": row["filename"],
            "content": row["content"],
            "distance": row["distance"]
        })

    cursor.close()
    conn.close()

    return results
