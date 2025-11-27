import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
from .embeddings import get_embedding

@csrf_exempt
def ask_rag(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=400)

    try:
        data = json.loads(request.body)
        query = data.get("query", "")
        if not query:
            return JsonResponse({"error": "Query missing"}, status=400)

        # Step 1: Embed query
        query_vec = get_embedding(query)

        # Convert Python list → pgvector-compatible string
        query_vec_str = "[" + ",".join(str(x) for x in query_vec) + "]"

        # Step 2: Query Postgres using pgvector similarity
        with connection.cursor() as cur:
            cur.execute("""
                SELECT filename, content
                FROM documents
                ORDER BY embedding <-> %s::vector
                LIMIT 1;
            """, [query_vec])


            row = cur.fetchone()

        if not row:
            return JsonResponse({"error": "No documents found."})

        filename, content = row
        return JsonResponse({
            "query": query,
            "best_match": filename,
            "context": content
        })

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
