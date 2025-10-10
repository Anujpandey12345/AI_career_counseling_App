from django import forms
from .models import ResumeS

class ResumeForm(forms.ModelForm):
    class Meta:
        model = ResumeS
        fields = ['name', 'email', 'resume_file']
