from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class ProjectFunctionalTests(TestCase):
    def create_user(self, username, password='testpass123', **extra_fields):
        defaults = {
            'email': f'{username}@example.com',
        }
        defaults.update(extra_fields)
        return get_user_model().objects.create_user(username=username, password=password, **defaults)

    def test_edit_profile_basic_post_updates_user_information(self):
        user = self.create_user('perfil-editable', nombreMostrado='Perfil Editable')
        self.client.force_login(user)

        response = self.client.post(
            reverse('profiles:edit_profile'),
            {
                'form_type': 'basic',
                'first_name': 'Mario',
                'last_name': 'Rojas',
                'email': 'mario@example.com',
                'nombreMostrado': 'Mario Rojas',
            },
        )

        user.refresh_from_db()

        self.assertRedirects(response, reverse('profiles:my_profile'))
        self.assertEqual(user.first_name, 'Mario')
        self.assertEqual(user.last_name, 'Rojas')
        self.assertEqual(user.email, 'mario@example.com')
        self.assertEqual(user.nombreMostrado, 'Mario Rojas')