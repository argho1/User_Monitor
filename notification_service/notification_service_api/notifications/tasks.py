import json
from django.template.loader import render_to_string
from celery import shared_task
from .utils import send_email, send_sms

@shared_task
def handle_user_registered_event(message):
    event = json.loads(message)
    email = event.get('email')
    username = event.get('username')

    context = {
        'username': username,
    }

    # Notification content
    subject = "Welcome to Our Service"
    content = render_to_string('welcome_message.txt', context)

    # Send email
    
    send_email(to_email=email, subject=subject, content=content)

    ##Send SMS

    # phone_number = event.get('phone_number')
    # sms_content = f'Hello {username}, thank you for registering!'
    # send_sms(to_number=phone_number, message=sms_content)