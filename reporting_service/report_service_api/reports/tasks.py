# from celery import shared_task
# from .utils import get_user_activity_data, get_weather_data, generate_pdf_report
# from .models import Report
# from django.core.files.base import ContentFile
# from django.conf import settings
# import datetime

# @shared_task
# def generate_scheduled_report():
#     user_data = get_user_activity_data()
#     print(f'\n{user_data}\n')
#     # weather_data = get_weather_data()

#     # Generating report
#     pdf_content = generate_pdf_report(user_data)

#     # Save report to the database
#     report = Report(title='Daily Report')
#     report.file.save(f'daily_report_{datetime.date.today()}.pdf', ContentFile(pdf_content))
#     report.save()

#     try:
#         with RabbitMQPublisher() as publisher:
#             message = {
#                 'report_id': report.id,
#                 'title': report.title,
#                 'created_at': str(report.created_at),
#             }
#             publisher.publish(message, queue_name='report_generated')
#     except Exception as e:
#         logger.error(f'Error publishing to RabbitMQ: {e}')



