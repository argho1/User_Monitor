import requests
from celery import shared_task
from django.conf import settings
from django.core.files.base import ContentFile
from report_service_api.rabbitmq_publisher import RabbitMQPublisher

from .models import Report
from .utils import generate_pdf_report, get_superusers_and_staff, get_user_activity_data

@shared_task(name='reports.tasks.generate_scheduled_report_n_send')
def generate_scheduled_report_n_send(frequency):
    # Fetching superusers and staff
    users_to_email = get_superusers_and_staff()

    # Fetching data for all users
    user_data = get_user_activity_data()

    # Generating report
    report_content = generate_pdf_report(user_data)

    # Save report
    report = Report(title=f'{frequency.capitalize()} User Report')
    report.file.save(f'{frequency}_user_report.pdf', ContentFile(report_content))
    report.save()

    # # Prepare message
    # message = {
    #     'name': f'{frequency.capitalize()} User Report',
    #     'report_id': report.id,
    #     'email': [user['email'] for user in users_to_email],
    #     'report_type': frequency,
    #     'status': 'success',
    # }

    # publisher = RabbitMQPublisher(queue_name='report_generated')
    # publisher.publish(message)


