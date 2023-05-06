from dataclasses import dataclass
from typing import Any


@dataclass
class BaseMessage:
    exchange_name: str
    routing_key: str
    message: Any


class DevActivationMessage(BaseMessage):
    exchange_name = 'dev_activation_exchange'
    routing_key = 'dev_activation_queue'


class ClientActivationMessage(BaseMessage):
    exchange_name = 'client_activation_exchange'
    routing_key = 'client_activation_queue'


class OwnerAccessMessage(BaseMessage):
    exchange_name = 'owner_access_exchange'
    routing_key = 'owner_access_queue'


class DevAccessMessage(BaseMessage):
    exchange_name = 'dev_access_exchange'
    routing_key = 'dev_access_queue'


class FriendAddedMessage(BaseMessage):
    exchange_name = 'friend_added_exchange'
    routing_key = 'friend_added_queue'
