from django.urls import path
from . import views

app_name = 'feed'

urlpatterns = [
    path('', views.index, name='index'),
    path('empresa/', views.company_feed, name='company_feed'),
    path('publicacion/<int:post_id>/', views.post_detail, name='publication_detail'),
    path('<int:post_id>/', views.post_detail, name='post_detail'),
    path('<int:post_id>/eliminar/', views.delete_publication, name='delete_publication'),
    path('<int:post_id>/comentarios/', views.add_comment, name='add_comment'),
    path(
        '<int:post_id>/comentarios/<int:comment_id>/editar/',
        views.edit_comment,
        name='edit_comment',
    ),
    path(
        '<int:post_id>/comentarios/<int:comment_id>/eliminar/',
        views.delete_comment,
        name='delete_comment',
    ),
    path('<int:post_id>/likes/toggle/', views.toggle_publication_like, name='toggle_publication_like'),
    path(
        '<int:post_id>/comentarios/<int:comment_id>/likes/toggle/',
        views.toggle_comment_like,
        name='toggle_comment_like',
    ),
    path('publicar/', views.create_post, name='create_post'),
]
