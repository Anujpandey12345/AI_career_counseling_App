from django.shortcuts import render
import requests
from .forms import resumeForm
from .models import resumeL
from django.conf import settings
from django.contrib.auth.decorators import login_required



@login_required(login_url='login')
def linkdin_summary_view(request):
    summary = None
    debug_info = None  # For debugging API response

    if request.method == "POST":
        form = resumeForm(request.POST, request.FILES)
        if form.is_valid():
            resume_obj = form.save()

            # Read resume file content
            resume_file = resume_obj.resume_file
            resume_file.seek(0)
            resume_text = resume_file.read().decode('utf-8', errors='ignore')

            api_key = settings.OPENROUTER_API_KEY

            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            }

            data = {
                "model": "gpt-4o-mini",  # Ensure this model exists in your OpenRouter plan
                "messages": [
                    {"role": "system", "content": "You are a professional LinkedIn summary writer."},
                    {"role": "user", "content": f"Generate a concise professional LinkedIn summary for this resume:\n\n{resume_text}"}
                ]
            }

            try:
                response = requests.post(
                    "https://openrouter.ai/api/v1/chat/completions",  # ✅ Correct endpoint
                    headers=headers,
                    json=data,
                    timeout=60
                )

                debug_info = response.text  # Save raw response for debugging

                # Handle empty or error responses
                if not response.text:
                    summary = "Error: Empty response from OpenRouter API"
                elif response.status_code != 200:
                    summary = f"Error: OpenRouter API returned {response.status_code} - {response.text}"
                else:
                    try:
                        result_json = response.json()
                        summary = result_json['choices'][0]['message']['content']
                    except (ValueError, KeyError, IndexError):
                        summary = f"Error: Unexpected JSON response from OpenRouter API:\n{response.text}"

            except requests.exceptions.RequestException as e:
                summary = f"Error generating summary: {e}"

            # Save summary to database
            resume_obj.summary = summary
            resume_obj.save()
    else:
        form = resumeForm()

    return render(request, 'linkdinS/linkdin_summary.html', {
        'form': form,
        'summary': summary,
        'debug_info': debug_info  # Optional: display in template for debugging
    })
