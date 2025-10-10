from django.contrib import admin
from .models import Resume

@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone', 'user')
    search_fields = ('full_name', 'email', 'skills', 'education')
    list_filter = ('user',)
