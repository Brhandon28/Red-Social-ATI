from django.conf import settings
from django.db import models
from django.utils import timezone


class Publication(models.Model):
	author = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE,
		related_name='publications',
	)
	content = models.TextField()
	image = models.ImageField(upload_to='publications/', blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['-created_at']

	def __str__(self):
		return f'Publicacion {self.pk} - {self.author}'

	@property
	def summary(self):
		return self.content

	@property
	def company(self):
		return str(self.author)

	@property
	def followers(self):
		if hasattr(self.author, 'get_tipoUsuario_display'):
			return self.author.get_tipoUsuario_display()
		return 'Cuenta personal'

	@property
	def age(self):
		delta = timezone.now() - self.created_at
		if delta.days > 0:
			return f'{delta.days} d'
		hours = delta.seconds // 3600
		if hours > 0:
			return f'{hours} h'
		minutes = delta.seconds // 60
		if minutes > 0:
			return f'{minutes} min'
		return 'Ahora'


class Comment(models.Model):
	publication = models.ForeignKey(
		Publication,
		on_delete=models.CASCADE,
		related_name='comments',
	)
	parent = models.ForeignKey(
		'self',
		on_delete=models.CASCADE,
		null=True,
		blank=True,
		related_name='replies',
	)
	author = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE,
		related_name='publication_comments',
	)
	content = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['created_at']

	def __str__(self):
		return f'Comentario {self.pk} - {self.author}'

	@property
	def text(self):
		return self.content


class PublicationLike(models.Model):
	publication = models.ForeignKey(
		Publication,
		on_delete=models.CASCADE,
		related_name='likes',
	)
	user = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE,
		related_name='publication_likes',
	)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		constraints = [
			models.UniqueConstraint(
				fields=['publication', 'user'],
				name='unique_publication_like_per_user',
			)
		]

	def __str__(self):
		return f'Like pub {self.publication_id} - {self.user_id}'


class CommentLike(models.Model):
	comment = models.ForeignKey(
		Comment,
		on_delete=models.CASCADE,
		related_name='likes',
	)
	user = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE,
		related_name='comment_likes',
	)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		constraints = [
			models.UniqueConstraint(
				fields=['comment', 'user'],
				name='unique_comment_like_per_user',
			)
		]

	def __str__(self):
		return f'Like comentario {self.comment_id} - {self.user_id}'
