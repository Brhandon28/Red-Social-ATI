from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.inbox, name='inbox'),
    path('<int:chat_id>/', views.chat_detail, name='chat_detail'),
]
