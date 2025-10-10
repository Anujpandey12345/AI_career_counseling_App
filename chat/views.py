# chat/views.py
from django.shortcuts import render
from django.http import JsonResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import requests
import json
import traceback
from functools import wraps

def login_required_json(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({"error": "Please login then I can help you."}, status=401)
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def chat_page(request):
    """
    Render the chat UI page.
    """
    return render(request, 'chat/chat.html')

@csrf_exempt  # Only for development — REMOVE in production and handle CSRF properly
@login_required_json  # Custom login check that returns JSON error if not logged in
def chat_with_ai(request):
    """
    Handle chat messages with AI — only accessible by logged-in users.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '')

            print("Received user message:", user_message)  # Debug log

            headers = {
                "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
                "HTTP-Referer": "http://127.0.0.1:8000",
                "X-Title": "AI Customer Assistant",
                "Content-Type": "application/json"
            }

            payload = {
                "model": "openai/gpt-4o",
                "messages": [
                    {"role": "system", "content": "You are a helpful AI assistant for customer support."},
                    {"role": "user", "content": user_message}
                ]
            }

            print("Payload:", json.dumps(payload, indent=2))  # Debug log

            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                data=json.dumps(payload)
            )

            print("API status code:", response.status_code)
            print("API response:", response.text)

            if response.status_code == 200:
                ai_reply = response.json()["choices"][0]["message"]["content"]
                return JsonResponse({"reply": ai_reply})
            else:
                return JsonResponse({
                    "error": "Failed to fetch response from OpenRouter API",
                    "details": response.text
                }, status=500)

        except Exception as e:
            traceback.print_exc()
            return JsonResponse({
                "error": "Something went wrong",
                "details": str(e)
            }, status=500)

    return HttpResponseNotAllowed(['POST'], "Only POST method is allowed.")
