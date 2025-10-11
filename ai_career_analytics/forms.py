from django import forms
from .models import CareerAnalytics


class CareerForm(forms.ModelForm):
    class Meta:
        model = CareerAnalytics
        fields = ['name', 'resume']