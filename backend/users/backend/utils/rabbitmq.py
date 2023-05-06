import pika

from config.settings.rabbitmq import RABBITMQ_HOST, RABBITMQ_PORT, RABBITMQ_USERNAME, RABBITMQ_PASSWORD


class RabbitMQ:
    def __init__(self, exchange_name, queue_name):
        self.host = RABBITMQ_HOST
        self.port = RABBITMQ_PORT
        self.username = RABBITMQ_USERNAME
        self.password = RABBITMQ_PASSWORD
        self.exchange_name = exchange_name
        self.queue_name = queue_name

        credentials = pika.PlainCredentials(self.username, self.password)
        parameters = pika.ConnectionParameters(
            host=self.host,
            port=self.port,
            virtual_host='/',
            credentials=credentials
        )
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()

    def publish(self, message: str) -> None:
        self.channel.basic_publish(
            exchange=self.exchange_name,
            routing_key=self.queue_name,
            body=message.encode()
        )
