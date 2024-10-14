import json
from django.conf import settings
from django.template.loader import render_to_string
from celery import shared_task

from .utils import get_report_file, send_email, send_sms, get_user_notification_perference

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

    phone_number = '+91'+event.get('phone_number')

    sms_content = f'Hello {username}, thank you for registering!'
    
    # Send SMS
    send_sms(to_number=phone_number, message=sms_content)


@shared_task(name='notifications.tasks.handle_report_generated_event')
def handle_report_generated_event(message):
    event = json.loads(message)
    email = event.get('email')
    report_id = event.get('report_id')
    report_type = event.get('report_type')
    phone_number = '+91'+event.get('phone_number')
    user_id = event.get('user_id')

    # get report file
    report_content = get_report_file(report_id)
    if not report_content:
        return
    
    notification_perference = get_user_notification_perference(user_id) 

    if notification_perference == None:
        return 'xxxxx FAILED TO GET NOTIFICATION PREFERENCES!! xxxxx'

    if notification_perference['email_notification'] and email:
        subject = f'Your {report_type} Report'
        content = 'Please find your report attached.'
        send_email(to_email=email, 
                subject=subject, 
                content=content, 
                attachment=report_content)
        
    if notification_perference['sms_notification'] and event.get('phone_number'):
        sms_content = f"Your {report_type} Report is ready to be downloaded at f'{settings.REPORTING_API_URL}{report_id}/download/'"
        send_sms(to_number=phone_number, message=sms_content)
    



