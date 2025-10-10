from django.urls import path
from . import views

urlpatterns = [
    path('chat/', views.chat_page, name='chat_page'),  # for GET (page render)
    path('chat/api/', views.chat_with_ai, name='chat_api'),  # for POST (AJAX call)
]
