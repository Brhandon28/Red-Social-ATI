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
from django.conf.urls.i18n import i18n_patterns
from django.urls import include, path
# Importamos gettext_lazy para permitir la traducción de los textos de la propia URL
from django.utils.translation import gettext_lazy as _



def home_view(request):
    return render(request, 'home.html')

# URLs NO traducidas
# Para rutas que no necesitan el prefijo de idioma (como APIs, webhooks o archivos estáticos).
urlpatterns = [
    # Ejemplo: path('api/', include('apps.api.urls')),
]

# URLs traducidas (añaden el prefijo /es/, /en/, etc.)
# Agregamos todas las vistas de la aplicación aquí para que Django maneje el idioma correctamente.
urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('feed/', include('apps.feed.urls')),
    path('posts/', include('apps.posts.urls')),
    path('', home_view, name='home'),
    path('', include('apps.accounts.urls')),
    
    # Usando _() permitimos que la ruta cambie según el idioma 
    # (ej. /es/empleos/ vs /en/jobs/)
    path(_('perfil/'), include('apps.profiles.urls')),
    path(_('empleos/'), include('apps.jobs.urls')),
    path(_('mi-red/'), include('apps.network.urls')),
    path(_('notificaciones/'), include('apps.notifications.urls')),
    path(_('chat/'), include('apps.chat.urls')),
)

handler404 = 'socialit.views.custom_404'
#handler500 = 'socialit.views.custom_500'