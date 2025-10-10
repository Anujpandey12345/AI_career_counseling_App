import requests
from django.conf import settings

def generate_ai_summary(prompt):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "model": "mistralai/mixtral-8x7b-instruct",
        "messages": [
            {"role": "system", "content": "You are an expert resume writer."},
            {"role": "user", "content": prompt},
        ],
    }

    response = requests.post(url, headers=headers, json=data)
    result = response.json()
    return result["choices"][0]["message"]["content"]
