from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from kombu import Queue

CELERY_QUEUES = (
    Queue('user_registered', routing_key='user.registered'),
    Queue('report_generated', routing_key='report.generated'),
)

CELERY_ROUTES = {
    'notifications.tasks.handle_user_registered_event': {'queue': 'user_registered', 
                                                         'routing_key': 'user.registered'},
    'notifications.tasks.handle_report_generated_event': {'queue': 'report_generated', 
                                                          'routing_key': 'report.generated'},
}

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'notification_service_api.settings')

# Create an instance of the Celery application.
app = Celery('notification_service_api')

# Load task modules from all registered Django app configs.
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.broker_connection_retry_on_startup = True