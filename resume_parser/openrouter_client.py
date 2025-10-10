import os
import requests
from django.conf import settings

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

def call_openrouter_for_resume(extracted_text, model="mistralai/mixtral-8x7b-instruct"):
    """
    Sends the resume text to OpenRouter and requests structured JSON using json_schema.
    Returns parsed JSON (Python dict) on success or raises an exception.
    """

    api_key = settings.OPENROUTER_API_KEY
    if not api_key:
        raise ValueError("OPENROUTER_API_KEY not configured")

    # Example JSON Schema we ask the model to return
    json_schema = {
        "name": "resume_schema",
        "schema": {
            "type": "object",
            "properties": {
                "full_name": {"type": "string"},
                "email": {"type": "string"},
                "phone": {"type": "string"},
                "summary": {"type": "string"},
                "skills": {"type": "array", "items": {"type": "string"}},
                "education": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "degree": {"type": "string"},
                            "institution": {"type": "string"},
                            "start_year": {"type": "string"},
                            "end_year": {"type": "string"}
                        }
                    }
                },
                "experience": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "title": {"type": "string"},
                            "company": {"type": "string"},
                            "start_date": {"type": "string"},
                            "end_date": {"type": "string"},
                            "description": {"type": "string"}
                        }
                    }
                }
            },
            "required": []
        }
    }

    system_prompt = {
        "role": "system",
        "content": (
            "You are a resume-parsing assistant. Extract structured information from the resume text "
            "and return ONLY JSON matching the requested json_schema. Fields: full_name, email, phone, summary, "
            "skills (array), education (array), experience (array). Location fields optional if not present."
        )
    }

    user_prompt = {
        "role": "user",
        "content": f"Extract resume information from the following resume text:\n\n{extracted_text}"
    }

    payload = {
        "model": model,
        "messages": [system_prompt, user_prompt],
        # Important: ask for structured output using the response_format parameter (json_schema).
        "response_format": {
            "type": "json_schema",
            "json_schema": json_schema
        },
        # Optional: limit tokens, temperature etc.
        "max_tokens": 1200,
        "temperature": 0.0
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        # Optional headers to attribute your app on OpenRouter's site:
        # "HTTP-Referer": "https://your-app.example.com",
        # "X-Title": "My Resume Parser App"
    }

    resp = requests.post(OPENROUTER_URL, json=payload, headers=headers, timeout=60)
    resp.raise_for_status()
    data = resp.json()

    # OpenRouter returns chat-completion style object. The structured response
    # will usually appear in data['choices'][0]['message']['content'] or in a special field.
    # The docs show structured outputs are included in the response; check the provider's returned shape.
    # Here we try to read the JSON schema result robustly:
    try:
        # Many implementations put the parsed JSON in choices[0].message.content or choices[0].content
        choice = data.get("choices", [])[0]
        # For OpenRouter structured outputs, some SDKs parse into `message` with `content` containing the json.
        message = choice.get("message") or {}
        content = message.get("content") or choice.get("content")
        # If content is a dict already (some providers return parsed), return it.
        if isinstance(content, dict):
            return content
        # Otherwise, try to parse JSON out of the content string
        import json as _json
        parsed = _json.loads(content)
        return parsed
    except Exception as e:
        # fallback: return raw data for debugging
        return {"raw_response": data}
