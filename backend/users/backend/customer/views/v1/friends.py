from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from customer.models import CustomerUser, FriendShipRequest
from customer.serializers.v1.friendship_serializer import FriendShipRequestSerializer
from utils.broker.message import FriendAddedMessage
from utils.broker.rabbitmq import RabbitMQ


class FriendshipViewSet(viewsets.ModelViewSet):
    queryset = CustomerUser.objects.all()
    serializer_class = FriendShipRequestSerializer

    @action(detail=True, methods=['post'])
    def add_friend(self, request, pk=None):
        user = request.user
        friend_id = request.data.get('friend_id')
        try:
            friend = CustomerUser.objects.get(id=friend_id)
        except CustomerUser.DoesNotExist:
            return Response({'error': 'Friend not found.'}, status=status.HTTP_404_NOT_FOUND)
        friend_request = FriendShipRequest.objects.create(sender=user, receiver=friend)
        message = FriendAddedMessage(
            message={'friend_id': friend_id}
        )
        with RabbitMQ() as rabbitmq:
            rabbitmq.send_message(message)
        return Response({'success': 'Friend request sent.'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def accept_friend_request(self, request, pk=None):
        user = request.user
        friend_id = request.data.get('friend_id')
        try:
            friend = CustomerUser.objects.get(id=friend_id)
        except CustomerUser.DoesNotExist:
            return Response({'error': 'Friend not found.'}, status=status.HTTP_404_NOT_FOUND)
        friend_request = FriendShipRequest.objects.get(sender=friend, receiver=user)
        friend_request.status = FriendShipRequest.ACCEPTED
        friend_request.save()
        return Response({'success': 'Friend request accepted.'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def reject_friend_request(self, request, pk=None):
        user = request.user
        friend_id = request.data.get('friend_id')
        try:
            friend = CustomerUser.objects.get(id=friend_id)
        except CustomerUser.DoesNotExist:
            return Response({'error': 'Friend not found.'}, status=status.HTTP_404_NOT_FOUND)
        friend_request = FriendShipRequest.objects.get(sender=friend, receiver=user)
        friend_request.status = FriendShipRequest.REJECTED
        friend_request.save()
        return Response({'success': 'Friend request rejected.'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def remove_friend(self, request, pk=None):
        user = request.user
        friend_id = request.data.get('friend_id')
        try:
            friend = CustomerUser.objects.get(id=friend_id)
        except CustomerUser.DoesNotExist:
            return Response({'error': 'Friend not found.'}, status=status.HTTP_404_NOT_FOUND)
        friend_request_1 = FriendShipRequest.objects.filter(sender=user, receiver=friend).first()
        friend_request_2 = FriendShipRequest.objects.filter(sender=friend, receiver=user).first()
        if friend_request_1 and friend_request_1.status == FriendShipRequest.ACCEPTED and friend_request_2 and friend_request_2.status == FriendShipRequest.ACCEPTED:
            friend_request_1.delete()
            friend_request_2.delete()
            return Response({'success': 'Removed from friends.'}, status=status.HTTP_200_OK)
        return Response({'error': 'No friend found.'}, status=status.HTTP_400_BAD_REQUEST)
