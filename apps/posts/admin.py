from django.contrib import admin

from .models import Comment, CommentLike, Publication, PublicationLike


@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
	list_display = ('id', 'author', 'created_at')
	search_fields = ('author__username', 'author__nombreMostrado', 'content')
	list_filter = ('created_at',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
	list_display = ('id', 'publication', 'author', 'created_at')
	search_fields = ('author__username', 'author__nombreMostrado', 'content')
	list_filter = ('created_at',)


@admin.register(PublicationLike)
class PublicationLikeAdmin(admin.ModelAdmin):
	list_display = ('id', 'publication', 'user', 'created_at')
	list_filter = ('created_at',)


@admin.register(CommentLike)
class CommentLikeAdmin(admin.ModelAdmin):
	list_display = ('id', 'comment', 'user', 'created_at')
	list_filter = ('created_at',)
