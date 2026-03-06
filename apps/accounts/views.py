from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.utils.translation import gettext_lazy as _

from .forms import LoginForm, RegistroEmpresaForm, RegistroProfesionalForm


def login_view(request):
    if request.user.is_authenticated:
        return redirect('feed:index')

    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            next_url = request.GET.get('next') or 'feed:index'
            return redirect(next_url)

    return render(request, 'accounts/login.html', {'form': form})


def register_view(request):
    account_type = request.POST.get('account_type', 'comun')

    if account_type == 'empresarial':
        form = RegistroEmpresaForm(request.POST or None)
    else:
        form = RegistroProfesionalForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('feed:index')

    return render(request, 'accounts/register.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('accounts:login')
