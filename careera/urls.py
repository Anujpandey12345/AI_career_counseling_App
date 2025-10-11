from django.contrib import admin
from django.urls import path,include
from careera import views

urlpatterns = [
    path('', views.index, name='indexhome'),
    path('signup/', views.signup, name='signup'),
    path('term&condition/', views.term_condition, name='term_condition'),
    path('login/', views.LoginView, name='login'),
    path('logout/', views.LogoutView, name='logout'),
    path('resume-builder/', views.resume_builder, name='resume_builder'),
    path("resume/<int:resume_id>/download_pdf/", views.download_pdf, name="download_pdf"),
    path('forget/', views.ForgetPassword, name='Forget_pass'),
    path('newpass/<str:user>/', views.NewPasswordPage, name='new_pass'),
    path('stats-api/', views.stats_api, name='stats_api'),


]