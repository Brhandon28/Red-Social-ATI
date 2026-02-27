from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import redirect, render
from django.utils.translation import gettext_lazy as _


AUTH_COOKIE_NAME = 'hardcoded_auth'
AUTH_USER_COOKIE_NAME = 'hardcoded_user'
AUTH_COOKIE_MAX_AGE = 60 * 60 * 8


def login_view(request):
    if getattr(request, 'hardcoded_auth', False):
        return redirect('feed:index')

    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        username = (request.POST.get('username') or '').strip()
        password = request.POST.get('password') or ''

        hardcoded_user = 'admin'
        hardcoded_password = '123456'

        if username == hardcoded_user and password == hardcoded_password:
            next_url = request.GET.get('next') or 'feed:index'
            response = redirect(next_url)
            response.set_cookie(
                AUTH_COOKIE_NAME,
                '1',
                max_age=AUTH_COOKIE_MAX_AGE,
                httponly=True,
                samesite='Lax',
            )
            response.set_cookie(
                AUTH_USER_COOKIE_NAME,
                hardcoded_user,
                max_age=AUTH_COOKIE_MAX_AGE,
                httponly=True,
                samesite='Lax',
            )
            return response

        form.add_error(None, _('Credenciales inválidas.'))

    return render(request, 'accounts/login.html', {'form': form})


def register_view(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        form.add_error(None, _('Registro deshabilitado en modo hardcodeado.'))

    return render(request, 'accounts/register.html', {'form': form})


def logout_view(request):
    response = redirect('accounts:login')
    response.delete_cookie(AUTH_COOKIE_NAME)
    response.delete_cookie(AUTH_USER_COOKIE_NAME)
    return response
