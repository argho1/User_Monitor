from django.db import models

class UserNotificationPreferance(models.Model):
    user_id = models.IntegerField(unique=True)
    email_enabled = models.BooleanField(default=True)
    sms_enabled = models.BooleanField(default=True)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)




