import json
from django.template.loader import render_to_string
from celery import shared_task
from .utils import get_report_file, send_email, send_sms

@shared_task(name='notifications.tasks.handle_user_registered_event')
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


@shared_task(name='notifications.tasks.handle_report_generated_event')
def handle_report_generated_event(message):
    event = json.loads(message)
    email = event.get('email')
    report_id = event.get('report_id')
    report_type = event.get('report_type')

    report_content = get_report_file(report_id)
    if not report_content:
        return
    
    subject = f'Your {report_type} Report'
    content = 'Please find your report attached.'

    send_email(to_email=email, subject=subject, content=content, attachment=report_content)


