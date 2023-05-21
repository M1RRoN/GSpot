from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from customer.models import CustomerUser
from customer.serializers.v1.friendship_serializer import UserSerializer
from utils.broker.message import FriendAddedMessage
from utils.broker.rabbitmq import RabbitMQ


class FriendshipViewSet(viewsets.ModelViewSet):
    queryset = CustomerUser.objects.all()
    serializer_class = UserSerializer

    @action(detail=True, methods=['post'])
    def add_friend(self, request, pk=None):
        user = self.get_object()
        friend_id = request.data.get('friend_id')
        try:
            friend = CustomerUser.objects.get(id=friend_id)
        except CustomerUser.DoesNotExist:
            return Response({'error': 'Friend not found.'}, status=status.HTTP_404_NOT_FOUND)
        user.friends.add(friend)
        message = FriendAddedMessage(
            exchange_name='friend_added_exchange',
            routing_key='friend_added_queue',
            message={'friend_id': friend_id}
        )
        with RabbitMQ() as rabbitmq:
            rabbitmq.send_message(message)
        return Response({'success': 'Added to friends.'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def accept_friend_request(self, request, pk=None):
        user = self.get_object()
        friend_id = request.data.get('friend_id')
        try:
            friend = CustomerUser.objects.get(id=friend_id)
        except CustomerUser.DoesNotExist:
            return Response({'error': 'Friend not found.'}, status=status.HTTP_404_NOT_FOUND)
        if user in friend.friends.all():
            user.friends.add(friend)
            return Response({'success': 'Friend request accepted.'}, status=status.HTTP_200_OK)
        return Response({'error': 'No friend request found.'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def reject_friend_request(self, request, pk=None):
        user = self.get_object()
        friend_id = request.data.get('friend_id')
        try:
            friend = CustomerUser.objects.get(id=friend_id)
        except CustomerUser.DoesNotExist:
            return Response({'error': 'Friend not found.'}, status=status.HTTP_404_NOT_FOUND)
        if user in friend.friends.all():
            user.friends.remove(friend)
            return Response({'success': 'Friend request rejected.'}, status=status.HTTP_200_OK)
        return Response({'error': 'No friend request found.'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def remove_friend(self, request, pk=None):
        user = self.get_object()
        friend_id = request.data.get('friend_id')
        try:
            friend = CustomerUser.objects.get(id=friend_id)
        except CustomerUser.DoesNotExist:
            return Response({'error': 'Friend not found.'}, status=status.HTTP_404_NOT_FOUND)
        if user in friend.friends.all() and friend in user.friends.all():
            user.friends.remove(friend)
            return Response({'success': 'Removed from friends.'}, status=status.HTTP_200_OK)
        return Response({'error': 'No friend found.'}, status=status.HTTP_400_BAD_REQUEST)
