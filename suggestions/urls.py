from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_resume1, name='upload_resume1'),
]
