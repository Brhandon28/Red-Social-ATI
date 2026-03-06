from django.urls import path
from . import views

app_name = 'network'

urlpatterns = [
    path('', views.contacts, name='contacts'),
    path('conectar/<str:username>/', views.send_connection_request, name='send_connection_request'),
    path('solicitudes/<int:request_id>/aceptar/', views.accept_connection_request, name='accept_connection_request'),
    path('solicitudes/<int:request_id>/rechazar/', views.reject_connection_request, name='reject_connection_request'),
    path('<str:username>/', views.contact_profile, name='contact_profile'),
]
