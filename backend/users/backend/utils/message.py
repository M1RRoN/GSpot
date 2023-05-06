from abc import ABC

from utils.rabbitmq import RabbitMQ


class BaseMessage(ABC):
    def __init__(self, message: str, exchange_name: str, queue_name: str) -> None:
        self.message = message
        self.exchange_name = exchange_name
        self.queue_name = queue_name

    def send(self) -> None:
        with RabbitMQ(
                exchange_name=self.exchange_name,
                queue_name=self.queue_name
        ) as rabbitmq:
            rabbitmq.publish(self.message)


class DevActivationMessage(BaseMessage):
    def __init__(self, message: str) -> None:
        super().__init__(message, 'dev_activation_exchange', 'dev_activation_queue')


class ClientActivationMessage(BaseMessage):
    def __init__(self, message: str) -> None:
        super().__init__(message, 'client_activation_exchange', 'client_activation_queue')


class OwnerAccessMessage(BaseMessage):
    def __init__(self, message: str) -> None:
        super().__init__(message, 'owner_access_exchange', 'owner_access_queue')


class DevAccessMessage(BaseMessage):
    def __init__(self, message: str) -> None:
        super().__init__(message, 'dev_access_exchange', 'dev_access_queue')


class FriendAddedMessage(BaseMessage):
    def __init__(self, message: str) -> None:
        super().__init__(message, 'friend_added_exchange', 'friend_added_queue')
