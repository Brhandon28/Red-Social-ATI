from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('iniciar-sesion/', views.login_view, name='login'),
    path('registrarse/', views.register_view, name='register'),
    path('cerrar-sesion/', views.logout_view, name='logout'),
]
