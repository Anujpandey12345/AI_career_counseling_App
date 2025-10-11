from django.shortcuts import render, redirect
from careerc.forms  import CreateUserForm
from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
# Create your views here.
def index(request):
    return render(request, 'careera/index.html')

    
def term_condition(request):
    return render(request, 'careera/term&condition.html')


def signup(request):
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            return render(request, 'careera/signUp.html', {'form': form})
    else:
        form = CreateUserForm()
    return render(request, 'careera/signUp.html', {'form': form})


def LoginView(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        print("Username", username)
        print("Password", password)

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            print("Login Done !!")
            return redirect('/')
        else:
            print("Some error")

    context = {}
    return render(request, 'careera/login.html', context)

def LogoutView(request):
    logout(request)
    print("Logout SuccessFully")
    return redirect('indexhome')




from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template.loader import get_template
from weasyprint import HTML
import tempfile
from django.core.mail import send_mail
from django.conf import settings

from .models import Resume
from .forms import ResumeForm
from .utils import generate_ai_summary

@login_required(login_url='login')
def resume_builder(request):
    ai_summary = ""
    if request.method == "POST":
        form = ResumeForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            # If user clicked AI summary generation
            if 'generate_summary' in request.POST:
                prompt = f"Write a professional resume summary based on: {data}"
                ai_summary = generate_ai_summary(prompt)
                data['summary'] = ai_summary
                form = ResumeForm(initial=data)
            else:
                # Save resume and show preview
                resume = form.save()
                return render(request, "careera/resume_preview.html", {"resume": resume})
    else:
        form = ResumeForm()

    return render(request, "careera/resume_form.html", {"form": form, "ai_summary": ai_summary})

@login_required(login_url='login')
def download_pdf(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id)
    template_path = 'careera/resume_preview.html'
    context = {'resume': resume}

    # Render HTML template with context data
    template = get_template(template_path)
    html = template.render(context)

    # Create a PDF response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{resume.full_name}_Resume.pdf"'

    # Generate PDF using WeasyPrint (supports CSS & inline styling)
    with tempfile.NamedTemporaryFile(delete=True) as temp_pdf:
        HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(target=response)

    return response





def ForgetPassword(request):
    if request.method == "POST":
        email = request.POST.get("email")
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            print("User Exist", "Email :" , email)
            send_mail("Reset Your Password : ", f"Hey Ai Career Counsloe User : {user} ! for reset the password click on given link \n http://127.0.0.1:8000/newpass/{user}/",  settings.EMAIL_HOST_USER, [email], fail_silently=True)
            return render(request, "careera/passSend.html")

        return render(request, "careera/forgetPass.html")
    return render(request, "careera/forgetPass.html")




def NewPasswordPage(request, user):
    userid = User.objects.get(username=user)
    print("UserId :", userid)
    if request.method == "POST":
        pass1 = request.POST.get("password1")
        pass2 = request.POST.get("password2")

        print("Pass1 and Pass2 : ", pass1, pass2)
        if pass1 == pass2:
            userid.set_password(pass1)
            userid.save()
            return render(request, "careera/passchange.html")

    return render(request, "careera/newpass.html")




from resume_parser.models import ResumeP
from django.http import JsonResponse
from skillup.models import UserSkillRoadmap

def stats_api(request):
    total_resumes = ResumeP.objects.count()
    total_career_paths = UserSkillRoadmap.objects.count()

    data = {
        "total_resumes": total_resumes,
        "accuracy_rate": 95,  # Static for now
        "total_career_paths": total_career_paths
    }
    return JsonResponse(data)

