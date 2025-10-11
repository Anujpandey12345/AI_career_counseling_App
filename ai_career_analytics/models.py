from django.db import models

# Create your models here.
class CareerAnalytics(models.Model):
    name = models.CharField(max_length=100)
    resume = models.FileField(upload_to='resumes/')
    created_at = models.DateTimeField(auto_now_add=True)
    insights = models.TextField(blank=True, null=True)


    def __str__(self):
        return self.name