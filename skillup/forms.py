# skillup/forms.py
from django import forms
from .models import UserSkillRoadmap  # make sure this exists

class SkillUp(forms.ModelForm):
    class Meta:
        model = UserSkillRoadmap  # must specify the model
        fields = ['name', 'resume']  # the fields you want in the form
