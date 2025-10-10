

# Create your views here.
from django.shortcuts import render, redirect
from .forms import ResumeForm
from .models import ResumeS
from .utils import extract_text_from_resume
from .ai import get_ai_career_suggestions

def upload_resume1(request):
    if request.method == 'POST':
        form = ResumeForm(request.POST, request.FILES)
        if form.is_valid():
            resume = form.save()
            file_path = resume.resume_file.path
            text = extract_text_from_resume(file_path)
            suggestions = get_ai_career_suggestions(text)
            resume.ai_suggestions = suggestions
            resume.save()
            return render(request, 'suggestions/result1.html', {'resume': resume})
    else:
        form = ResumeForm()
    return render(request, 'suggestions/upload1.html', {'form': form})
