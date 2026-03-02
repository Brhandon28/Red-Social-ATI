"""
URL configuration for socialit project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.shortcuts import render
from django.urls import include, path


def home_view(request):
    return render(request, 'home.html')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('feed/', include('apps.feed.urls')),
    path('posts/', include('apps.posts.urls')),
    path('', home_view, name='home'),
    path('', include('apps.accounts.urls')),
    path('perfil/', include('apps.profiles.urls')),
    path('empleos/', include('apps.jobs.urls')),
    path('mi-red/', include('apps.network.urls')),
    path('notificaciones/', include('apps.notifications.urls')),
    path('chat/', include('apps.chat.urls')),
]

handler404 = 'socialit.views.custom_404'