import pika
import json
from django.conf import settings

class RabbitMQPublisher:
    def __init__(self, queue_name):
        self.queue_name = queue_name


    def __enter__(self):
        # credentials = pika.PlainCredentials(settings.RABBITMQ_USER, settings.RABBITMQ_PASSWORD)
        parameters = pika.ConnectionParameters(
            host=settings.RABBITMQ_HOST,
            # port=settings.RABBITMQ_PORT,
            # credentials=credentials,
            heartbeat=600, # Heartbeat in sec
            blocked_connection_timeout=300, # Timeout when blocked in sec
        )
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue_name, durable=True)
        return self
        

    def publish(self, message):
        self.channel.basic_publish(
            exchange='',
            routing_key=self.queue_name,
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=2,
                content_type='application/json'
            )
        )
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.connection.close()






