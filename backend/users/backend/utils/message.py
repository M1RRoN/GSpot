from abc import ABC, abstractmethod

from utils.rabbitmq import RabbitMQ


class BaseMessage(ABC):
    @abstractmethod
    def send(self):
        pass


class DevActivationMessage(BaseMessage):
    def __init__(self, message):
        self.message = message

    def send(self):
        rabbitmq = RabbitMQ(
            host='localhost',
            port=5672,
            username='guest',
            password='guest',
            exchange_name='dev_activation_exchange'
        )
        rabbitmq.publish(self.message)
        rabbitmq.close()


class ClientActivationMessage(BaseMessage):
    def __init__(self, message):
        self.message = message

    def send(self):
        rabbitmq = RabbitMQ(
            host='localhost',
            port=5672,
            username='guest',
            password='guest',
            exchange_name='client_activation_exchange'
        )
        rabbitmq.publish(self.message)
        rabbitmq.close()


class OwnerAccessMessage(BaseMessage):
    def __init__(self, message):
        self.message = message

    def send(self):
        rabbitmq = RabbitMQ(
            host='localhost',
            port=5672,
            username='guest',
            password='guest',
            exchange_name='owner_access_exchange'
        )
        rabbitmq.publish(self.message)
        rabbitmq.close()


class DevAccessMessage(BaseMessage):
    def __init__(self, message):
        self.message = message

    def send(self):
        rabbitmq = RabbitMQ(
            host='localhost',
            port=5672,
            username='guest',
            password='guest',
            exchange_name='dev_access_exchange'
        )
        rabbitmq.publish(self.message)
        rabbitmq.close()


class FriendAddedMessage(BaseMessage):
    def __init__(self, message):
        self.message = message

    def send(self):
        rabbitmq = RabbitMQ(
            host='localhost',
            port=5672,
            username='guest',
            password='guest',
            exchange_name='friend_added_exchange'
        )
        rabbitmq.publish(self.message)
        rabbitmq.close()
