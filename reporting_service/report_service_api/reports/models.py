from django.db import models

class Report(models.Model):
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='reports/generated_reports/')