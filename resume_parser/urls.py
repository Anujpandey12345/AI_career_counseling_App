from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_resume, name='upload_resume'),
    path('resume/<int:pk>/', views.resume_detail, name='resume_detail'),
]
