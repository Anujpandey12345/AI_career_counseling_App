from django import forms
from .models import Resume

class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = [
            'full_name', 'email', 'phone', 'location',
            'linkedin', 'portfolio', 'summary',
            'experience', 'education', 'skills', 'certifications'
        ]
        widgets = {
            'summary': forms.Textarea(attrs={'rows': 3}),
            'experience': forms.Textarea(attrs={'rows': 3}),
            'education': forms.Textarea(attrs={'rows': 3}),
            'skills': forms.Textarea(attrs={'rows': 3}),
            'certifications': forms.Textarea(attrs={'rows': 3}),
        }
