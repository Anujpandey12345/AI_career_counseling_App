from django import forms
from .models import ResumeP

class ResumeUploadForm(forms.ModelForm):
    class Meta:
        model = ResumeP
        fields = ['file']
