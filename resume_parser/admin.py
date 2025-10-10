from django.contrib import admin
from .models import ResumeP

@admin.register(ResumeP)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ('id', 'original_filename', 'uploaded_at')
    readonly_fields = ('uploaded_at', 'text', 'parsed_json')
    search_fields = ('original_filename',)
    list_filter = ('uploaded_at',)
