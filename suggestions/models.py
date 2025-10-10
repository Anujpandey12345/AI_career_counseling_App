from django.db import models

class ResumeS(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    resume_file = models.FileField(upload_to='resumes/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    ai_suggestions = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
