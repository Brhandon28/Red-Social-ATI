from urllib.parse import urlencode

from django.shortcuts import redirect


AUTH_COOKIE_NAME = 'hardcoded_auth'
AUTH_USER_COOKIE_NAME = 'hardcoded_user'


class HardcodedAuthMiddleware:
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
        is_hardcoded_auth = request.COOKIES.get(AUTH_COOKIE_NAME) == '1'
        request.hardcoded_auth = is_hardcoded_auth
        request.hardcoded_user = request.COOKIES.get(AUTH_USER_COOKIE_NAME, '')

        path = request.path

        if is_hardcoded_auth and path in ('/iniciar-sesion/', '/registrarse/'):
            return redirect('feed:index')

        is_public = path in self.public_paths or path.startswith(self.public_prefixes)
        is_protected = path.startswith(self.protected_prefixes)

        if (not is_hardcoded_auth) and is_protected and (not is_public):
            query = urlencode({'next': path})
            return redirect(f'/iniciar-sesion/?{query}')

        return self.get_response(request)