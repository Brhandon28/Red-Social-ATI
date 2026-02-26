from django.urls import path
from . import views

app_name = 'network'

urlpatterns = [
    path('', views.contacts, name='contacts'),
    path('<str:username>/', views.contact_profile, name='contact_profile'),
]
