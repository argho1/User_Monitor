import pika
import json
from django.conf import settings
from . import config

class RabbitMQPublisher:
    def __init__(self):
        # credentials = pika.PlainCredentials(config.RABBITMQ_USER, config.RABBITMQ_PASSWORD)
        parameters = pika.ConnectionParameters(
            host=config.RABBITMQ_HOST,
            # port=config.RABBITMQ_PORT,
            # credentials=credentials,
            heartbeat=600, # Heartbeat in sec
            blocked_connection_timeout=300, # Timeout when blocked in sec
        )
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=config.RABBITMQ_QUEUE, durable=True)

    def publish(self, message):
        self.channel.basic_publish(
            exchange='',
            routing_key=config.RABBITMQ_QUEUE,
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=2,
                content_type='application/json'
            )
        )
    
    def close(self):
        self.connection.close()






