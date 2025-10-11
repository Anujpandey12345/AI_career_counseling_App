from django.urls import path
from . import views

urlpatterns = [
    path('', views.linkdin_summary_view, name='linkedin_summary'),
]
