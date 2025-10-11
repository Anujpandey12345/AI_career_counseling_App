from django.shortcuts import render
from .models import UserSkillRoadmap
from .forms import SkillUp
import requests
from django.conf import settings
import PyPDF2
import docx
from django.contrib.auth.decorators import login_required

# Function to extract text from PDF, DOCX, or TXT

def extract_resume_text(file):
    # PDF
    if file.name.endswith('.pdf'):
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        return text.strip()

    # DOCX
    elif file.name.endswith('.docx'):
        doc = docx.Document(file)
        text = '\n'.join([para.text for para in doc.paragraphs])
        return text.strip()

    # TXT fallback
    else:
        return file.read().decode('utf-8', errors='ignore').strip()

@login_required(login_url='login')
def skill_view(request):
    roadmap = None
    if request.method == "POST":
        form = SkillUp(request.POST, request.FILES)
        if form.is_valid():
            user_obj = form.save(commit=False)
            resume_file = request.FILES['resume']
            resume_text = extract_resume_text(resume_file)

            if not resume_text:
                roadmap = ("It seems that your resume could not be read. "
                           "Please provide details manually: Current Job, Skills, Career Goals, "
                           "Areas of Interest, and Education.")
            else:
                # Call OpenRouter API
                headers = {
                    "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
                    "Content-Type": "application/json"
                }

                data = {
                    "model": "gpt-4o-mini",
                    "messages": [
                        {"role": "system", "content": "You are a career advisor AI."},
                        {"role": "user", "content": f"Analyze this resume and provide a customized AI skill-up learning roadmap:\n\n{resume_text}"}
                    ],
                    "temperature": 0.7
                }

                response = requests.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    json=data,
                    headers=headers
                )

                # Safely extract the response
                try:
                    result = response.json()
                    roadmap = result['choices'][0]['message']['content']
                except Exception:
                    roadmap = "Sorry, something went wrong while generating your roadmap. Please try again."

            user_obj.roadmap = roadmap
            user_obj.save()

    else:
        form = SkillUp()

    return render(request, 'skillup/skill.html', {'form': form, 'roadmap': roadmap})
