from django import forms
from .models import resumeL


class resumeForm(forms.ModelForm):
    class Meta:
        model = resumeL
        fields = ['name', 'resume_file']