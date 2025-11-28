# backend/api/views.py

from django.http import JsonResponse
from rag_utils.engine_wrapper import ask_rag_engine # <-- CHANGE THIS IMPORT
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def ask(request):
    if request.method == "POST":
        data = json.loads(request.body)
        query = data.get("query")
        # Call the new wrapper function
        result = ask_rag_engine(query)
        return JsonResponse(result)
    return JsonResponse({"error": "POST method required"}, status=400)