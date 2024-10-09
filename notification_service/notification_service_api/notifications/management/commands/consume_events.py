from typing import Any
from django.core.management.base import BaseCommand
import pika
from notifications.tasks import handle_user_registered_event

class Command(BaseCommand):
    help = 'Consume message from RabbitMQ'

    def handle(self, *args, **options):
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        channel.queue_declare(queue='user_registered')

        def callback(ch, method, properties, body):
            handle_user_registered_event.delay(body.decode())

        channel.basic_consume(queue='user_registered', on_message_callback=callback, auto_ack=False)
        print(' [*] waiting for message. To exit press CTRL+C ')
        channel.start_consuming()