from django.db import models
from django.contrib.auth.models import User

class Resume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    location = models.CharField(max_length=200, blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    portfolio = models.URLField(blank=True, null=True)
    summary = models.TextField(blank=True, null=True)
    experience = models.TextField(blank=True, null=True)
    education = models.TextField(blank=True, null=True)
    skills = models.TextField(blank=True, null=True)
    certifications = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name
