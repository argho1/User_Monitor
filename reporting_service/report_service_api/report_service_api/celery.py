from __future__ import absolute_import
import os
from celery import Celery
from kombu import Queue

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'report_service_api.settings')

app = Celery('report_service_api')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.broker_connection_retry_on_startup = True


# Define the queue for the report service
app.conf.task_queues = (
    Queue('report_tasks', routing_key='report.#'),
)


# Route the tasks for the report service to the correct queue
app.conf.task_routes = {
    'reports.tasks.generate_scheduled_report_n_send': {
        'queue': 'report_tasks',
        'routing_key': 'report.scheduled'
    },
}