from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.posts.models import Publication


class PostsTests(TestCase):
	def test_publication_summary_matches_content(self):
		author = get_user_model().objects.create_user(
			username='autor_posts',
			email='autor_posts@test.com',
			password='testpass123',
		)
		publication = Publication.objects.create(author=author, content='Contenido de prueba')

		self.assertEqual(publication.summary, 'Contenido de prueba')
