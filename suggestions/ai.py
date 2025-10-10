import requests
import json
from django.conf import settings
def get_ai_career_suggestions(resume_text):
    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
    "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
    "Content-Type": "application/json"
    }

    prompt = f"""
    You are a professional career advisor.
    Analyze this resume text and suggest 3–5 career paths suitable for this person.
    Give brief explanations for each suggestion based on their skills and experience.
    
    Resume Text:
    {resume_text}
    """

    data = {
        "model": "gpt-4o-mini",  # or another OpenRouter model you prefer
        "messages": [
            {"role": "system", "content": "You are an AI career counselor."},
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # raise an error if HTTP status != 200
        result = response.json()

        # Debugging print — optional
        print("AI Response:", json.dumps(result, indent=2))

        # Safely check if 'choices' exist
        if 'choices' in result and len(result['choices']) > 0:
            return result['choices'][0]['message']['content']
        elif 'error' in result:
            return f"❌ AI API Error: {result['error'].get('message', 'Unknown error')}"
        else:
            return "⚠️ Unexpected response from AI model. Please try again."
    except requests.exceptions.RequestException as e:
        return f"🚫 Request error: {e}"
    except Exception as e:
        return f"⚠️ Unexpected error: {e}"
