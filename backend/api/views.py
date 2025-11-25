from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import ollama

@csrf_exempt
def chat(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_message = data.get("message", "")

        # Call Ollama Phi model
        response = ollama.chat(
            model="phi3.5",
            messages=[{"role": "user", "content": user_message}]
        )

        bot_reply = response['message']['content']
        return JsonResponse({"reply": bot_reply})

    return JsonResponse({"error": "POST only"}, status=400)
