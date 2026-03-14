from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.network.models import ConnectionRequest


class NetworkTests(TestCase):
    def test_send_connection_request_creates_pending_relation(self):
        sender = get_user_model().objects.create_user(
            username='sender_net',
            email='sender_net@test.com',
            password='testpass123',
        )
        receiver = get_user_model().objects.create_user(
            username='receiver_net',
            email='receiver_net@test.com',
            password='testpass123',
        )
        self.client.force_login(sender)

        response = self.client.post(reverse('network:send_connection_request', args=[receiver.username]))

        self.assertRedirects(response, reverse('profiles:my_profile'))
        self.assertTrue(
            ConnectionRequest.objects.filter(
                sender=sender,
                receiver=receiver,
                status=ConnectionRequest.Status.PENDING,
            ).exists()
        )
