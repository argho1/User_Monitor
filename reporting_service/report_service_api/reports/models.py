from django.db import models

class Report(models.Model):
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='reports/generated_reports/')

    # class Meta:
    #     permissions = [
    #         ('view_report', 'Can view report'),
    #         ('delete_report', 'Can delete report'),
    #     ]

    def __str__(self):
        return self.title



