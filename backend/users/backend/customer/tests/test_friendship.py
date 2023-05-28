from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from customer.models import CustomerUser, FriendShipRequest


class FriendshipViewSetTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = CustomerUser.objects.create(username='user1')
        self.user2 = CustomerUser.objects.create(username='user2')

    def test_add_friend(self):
        url = reverse('friendship-add-friend', kwargs={'pk': self.user1.pk})
        data = {'friend_id': self.user2.pk}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(FriendShipRequest.objects.count(), 1)
        self.assertEqual(FriendShipRequest.objects.first().sender, self.user1)
        self.assertEqual(FriendShipRequest.objects.first().receiver, self.user2)

    def test_accept_friend_request(self):
        friend_request = FriendShipRequest.objects.create(sender=self.user2, receiver=self.user1)
        url = reverse('friendship-accept-friend-request', kwargs={'pk': self.user1.pk})
        data = {'friend_id': self.user2.pk}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        friend_request.refresh_from_db()
        self.assertEqual(friend_request.status, FriendShipRequest.ACCEPTED)

    def test_reject_friend_request(self):
        friend_request = FriendShipRequest.objects.create(sender=self.user2, receiver=self.user1)
        url = reverse('friendship-reject-friend-request', kwargs={'pk': self.user1.pk})
        data = {'friend_id': self.user2.pk}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        friend_request.refresh_from_db()
        self.assertEqual(friend_request.status, FriendShipRequest.REJECTED)

    def test_remove_friend(self):
        friend_request_1 = FriendShipRequest.objects.create(sender=self.user1, receiver=self.user2,
                                                            status=FriendShipRequest.ACCEPTED)
        friend_request_2 = FriendShipRequest.objects.create(sender=self.user2, receiver=self.user1,
                                                            status=FriendShipRequest.ACCEPTED)
        url = reverse('friendship-remove-friend', kwargs={'pk': self.user1.pk})
        data = {'friend_id': self.user2.pk}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(FriendShipRequest.objects.count(), 0)
