from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    # For adding custom fields if required
    pass

    def __str__(self):
        return self.username

