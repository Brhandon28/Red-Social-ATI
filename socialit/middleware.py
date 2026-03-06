from urllib.parse import urlencode

from django.conf import settings
from django.shortcuts import redirect


class LoginRequiredMiddleware:
    """
    Middleware that redirects unauthenticated users to the login page
    for protected paths, using Django's built-in authentication system.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.public_paths = {
            '/',
            '/iniciar-sesion/',
            '/registrarse/',
        }
        self.public_prefixes = (
            '/admin/',
            '/static/',
            '/media/',
        )
        self.protected_prefixes = (
            '/feed/',
            '/perfil/',
            '/empleos/',
            '/mi-red/',
            '/notificaciones/',
            '/chat/',
            '/cerrar-sesion/',
        )

    def __call__(self, request):
        path = request.path
        is_authenticated = request.user.is_authenticated

        if is_authenticated and path in ('/iniciar-sesion/', '/registrarse/'):
            return redirect('feed:index')

        is_public = path in self.public_paths or path.startswith(self.public_prefixes)
        is_protected = path.startswith(self.protected_prefixes)

        if (not is_authenticated) and is_protected and (not is_public):
            login_url = getattr(settings, 'LOGIN_URL', '/iniciar-sesion/')
            query = urlencode({'next': path})
            return redirect(f'{login_url}?{query}')

        return self.get_response(request)