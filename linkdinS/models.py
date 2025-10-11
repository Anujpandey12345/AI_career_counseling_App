from django.db import models

# Create your models here.


class resumeL(models.Model):
    name = models.CharField(max_length=100)
    resume_file = models.FileField(upload_to='resumes/')
    linkdin_summary = models.TextField(blank=True, null=True)
    upload_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.name