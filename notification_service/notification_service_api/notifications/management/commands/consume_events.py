from typing import Any
from django.core.management.base import BaseCommand
import pika
from notifications.tasks import handle_report_generated_event, handle_user_registered_event

class Command(BaseCommand):
    help = 'Consume message from RabbitMQ'

    def handle(self, *args, **options):
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        
        # Declare both queues
        channel.queue_declare(queue='user_registered', durable=True)
        channel.queue_declare(queue='report_generated', durable=True)

        # Callback for user_registered queue
        def user_registered_callback(ch, method, properties, body):
            try:
                handle_user_registered_event.delay(body.decode())
                ch.basic_ack(delivery_tag=method.delivery_tag)
            except Exception as e:
                print(f'Error in user_registered_callback: {e}')
                ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

        # Callback for report_generated queue
        def report_generated_callback(ch, method, properties, body):
            try:
                handle_report_generated_event.delay(body.decode())
                ch.basic_ack(delivery_tag=method.delivery_tag)
            except Exception as e:
                print(f'Error in user_registered_callback: {e}')
                ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)


        channel.basic_consume(
            queue='user_registered',
            on_message_callback=user_registered_callback,
            auto_ack=False,
        )

        channel.basic_consume(
            queue='report_generated',
            on_message_callback=report_generated_callback,
            auto_ack=False,
        )

        print(' [*] Waiting for message. To exit press CTRL+C ')
        channel.start_consuming()





