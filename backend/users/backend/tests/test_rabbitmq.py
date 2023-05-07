import pika
import unittest
from unittest.mock import patch, MagicMock

from utils.broker.message import BaseMessage
from utils.broker.rabbitmq import RabbitMQ


class TestBaseMessage(unittest.TestCase):
    def test_create_base_message(self):
        message = {"Hello": "world!"}
        exchange_name = 'test_exchange'
        routing_key = 'test_queue'
        base_message = BaseMessage(exchange_name=exchange_name, routing_key=routing_key, message=message)
        self.assertEqual(base_message.exchange_name, exchange_name)
        self.assertEqual(base_message.routing_key, routing_key)
        self.assertEqual(base_message.message, message)


class TestRabbitMQ(unittest.TestCase):
    @patch('pika.BlockingConnection')
    def test_send_message(self, mock_pika):
        mock_channel = MagicMock()
        mock_pika.return_value.channel.return_value = mock_channel

        message = BaseMessage(
            exchange_name='test_exchange',
            routing_key='test_queue',
            message={'text': 'Hello, RabbitMQ!'}
        )

        with RabbitMQ() as rabbitmq:
            rabbitmq.send_message(message)

        mock_channel.basic_publish.assert_called_once_with(
            exchange='test_exchange',
            routing_key='test_queue',
            body=b'{"text": "Hello, RabbitMQ!"}'
        )

    def test_connection_closed_on_exception(self):
        with self.assertRaises(pika.exceptions.AMQPConnectionError):
            with RabbitMQ() as rabbitmq:
                raise pika.exceptions.AMQPConnectionError('Test error')
