from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    # For adding custom fields if required
    phone_number = models.CharField(unique=True, max_length=15, null=True, blank=True)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username

