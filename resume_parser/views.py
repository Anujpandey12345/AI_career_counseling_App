from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from .forms import ResumeUploadForm
from .models import ResumeP
from .utils import extract_text
from .openrouter_client import call_openrouter_for_resume

def upload_resume(request):
    if request.method == 'POST':
        form = ResumeUploadForm(request.POST, request.FILES)
        if form.is_valid():
            resume = form.save(commit=False)
            resume.original_filename = request.FILES['file'].name
            resume.save()
            # extract text
            text = extract_text(resume.file)
            resume.text = text
            resume.save()

            # call OpenRouter (may take 1-5 seconds)
            try:
                parsed = call_openrouter_for_resume(text)
                resume.parsed_json = parsed
                resume.save()
            except Exception as e:
                # capture error (in production, log properly)
                resume.parsed_json = {"error": str(e)}
                resume.save()

            return redirect('resume_detail', pk=resume.pk)
    else:
        form = ResumeUploadForm()
    return render(request, 'resume_parser/upload.html', {'form': form})

def resume_detail(request, pk):
    resume = get_object_or_404(ResumeP, pk=pk)
    return render(request, 'resume_parser/detail.html', {'resume': resume})
