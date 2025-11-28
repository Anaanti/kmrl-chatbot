from django.http import JsonResponse
from rag_utils.query_llm import answer_query
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def ask(request):
    if request.method == "POST":
        data = json.loads(request.body)
        query = data.get("query")
        result = answer_query(query)
        return JsonResponse(result)
    return JsonResponse({"error": "POST method required"}, status=400)
