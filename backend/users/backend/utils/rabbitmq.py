import pika


class RabbitMQ:
    def __init__(self, host, port, username, password, exchange_name):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.exchange_name = exchange_name

        credentials = pika.PlainCredentials(self.username, self.password)
        parameters = pika.ConnectionParameters(
            host=self.host,
            port=self.port,
            virtual_host='/',
            credentials=credentials
        )
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange=self.exchange_name, exchange_type='fanout')

    def publish(self, message):
        self.channel.basic_publish(
            exchange=self.exchange_name,
            routing_key='',
            body=message
        )

    def close(self):
        self.connection.close()
