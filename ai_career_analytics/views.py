from django.shortcuts import render
import fitz  # PyMuPDF
from .models import CareerAnalytics
from .forms import CareerForm
from django.conf import settings
import requests
from django.contrib.auth.decorators import login_required
# ----------------------------
# Extract text from uploaded PDF
# ----------------------------
# @login_required(login_url='login')
def extract_text_from_pdf(file):
    text = ""
    with fitz.open(stream=file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text


# ----------------------------
# Main Career Analytics View
# ----------------------------


@login_required(login_url='login')
def career_analytics_view(request):
    analytics = None

    if request.method == "POST":
        form = CareerForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            resume_file = request.FILES["resume"]
            resume_text = extract_text_from_pdf(resume_file)

            # ----------------------------
            # OpenRouter API Call
            # ----------------------------
            headers = {
                # ✅ Added space after 'Bearer'
                "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
                # ✅ Required headers for OpenRouter
                "HTTP-Referer": "http://localhost:8000",
                "X-Title": "AI Career Analytics",
            }

            data = {
                # ✅ Use a model that actually exists on OpenRouter
                "model": "gpt-4o-mini",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are an AI career analytics expert who analyzes resumes and provides career insights.",
                    },
                    {
                        "role": "user",
                        "content": f"Analyze this resume text and provide detailed insights including career growth potential, skill gaps, salary trends, and upskilling recommendations:\n\n{resume_text}",
                    },
                ],
            }

            try:
                response = requests.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers=headers,
                    json=data,
                    timeout=60,
                )

                if response.status_code == 200:
                    result = response.json()["choices"][0]["message"]["content"]
                    obj.insights = result
                    obj.save()
                    analytics = result
                else:
                    # ✅ Show API error text for debugging
                    analytics = f"❌ API Error {response.status_code}: {response.text}"

            except Exception as e:
                analytics = f"⚠️ Exception occurred: {str(e)}"

    else:
        form = CareerForm()

    return render(
        request,
        "ai_career_analytics/career_analytics.html",
        {"form": form, "analytics": analytics},
    )
