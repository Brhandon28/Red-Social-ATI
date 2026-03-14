from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.posts.models import Publication, PublicationLike


class FeedTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='feed_user',
            email='feed_user@test.com',
            password='testpass123',
        )
        self.author = get_user_model().objects.create_user(
            username='autor_feed',
            email='autor_feed@test.com',
            password='testpass123',
        )
        self.publication = Publication.objects.create(author=self.author, content='Post de prueba')

    def test_toggle_publication_like_creates_and_removes_like(self):
        self.client.force_login(self.user)
        url = reverse('feed:toggle_publication_like', args=[self.publication.pk])

        self.client.post(url)
        self.assertTrue(
            PublicationLike.objects.filter(publication=self.publication, user=self.user).exists()
        )

        self.client.post(url)
        self.assertFalse(
            PublicationLike.objects.filter(publication=self.publication, user=self.user).exists()
        )
