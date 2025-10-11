from django.urls import path
from .views import career_analytics_view

urlpatterns = [
    path('', career_analytics_view, name='career_analytics'),
]
