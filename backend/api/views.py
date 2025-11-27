# backend/api/views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rag_utils.llm import ask_llm 

@csrf_exempt  # allows POST requests without CSRF token
def ask(request):
    if request.method == "POST":
        query = request.POST.get("query", "").strip()
        if not query:
            return JsonResponse({"error": "No query provided"}, status=400)

        # Call Llama 3 via our new wrapper
        answer = ask_llm(query)

        # Return as JSON
        return JsonResponse({
            "answer": answer,
            "sources": [],      # you can keep empty if not using documents
            "distances": []     # same here
        })
    else:
        return JsonResponse({"error": "Only POST requests allowed"}, status=405)
