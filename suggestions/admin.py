from django.contrib import admin
from .models import ResumeS

@admin.register(ResumeS)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'uploaded_at', 'short_suggestions')
    search_fields = ('name', 'email')
    list_filter = ('uploaded_at',)

    def short_suggestions(self, obj):
        if obj.ai_suggestions:
            return obj.ai_suggestions[:80] + "..." if len(obj.ai_suggestions) > 80 else obj.ai_suggestions
        return "No suggestions yet"
    
    short_suggestions.short_description = "AI Career Suggestions"
