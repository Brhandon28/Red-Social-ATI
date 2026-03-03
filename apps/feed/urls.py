from django.urls import path
from . import views

app_name = 'feed'

urlpatterns = [
    path('', views.index, name='index'),
    path('empresa/', views.company_feed, name='company_feed'),
    path('publicacion/<int:post_id>/', views.post_detail, name='publication_detail'),
    path('<int:post_id>/', views.post_detail, name='post_detail'),
    path('publicar/', views.create_post, name='create_post'),
]
