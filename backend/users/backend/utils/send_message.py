from message import DevActivationMessage, ClientActivationMessage, OwnerAccessMessage, DevAccessMessage, FriendAddedMessage


def send_message(message_type, message):
    if message_type == 'dev_activation':
        DevActivationMessage(message).send()
    elif message_type == 'client_activation':
        ClientActivationMessage(message).send()
    elif message_type == 'owner_access':
        OwnerAccessMessage(message).send()
    elif message_type == 'dev_access':
        DevAccessMessage(message).send()
    elif message_type == 'friend_added':
        FriendAddedMessage(message).send()
    else:
        raise ValueError('Invalid message type')
