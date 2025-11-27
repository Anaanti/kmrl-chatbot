# rag_utils/embeddings_store.py
from django.db import connection

def store_embedding(filename, chunk_text, embedding):
    emb_str = "[" + ",".join(str(x) for x in embedding) + "]"
    with connection.cursor() as cur:
        cur.execute("""
            INSERT INTO documents (filename, content, embedding)
            VALUES (%s, %s, %s::vector)
        """, [filename, chunk_text, emb_str])
