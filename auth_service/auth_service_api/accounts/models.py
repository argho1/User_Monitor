from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser


class Role(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        permissions = [
            ("create_report", "Can create a report"),
            ("delete_report", "Can delete a report"),
            ("view_report", "Can view a report"),
        ]


class CustomUser(AbstractUser):
    # For adding custom fields if required
    phone_number = models.CharField(unique=True, max_length=15)
    email = models.EmailField(unique=True)
    roles = models.ManyToManyField('Role', related_name='users')

    def __str__(self):
        return self.username


class NotificationPreferences(models.Model):
    user = models.OneToOneField(CustomUser, 
                                on_delete=models.CASCADE, 
                                related_name='notification_preferences')
    email_notification = models.BooleanField(default=True)
    sms_notification = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} - Notification Preferences'

# Creates NotificationPreferences instance when a CustomUser is created
@receiver(post_save, sender=CustomUser)
def create_notification_preferences(sender, instance, created, **kwargs):
    if created:
        NotificationPreferences.objects.create(user=instance)

