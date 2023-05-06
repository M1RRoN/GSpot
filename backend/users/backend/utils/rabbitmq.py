import pika

from config.settings.rabbitmq import RABBITMQ_HOST, RABBITMQ_PORT, RABBITMQ_USERNAME, RABBITMQ_PASSWORD
from utils.message import BaseMessage


class RabbitMQ:
    def __init__(self, exchange_name: str, queue_name: str):
        self.host = RABBITMQ_HOST
        self.port = RABBITMQ_PORT
        self.username = RABBITMQ_USERNAME
        self.password = RABBITMQ_PASSWORD
        self.exchange_name = exchange_name
        self.queue_name = queue_name

    def __enter__(self):
        credentials = pika.PlainCredentials(self.username, self.password)
        parameters = pika.ConnectionParameters(
            host=self.host,
            port=self.port,
            virtual_host='/',
            credentials=credentials
        )
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()

    def send_message(self, message: BaseMessage) -> None:
        self.channel.basic_publish(
            exchange=message.exchange_name,
            routing_key=message.routing_key,
            body=str(message.message).encode()
        )

# Пример использования:
# def publish():
#     message = DevActivationMessage(message={'id': 1})
#     with RabbitMQ(exchange_name=message.exchange_name, queue_name=message.routing_key) as client:
#         client.send_message(message)
