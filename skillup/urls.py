# skillup/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.skill_view, name='skill_up_path'),
    path('extract/', views.extract_resume_text, name="extract"),
]
