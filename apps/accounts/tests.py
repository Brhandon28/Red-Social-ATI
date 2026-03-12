from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class AccountsTests(TestCase):
    def test_login_view_redirects_authenticated_user(self):
        user = get_user_model().objects.create_user(
            username='cuenta_test',
            email='cuenta@test.com',
            password='testpass123',
        )
        self.client.force_login(user)

        response = self.client.get(reverse('accounts:login'))

        self.assertRedirects(response, reverse('feed:index'))
