from django.db import models
 # if using Postgres
# If not using Postgres, use models.JSONField (Django 3.1+)
class ResumeP(models.Model):
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='resumes/')
    text = models.TextField(blank=True)
    parsed_json = models.JSONField(blank=True, null=True)
    original_filename = models.CharField(max_length=255, blank=True)


    def __str__(self):
        return f"{self.original_filename or self.file.name} ({self.uploaded_at.date()})"
